#if defined(__APPLE__)

#include "mimic/capture.h"

#include <atomic>
#include <memory>

namespace mimic {

class MacOSCapturer final : public Capturer {
public:
    ~MacOSCapturer() override { stop(); }

    bool start(const CaptureConfig& config, FrameCallback on_frame) override {
        if (running_.exchange(true)) return false;
        config_   = config;
        callback_ = std::move(on_frame);
        // TODO: SCStream initialization, request capture permission
        return true;
    }

    void stop() override {
        if (!running_.exchange(false)) return;
        // TODO: SCStream stopCapture
    }

    bool is_running() const override { return running_.load(); }

    std::optional<Frame> grab_one(const CaptureConfig&) override {
        // TODO: CGWindowListCreateImage or SCScreenshotManager (macOS 14+)
        return std::nullopt;
    }

private:
    std::atomic<bool> running_{false};
    CaptureConfig     config_{};
    FrameCallback     callback_;
};

std::unique_ptr<Capturer> make_macos_capturer() {
    return std::make_unique<MacOSCapturer>();
}

std::vector<DisplayInfo> list_displays() {
    // TODO: CGGetActiveDisplayList + CGDisplayBounds
    DisplayInfo primary;
    primary.index      = 0;
    primary.name       = "Built-in Retina Display";
    primary.bounds     = Rect{0, 0, 2880, 1800};
    primary.dpi_scale  = 2.0f;
    primary.is_primary = true;
    return {primary};
}

}

#endif
