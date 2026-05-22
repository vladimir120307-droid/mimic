#if defined(_WIN32)

#include "mimic/capture.h"

#include <atomic>
#include <memory>
#include <thread>

namespace mimic {

class WindowsCapturer final : public Capturer {
public:
    ~WindowsCapturer() override { stop(); }

    bool start(const CaptureConfig& config, FrameCallback on_frame) override {
        if (running_.exchange(true)) return false;
        config_   = config;
        callback_ = std::move(on_frame);
        worker_   = std::thread([this] { run(); });
        return true;
    }

    void stop() override {
        if (!running_.exchange(false)) return;
        if (worker_.joinable()) worker_.join();
    }

    bool is_running() const override { return running_.load(); }

    std::optional<Frame> grab_one(const CaptureConfig& /*config*/) override {
        // TODO: implement single-frame DXGI capture
        return std::nullopt;
    }

private:
    void run() {
        // TODO: IDXGIOutputDuplication acquisition loop
        // 1. CreateDXGIFactory1 -> IDXGIAdapter1 -> IDXGIOutput1::DuplicateOutput
        // 2. AcquireNextFrame -> CopyResource to staging texture
        // 3. Map -> emit Frame via callback_
        // 4. ReleaseFrame, sleep to honor target_fps
        while (running_.load()) {
            std::this_thread::sleep_for(
                std::chrono::milliseconds(1000 / std::max(1, config_.target_fps))
            );
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
    // TODO: EnumDisplayMonitors / IDXGIAdapter1::EnumOutputs
    DisplayInfo primary;
    primary.index      = 0;
    primary.name       = "Primary";
    primary.bounds     = Rect{0, 0, 1920, 1080};
    primary.dpi_scale  = 1.0f;
    primary.is_primary = true;
    return {primary};
}

}

#endif
