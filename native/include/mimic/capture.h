#pragma once

#include <chrono>
#include <cstdint>
#include <functional>
#include <memory>
#include <optional>
#include <string>
#include <vector>

namespace mimic {

struct Rect {
    int32_t x      = 0;
    int32_t y      = 0;
    int32_t width  = 0;
    int32_t height = 0;
};

enum class PixelFormat : uint8_t {
    BGRA8,
    RGBA8,
};

struct Frame {
    std::vector<uint8_t> data;
    int32_t              width        = 0;
    int32_t              height       = 0;
    int32_t              stride       = 0;
    PixelFormat          format       = PixelFormat::BGRA8;
    int64_t              timestamp_ns = 0;
    int32_t              cursor_x     = -1;
    int32_t              cursor_y     = -1;
    bool                 mouse_down   = false;
};

struct CaptureConfig {
    std::optional<Rect> region;
    int32_t             target_fps         = 30;
    bool                include_cursor     = true;
    bool                enable_dedup       = true;
    float               dedup_threshold    = 0.02f;
    std::optional<int>  display_index;
};

using FrameCallback = std::function<void(const Frame&)>;

class Capturer {
public:
    virtual ~Capturer() = default;

    virtual bool start(const CaptureConfig& config, FrameCallback on_frame) = 0;
    virtual void stop()                                                     = 0;
    virtual bool is_running() const                                         = 0;

    virtual std::optional<Frame> grab_one(const CaptureConfig& config)      = 0;
};

std::unique_ptr<Capturer> make_capturer();

struct DisplayInfo {
    int32_t     index         = 0;
    std::string name;
    Rect        bounds;
    float       dpi_scale     = 1.0f;
    bool        is_primary    = false;
};

std::vector<DisplayInfo> list_displays();

const char* platform_name();
const char* version();

}
