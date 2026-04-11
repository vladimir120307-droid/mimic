#if defined(_WIN32)

#include "mimic/capture.h"
#include "mimic/dedup.h"
#include "mimic/win_util.h"

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstring>
#include <memory>
#include <mutex>
#include <thread>
#include <vector>

#include <d3d11.h>
#include <dxgi1_2.h>

#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "dxgi.lib")

namespace mimic {

using win::ComPtr;
using win::HResultError;
using namespace std::chrono;

namespace {

class DxgiSession {
public:
    DxgiSession(int display_index) {
        ComPtr<IDXGIFactory1> factory;
        MIMIC_THROW_IF_FAILED(CreateDXGIFactory1(IID_PPV_ARGS(&factory)));

        ComPtr<IDXGIAdapter1> adapter;
        MIMIC_THROW_IF_FAILED(factory->EnumAdapters1(0, &adapter));

        const D3D_FEATURE_LEVEL levels[] = {
            D3D_FEATURE_LEVEL_11_1,
            D3D_FEATURE_LEVEL_11_0,
            D3D_FEATURE_LEVEL_10_1,
            D3D_FEATURE_LEVEL_10_0,
        };
        D3D_FEATURE_LEVEL got = D3D_FEATURE_LEVEL_11_0;
        MIMIC_THROW_IF_FAILED(D3D11CreateDevice(
            adapter.Get(),
            D3D_DRIVER_TYPE_UNKNOWN,
            nullptr,
            0,
            levels,
            ARRAYSIZE(levels),
            D3D11_SDK_VERSION,
            &device_,
            &got,
            &context_));

        ComPtr<IDXGIOutput> output;
        const UINT idx = static_cast<UINT>(std::max(0, display_index));
        MIMIC_THROW_IF_FAILED(adapter->EnumOutputs(idx, &output));

        ComPtr<IDXGIOutput1> output1;
        MIMIC_THROW_IF_FAILED(output.As(&output1));

        DXGI_OUTPUT_DESC od{};
        MIMIC_THROW_IF_FAILED(output->GetDesc(&od));
        output_origin_x_ = od.DesktopCoordinates.left;
        output_origin_y_ = od.DesktopCoordinates.top;

        MIMIC_THROW_IF_FAILED(output1->DuplicateOutput(device_.Get(), &duplication_));
    }

    bool acquire(Frame& out, int timeout_ms, bool include_cursor) {
        DXGI_OUTDUPL_FRAME_INFO info{};
        ComPtr<IDXGIResource> resource;
        HRESULT hr = duplication_->AcquireNextFrame(
            static_cast<UINT>(timeout_ms), &info, &resource);
        if (hr == DXGI_ERROR_WAIT_TIMEOUT) {
            return false;
        }
        if (hr == DXGI_ERROR_ACCESS_LOST) {
            duplication_.Reset();
            throw HResultError(hr, "DXGI access lost");
        }
        if (FAILED(hr)) {
            throw HResultError(hr, "AcquireNextFrame");
        }

        struct ReleaseGuard {
            IDXGIOutputDuplication* dup;
            ~ReleaseGuard() { dup->ReleaseFrame(); }
        } guard{duplication_.Get()};

        ComPtr<ID3D11Texture2D> desktop_image;
        MIMIC_THROW_IF_FAILED(resource.As(&desktop_image));

        D3D11_TEXTURE2D_DESC desc{};
        desktop_image->GetDesc(&desc);

        ensure_staging_(desc);
        context_->CopyResource(staging_.Get(), desktop_image.Get());

        if (include_cursor && info.PointerPosition.Visible) {
            cache_pointer_(*duplication_.Get(), info);
        }

        D3D11_MAPPED_SUBRESOURCE mapped{};
        MIMIC_THROW_IF_FAILED(context_->Map(
            staging_.Get(), 0, D3D11_MAP_READ, 0, &mapped));

        out.width        = static_cast<int32_t>(desc.Width);
        out.height       = static_cast<int32_t>(desc.Height);
        out.stride       = static_cast<int32_t>(mapped.RowPitch);
        out.format       = PixelFormat::BGRA8;
        out.timestamp_ns = duration_cast<nanoseconds>(
                               steady_clock::now().time_since_epoch())
                               .count();

        out.data.resize(static_cast<size_t>(mapped.RowPitch) * desc.Height);
        std::memcpy(out.data.data(), mapped.pData, out.data.size());

        context_->Unmap(staging_.Get(), 0);

        if (include_cursor && info.PointerPosition.Visible) {
            out.cursor_x = info.PointerPosition.Position.x - output_origin_x_;
            out.cursor_y = info.PointerPosition.Position.y - output_origin_y_;
            composite_cursor_(out);
        } else {
            out.cursor_x = -1;
            out.cursor_y = -1;
        }
        out.mouse_down = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;
        return true;
    }

private:
    void ensure_staging_(const D3D11_TEXTURE2D_DESC& desc) {
        if (staging_ && staging_w_ == desc.Width && staging_h_ == desc.Height) return;
        D3D11_TEXTURE2D_DESC sd = desc;
        sd.Usage          = D3D11_USAGE_STAGING;
        sd.BindFlags      = 0;
        sd.CPUAccessFlags = D3D11_CPU_ACCESS_READ;
        sd.MiscFlags      = 0;
        staging_.Reset();
        MIMIC_THROW_IF_FAILED(device_->CreateTexture2D(&sd, nullptr, &staging_));
        staging_w_ = desc.Width;
        staging_h_ = desc.Height;
    }

