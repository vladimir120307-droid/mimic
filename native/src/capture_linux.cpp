#if defined(__linux__)

#include "mimic/capture.h"
#include "mimic/dedup.h"

#include <atomic>
#include <chrono>
#include <cstring>
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include <sys/ipc.h>
#include <sys/shm.h>

#include <xcb/shm.h>
#include <xcb/xcb.h>

namespace mimic {

using namespace std::chrono;

namespace {

class XcbShmCapturer final : public Capturer {
public:
    XcbShmCapturer()  = default;
    ~XcbShmCapturer() override { stop(); release_shm(); }

    bool start(const CaptureConfig& config, FrameCallback on_frame) override {
        if (running_.exchange(true)) return false;
        config_   = config;
        callback_ = std::move(on_frame);

        if (!ensure_connection()) {
            running_.store(false);
            return false;
        }
        worker_ = std::thread([this] { run_(); });
        return true;
    }

    void stop() override {
        if (!running_.exchange(false)) return;
        if (worker_.joinable()) worker_.join();
    }

    bool is_running() const override { return running_.load(); }

    std::optional<Frame> grab_one(const CaptureConfig& config) override {
        if (!ensure_connection()) return std::nullopt;
        for (int attempt = 0; attempt < 5; ++attempt) {
            Frame f;
            if (capture_once(config, f)) return f;
        }
        return std::nullopt;
    }

private:
    bool ensure_connection() {
        if (connection_) return true;
        connection_ = xcb_connect(nullptr, nullptr);
        if (!connection_ || xcb_connection_has_error(connection_)) {
            release_connection();
            return false;
        }
        const xcb_setup_t*       setup    = xcb_get_setup(connection_);
        xcb_screen_iterator_t    iterator = xcb_setup_roots_iterator(setup);
        screen_                           = iterator.data;
        if (!screen_) {
            release_connection();
            return false;
        }
        // Probe for MIT-SHM extension
        xcb_query_extension_cookie_t cookie =
            xcb_query_extension(connection_, 7, "MIT-SHM");
        xcb_query_extension_reply_t* reply =
            xcb_query_extension_reply(connection_, cookie, nullptr);
        shm_available_ = reply && reply->present;
        free(reply);
        return true;
    }

    void release_connection() {
        if (connection_) xcb_disconnect(connection_);
        connection_ = nullptr;
        screen_     = nullptr;
    }

    bool ensure_shm(int width, int height) {
        if (shm_seg_ && shm_w_ == width && shm_h_ == height) return true;
        release_shm();

        if (!shm_available_) return false;
        const size_t bytes = static_cast<size_t>(width) * height * 4;
        shm_id_            = shmget(IPC_PRIVATE, bytes, IPC_CREAT | 0600);
        if (shm_id_ < 0) return false;
        shm_addr_ = static_cast<uint8_t*>(shmat(shm_id_, nullptr, 0));
        if (shm_addr_ == reinterpret_cast<void*>(-1)) {
            shmctl(shm_id_, IPC_RMID, nullptr);
            shm_id_ = -1;
            return false;
        }
        shm_seg_ = xcb_generate_id(connection_);
        xcb_void_cookie_t cookie =
            xcb_shm_attach_checked(connection_, shm_seg_, shm_id_, 0);
        xcb_generic_error_t* err = xcb_request_check(connection_, cookie);
        if (err) {
            free(err);
            release_shm();
            return false;
        }
        shm_w_ = width;
        shm_h_ = height;
        return true;
    }

    void release_shm() {
        if (shm_seg_) {
            xcb_shm_detach(connection_, shm_seg_);
            shm_seg_ = 0;
        }
        if (shm_addr_ && shm_addr_ != reinterpret_cast<void*>(-1)) {
            shmdt(shm_addr_);
            shm_addr_ = nullptr;
        }
        if (shm_id_ >= 0) {
            shmctl(shm_id_, IPC_RMID, nullptr);
            shm_id_ = -1;
        }
        shm_w_ = shm_h_ = 0;
    }

