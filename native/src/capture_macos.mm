#if defined(__APPLE__)

#include "mimic/capture.h"

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <memory>
#include <mutex>
#include <vector>

#import <AVFoundation/AVFoundation.h>
#import <CoreGraphics/CoreGraphics.h>
#import <CoreMedia/CoreMedia.h>
#import <CoreVideo/CoreVideo.h>
#import <Foundation/Foundation.h>
#import <ScreenCaptureKit/ScreenCaptureKit.h>

@class MimicStreamHandler;

namespace mimic {

namespace {

using namespace std::chrono;

struct StreamContext {
    std::mutex                  mutex;
    Deduplicator                dedup{0.02f};
    CaptureConfig               config;
    FrameCallback               callback;
    bool                        running = false;
};

}

}

@interface MimicStreamHandler : NSObject <SCStreamOutput, SCStreamDelegate>
@property (nonatomic, assign) mimic::StreamContext* ctx;
@end

@implementation MimicStreamHandler

- (void)stream:(SCStream*)stream
    didOutputSampleBuffer:(CMSampleBufferRef)sampleBuffer
                   ofType:(SCStreamOutputType)type {
    if (type != SCStreamOutputTypeScreen) return;
    if (!CMSampleBufferIsValid(sampleBuffer)) return;
    if (!_ctx) return;

    CVPixelBufferRef pb = CMSampleBufferGetImageBuffer(sampleBuffer);
    if (!pb) return;

    if (CVPixelBufferLockBaseAddress(pb, kCVPixelBufferLock_ReadOnly) != kCVReturnSuccess) {
        return;
    }

    const size_t w      = CVPixelBufferGetWidth(pb);
    const size_t h      = CVPixelBufferGetHeight(pb);
    const size_t stride = CVPixelBufferGetBytesPerRow(pb);
    const auto*  src    = static_cast<const uint8_t*>(CVPixelBufferGetBaseAddress(pb));

    mimic::Frame frame;
    frame.width        = static_cast<int32_t>(w);
    frame.height       = static_cast<int32_t>(h);
    frame.stride       = static_cast<int32_t>(stride);
    frame.format       = mimic::PixelFormat::BGRA8;
    frame.timestamp_ns = duration_cast<std::chrono::nanoseconds>(
                             std::chrono::steady_clock::now().time_since_epoch())
                             .count();
    frame.data.assign(src, src + stride * h);

    CVPixelBufferUnlockBaseAddress(pb, kCVPixelBufferLock_ReadOnly);

    std::lock_guard<std::mutex> lock(_ctx->mutex);
    if (!_ctx->running) return;
    if (!_ctx->config.enable_dedup || _ctx->dedup.accept(frame)) {
        if (_ctx->callback) _ctx->callback(frame);
    }
}

- (void)stream:(SCStream*)stream didStopWithError:(NSError*)error {
    if (!_ctx) return;
    std::lock_guard<std::mutex> lock(_ctx->mutex);
    _ctx->running = false;
}

@end

namespace mimic {

class MacOSCapturer final : public Capturer {
public:
    MacOSCapturer()  = default;
    ~MacOSCapturer() override { stop(); }

    bool start(const CaptureConfig& config, FrameCallback on_frame) override {
        if (ctx_.running) return false;

        ctx_.config   = config;
        ctx_.callback = std::move(on_frame);
        ctx_.dedup    = Deduplicator(config.dedup_threshold);
        ctx_.running  = true;

        __block bool ok = false;
        dispatch_semaphore_t sem = dispatch_semaphore_create(0);
        [SCShareableContent
            getShareableContentExcludingDesktopWindows:NO
                                  onScreenWindowsOnly:YES
                                    completionHandler:^(SCShareableContent* c, NSError* e) {
                                        if (c && c.displays.count > 0) {
                                            ok = [self _startWithContent:c];
                                        }
                                        dispatch_semaphore_signal(sem);
                                    }];
        dispatch_semaphore_wait(sem, dispatch_time(DISPATCH_TIME_NOW, NSEC_PER_SEC * 5));

        if (!ok) {
            ctx_.running = false;
            return false;
        }
        return true;
    }

