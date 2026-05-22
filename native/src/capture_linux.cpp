#if defined(__linux__)

#include "mimic/capture.h"

#include <atomic>
#include <memory>
#include <thread>

namespace mimic {

class LinuxCapturer final : public Capturer {
public:
    ~LinuxCapturer() override { stop(); }

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

    std::optional<Frame> grab_one(const CaptureConfig&) override {
        // TODO: PipeWire portal one-shot, XCB shm fallback
        return std::nullopt;
    }

private:
    void run() {
        // TODO: PipeWire stream loop (org.freedesktop.portal.ScreenCast)
        // Fallback: XCB shm GetImage when PipeWire unavailable
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

std::unique_ptr<Capturer> make_linux_capturer() {
    return std::make_unique<LinuxCapturer>();
}

std::vector<DisplayInfo> list_displays() {
    // TODO: enumerate via Wayland output globals or X11 RandR
    DisplayInfo primary;
    primary.index      = 0;
    primary.name       = "primary";
    primary.bounds     = Rect{0, 0, 1920, 1080};
    primary.dpi_scale  = 1.0f;
    primary.is_primary = true;
    return {primary};
}

}

#endif