    bool capture_once(const CaptureConfig& cfg, Frame& out) {
        if (!screen_) return false;
        const int w = screen_->width_in_pixels;
        const int h = screen_->height_in_pixels;

        if (shm_available_ && ensure_shm(w, h)) {
            xcb_shm_get_image_cookie_t cookie = xcb_shm_get_image(
                connection_, screen_->root, 0, 0, w, h, ~0,
                XCB_IMAGE_FORMAT_Z_PIXMAP, shm_seg_, 0);
            xcb_generic_error_t*       err = nullptr;
            xcb_shm_get_image_reply_t* reply =
                xcb_shm_get_image_reply(connection_, cookie, &err);
            if (!reply) {
                if (err) free(err);
                return false;
            }
            populate_frame(out, w, h, shm_addr_, w * 4, cfg);
            free(reply);
            return true;
        }
        // Fallback: regular xcb_get_image (slower).
        xcb_get_image_cookie_t cookie = xcb_get_image(
            connection_, XCB_IMAGE_FORMAT_Z_PIXMAP, screen_->root, 0, 0, w, h, ~0);
        xcb_generic_error_t*  err   = nullptr;
        xcb_get_image_reply_t* reply =
            xcb_get_image_reply(connection_, cookie, &err);
        if (!reply) {
            if (err) free(err);
            return false;
        }
        uint8_t*   data = xcb_get_image_data(reply);
        const int  len  = xcb_get_image_data_length(reply);
        const int  stride = len / std::max(1, h);
        populate_frame(out, w, h, data, stride, cfg);
        free(reply);
        return true;
    }

    void populate_frame(Frame&         out,
                        int            w,
                        int            h,
                        const uint8_t* src,
                        int            stride,
                        const CaptureConfig& /*cfg*/) {
        out.width        = w;
        out.height       = h;
        out.stride       = stride;
        out.format       = PixelFormat::BGRA8;
        out.timestamp_ns = duration_cast<nanoseconds>(
                               steady_clock::now().time_since_epoch())
                               .count();
        out.data.assign(src, src + static_cast<size_t>(stride) * h);
    }

    void run_() {
        Deduplicator dedup(config_.dedup_threshold);
        const auto   target =
            milliseconds(1000 / std::max(1, config_.target_fps));
        while (running_.load()) {
            const auto t0 = steady_clock::now();
            Frame      frame;
            if (capture_once(config_, frame)) {
                if (!config_.enable_dedup || dedup.accept(frame)) {
                    if (callback_) callback_(frame);
                }
            }
            const auto elapsed =
                duration_cast<milliseconds>(steady_clock::now() - t0);
            if (elapsed < target) std::this_thread::sleep_for(target - elapsed);
        }
    }

    std::atomic<bool>           running_{false};
    std::thread                 worker_;
    CaptureConfig               config_{};
    FrameCallback               callback_;

    xcb_connection_t*           connection_     = nullptr;
    xcb_screen_t*               screen_         = nullptr;
    bool                        shm_available_  = false;

    xcb_shm_seg_t               shm_seg_  = 0;
    int                         shm_id_   = -1;
    uint8_t*                    shm_addr_ = nullptr;
    int                         shm_w_    = 0;
    int                         shm_h_    = 0;
};

}

std::unique_ptr<Capturer> make_linux_capturer() {
    return std::make_unique<XcbShmCapturer>();
}

std::vector<DisplayInfo> list_displays() {
    std::vector<DisplayInfo> result;
    xcb_connection_t* conn = xcb_connect(nullptr, nullptr);
    if (!conn || xcb_connection_has_error(conn)) {
        if (conn) xcb_disconnect(conn);
        DisplayInfo fb;
        fb.index      = 0;
        fb.name       = "no-x11";
        fb.bounds     = Rect{0, 0, 1920, 1080};
        fb.dpi_scale  = 1.0f;
        fb.is_primary = true;
        result.push_back(fb);
        return result;
    }
    const xcb_setup_t*    setup = xcb_get_setup(conn);
    xcb_screen_iterator_t it    = xcb_setup_roots_iterator(setup);
    int index = 0;
    for (; it.rem; xcb_screen_next(&it), ++index) {
        DisplayInfo di;
        di.index      = index;
        di.name       = "screen-" + std::to_string(index);
        di.bounds     = Rect{0, 0, it.data->width_in_pixels, it.data->height_in_pixels};
        di.dpi_scale  = 1.0f;
        di.is_primary = (index == 0);
        result.push_back(di);
    }
    xcb_disconnect(conn);
    return result;
}

}

#endif