    void cache_pointer_(IDXGIOutputDuplication&         dup,
                        const DXGI_OUTDUPL_FRAME_INFO&  info) {
        if (info.PointerShapeBufferSize == 0) return;
        if (pointer_buffer_.size() < info.PointerShapeBufferSize) {
            pointer_buffer_.resize(info.PointerShapeBufferSize);
        }
        UINT required = 0;
        const HRESULT hr = dup.GetFramePointerShape(
            static_cast<UINT>(pointer_buffer_.size()),
            pointer_buffer_.data(),
            &required,
            &pointer_info_);
        if (FAILED(hr)) {
            pointer_info_ = {};
        }
    }

    void composite_cursor_(Frame& frame) {
        if (pointer_info_.Width == 0 || pointer_info_.Height == 0) return;
        if (pointer_buffer_.empty()) return;
        if (frame.cursor_x < 0 || frame.cursor_y < 0) return;

        // Only handle DXGI_OUTDUPL_POINTER_SHAPE_TYPE_COLOR (1) in this scaffold.
        // Monochrome (2) and masked color (4) are TODO — most modern cursors are COLOR.
        if (pointer_info_.Type != DXGI_OUTDUPL_POINTER_SHAPE_TYPE_COLOR) return;

        const int cw = static_cast<int>(pointer_info_.Width);
        const int ch = static_cast<int>(pointer_info_.Height);
        const int pitch = static_cast<int>(pointer_info_.Pitch);

        for (int y = 0; y < ch; ++y) {
            const int dst_y = frame.cursor_y + y;
            if (dst_y < 0 || dst_y >= frame.height) continue;
            const uint8_t* src_row =
                pointer_buffer_.data() + static_cast<size_t>(y) * pitch;
            uint8_t* dst_row =
                frame.data.data() + static_cast<size_t>(dst_y) * frame.stride;
            for (int x = 0; x < cw; ++x) {
                const int dst_x = frame.cursor_x + x;
                if (dst_x < 0 || dst_x >= frame.width) continue;
                const uint8_t* sp = src_row + static_cast<size_t>(x) * 4;
                uint8_t*       dp = dst_row + static_cast<size_t>(dst_x) * 4;
                const float a = sp[3] / 255.0f;
                dp[0] = static_cast<uint8_t>(sp[0] * a + dp[0] * (1.0f - a));
                dp[1] = static_cast<uint8_t>(sp[1] * a + dp[1] * (1.0f - a));
                dp[2] = static_cast<uint8_t>(sp[2] * a + dp[2] * (1.0f - a));
                dp[3] = 0xFF;
            }
        }
    }

    ComPtr<ID3D11Device>           device_;
    ComPtr<ID3D11DeviceContext>    context_;
    ComPtr<IDXGIOutputDuplication> duplication_;
    ComPtr<ID3D11Texture2D>        staging_;
    UINT                           staging_w_       = 0;
    UINT                           staging_h_       = 0;
    int32_t                        output_origin_x_ = 0;
    int32_t                        output_origin_y_ = 0;
    std::vector<uint8_t>           pointer_buffer_;
    DXGI_OUTDUPL_POINTER_SHAPE_INFO pointer_info_{};
};

}

class WindowsCapturer final : public Capturer {
public:
    ~WindowsCapturer() override { stop(); }

    bool start(const CaptureConfig& config, FrameCallback on_frame) override {
        if (running_.exchange(true)) return false;
        config_   = config;
        callback_ = std::move(on_frame);
        worker_   = std::thread([this] { run_(); });
        return true;
    }