    void stop() override {
        if (!ctx_.running) return;
        ctx_.running = false;
        if (stream_) {
            [stream_ stopCaptureWithCompletionHandler:^(NSError*){}];
            stream_  = nil;
            handler_ = nil;
        }
    }

    bool is_running() const override { return ctx_.running; }

    std::optional<Frame> grab_one(const CaptureConfig& config) override {
        std::mutex             m;
        std::condition_variable cv;
        std::optional<Frame>   result;
        bool                   ready = false;

        bool started = start(config, [&](const Frame& f) {
            std::lock_guard<std::mutex> g(m);
            if (!ready) {
                result = f;
                ready  = true;
            }
            cv.notify_one();
        });
        if (!started) return std::nullopt;

        std::unique_lock<std::mutex> lock(m);
        cv.wait_for(lock, std::chrono::seconds(2), [&] { return ready; });
        stop();
        return result;
    }

private:
    bool _startWithContent(SCShareableContent* content) {
        SCDisplay* display = content.displays.firstObject;
        if (!display) return false;

        SCContentFilter* filter =
            [[SCContentFilter alloc] initWithDisplay:display excludingWindows:@[]];

        SCStreamConfiguration* cfg = [[SCStreamConfiguration alloc] init];
        cfg.width            = display.width;
        cfg.height           = display.height;
        cfg.minimumFrameInterval =
            CMTimeMake(1, std::max(1, ctx_.config.target_fps));
        cfg.pixelFormat      = kCVPixelFormatType_32BGRA;
        cfg.showsCursor      = ctx_.config.include_cursor;
        cfg.queueDepth       = 6;

        handler_     = [[MimicStreamHandler alloc] init];
        handler_.ctx = &ctx_;

        NSError* err   = nil;
        stream_        = [[SCStream alloc] initWithFilter:filter
                                            configuration:cfg
                                                 delegate:handler_];
        if (!stream_) return false;

        if (![stream_ addStreamOutput:handler_
                                 type:SCStreamOutputTypeScreen
                  sampleHandlerQueue:dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0)
                                error:&err]) {
            return false;
        }

        __block bool started = false;
        dispatch_semaphore_t sem = dispatch_semaphore_create(0);
        [stream_ startCaptureWithCompletionHandler:^(NSError* e) {
            started = (e == nil);
            dispatch_semaphore_signal(sem);
        }];
        dispatch_semaphore_wait(sem, dispatch_time(DISPATCH_TIME_NOW, NSEC_PER_SEC * 5));
        return started;
    }

    StreamContext       ctx_{};
    SCStream*           stream_  = nil;
    MimicStreamHandler* handler_ = nil;
};

std::unique_ptr<Capturer> make_macos_capturer() {
    return std::make_unique<MacOSCapturer>();
}

std::vector<DisplayInfo> list_displays() {
    std::vector<DisplayInfo> result;
    CGDirectDisplayID ids[32];
    uint32_t          count = 0;
    if (CGGetActiveDisplayList(32, ids, &count) != kCGErrorSuccess) {
        return result;
    }
    for (uint32_t i = 0; i < count; ++i) {
        DisplayInfo di;
        const CGRect b = CGDisplayBounds(ids[i]);
        di.index      = static_cast<int32_t>(i);
        di.name       = std::string("display-") + std::to_string(i);
        di.bounds.x   = static_cast<int32_t>(b.origin.x);
        di.bounds.y   = static_cast<int32_t>(b.origin.y);
        di.bounds.width  = static_cast<int32_t>(b.size.width);
        di.bounds.height = static_cast<int32_t>(b.size.height);
        di.is_primary    = (ids[i] == CGMainDisplayID());

        const size_t pixel_w = CGDisplayPixelsWide(ids[i]);
        di.dpi_scale = b.size.width > 0
            ? static_cast<float>(pixel_w) / static_cast<float>(b.size.width)
            : 1.0f;
        result.push_back(di);
    }
    return result;
}

}

#endif
