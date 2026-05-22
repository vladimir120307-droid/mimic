#if defined(_WIN32)

#include "mimic/capture.h"

#include <gtest/gtest.h>

using namespace mimic;

TEST(DxgiGrab, GrabOneReturnsFrameOnWindowsWithDisplay) {
    auto cap = make_capturer();
    ASSERT_NE(cap, nullptr);

    CaptureConfig cfg;
    cfg.target_fps     = 30;
    cfg.include_cursor = false;
    cfg.enable_dedup   = false;

    auto frame = cap->grab_one(cfg);

    if (!frame.has_value()) {
        GTEST_SKIP() << "No display available (headless / Session 0 / driver issue)";
    }

    EXPECT_GT(frame->width,  0);
    EXPECT_GT(frame->height, 0);
    EXPECT_GE(frame->stride, frame->width * 4);
    EXPECT_FALSE(frame->data.empty());
    EXPECT_EQ(frame->format, PixelFormat::BGRA8);
    EXPECT_EQ(frame->data.size(),
              static_cast<size_t>(frame->stride) * frame->height);
}

#endif