    void stop() override {
        if (!running_.exchange(false)) return;
        if (worker_.joinable()) worker_.join();
    }

    bool is_running() const override { return running_.load(); }

    std::optional<Frame> grab_one(const CaptureConfig& config) override {
        try {
            DxgiSession session(config.display_index.value_or(0));
            Frame       f;
            for (int attempt = 0; attempt < 30; ++attempt) {
                if (session.acquire(f, 100, config.include_cursor)) return f;
            }
        } catch (const HResultError&) {
            return std::nullopt;
        }
        return std::nullopt;
    }

private:
    void run_() {
        Deduplicator    dedup(config_.dedup_threshold);
        const auto      target_ms =
            milliseconds(1000 / std::max(1, config_.target_fps));

        std::unique_ptr<DxgiSession> session;
        try {
            session = std::make_unique<DxgiSession>(
                config_.display_index.value_or(0));
        } catch (const HResultError&) {
            running_.store(false);
            return;
        }

        while (running_.load()) {
            const auto t0 = steady_clock::now();
            Frame      frame;
            try {
                if (!session->acquire(frame, 100, config_.include_cursor)) {
                    continue;
                }
            } catch (const HResultError&) {
                try {
                    session = std::make_unique<DxgiSession>(
                        config_.display_index.value_or(0));
                } catch (const HResultError&) {
                    break;
                }
                continue;
            }

            if (!config_.enable_dedup || dedup.accept(frame)) {
                if (callback_) callback_(frame);
            }

            const auto elapsed =
                duration_cast<milliseconds>(steady_clock::now() - t0);
            if (elapsed < target_ms) {
                std::this_thread::sleep_for(target_ms - elapsed);
            }
        }
    }

    std::atomic<bool> running_{false};
    std::thread       worker_;
    CaptureConfig     config_{};
    FrameCallback     callback_;
};

std::unique_ptr<Capturer> make_windows_capturer() {
    return std::make_unique<WindowsCapturer>();
}

std::vector<DisplayInfo> list_displays() {
    std::vector<DisplayInfo> result;
    try {
        ComPtr<IDXGIFactory1> factory;
        MIMIC_THROW_IF_FAILED(CreateDXGIFactory1(IID_PPV_ARGS(&factory)));

        ComPtr<IDXGIAdapter1> adapter;
        if (FAILED(factory->EnumAdapters1(0, &adapter))) return result;

        ComPtr<IDXGIOutput> output;
        for (UINT i = 0; adapter->EnumOutputs(i, &output) != DXGI_ERROR_NOT_FOUND; ++i) {
            DXGI_OUTPUT_DESC od{};
            if (FAILED(output->GetDesc(&od))) continue;

            char name[64] = {};
            WideCharToMultiByte(
                CP_UTF8, 0, od.DeviceName, -1, name, sizeof(name), nullptr, nullptr);

            DisplayInfo di;
            di.index      = static_cast<int32_t>(i);
            di.name       = name;
            di.bounds.x   = od.DesktopCoordinates.left;
            di.bounds.y   = od.DesktopCoordinates.top;
            di.bounds.width =
                od.DesktopCoordinates.right - od.DesktopCoordinates.left;
            di.bounds.height =
                od.DesktopCoordinates.bottom - od.DesktopCoordinates.top;

            HMONITOR    monitor = od.Monitor;
            MONITORINFO mi{};
            mi.cbSize = sizeof(mi);
            if (GetMonitorInfoW(monitor, &mi)) {
                di.is_primary = (mi.dwFlags & MONITORINFOF_PRIMARY) != 0;
            }

            UINT dpi_x = 96, dpi_y = 96;
            if (auto get_dpi = reinterpret_cast<HRESULT (WINAPI*)(HMONITOR, int, UINT*, UINT*)>(
                    GetProcAddress(GetModuleHandleW(L"shcore.dll"), "GetDpiForMonitor"))) {
                get_dpi(monitor, 0 /* MDT_EFFECTIVE_DPI */, &dpi_x, &dpi_y);
            }
            di.dpi_scale = static_cast<float>(dpi_x) / 96.0f;

            result.push_back(std::move(di));
            output.Reset();
        }
    } catch (const HResultError&) {
        // Fall through with whatever we collected.
    }
    if (result.empty()) {
        DisplayInfo fallback;
        fallback.index      = 0;
        fallback.name       = "Primary";
        fallback.bounds     = Rect{0, 0, 1920, 1080};
        fallback.dpi_scale  = 1.0f;
        fallback.is_primary = true;
        result.push_back(fallback);
    }
    return result;
}

}

#endif
