#include "mimic/dedup.h"

#include <gtest/gtest.h>

#include <vector>

using namespace mimic;

namespace {

Frame make_solid_frame(int w, int h, uint8_t r, uint8_t g, uint8_t b) {
    Frame f;
    f.width  = w;
    f.height = h;
    f.stride = w * 4;
    f.format = PixelFormat::RGBA8;
    f.data.resize(static_cast<size_t>(w) * h * 4);
    for (size_t i = 0; i < f.data.size(); i += 4) {
        f.data[i + 0] = r;
        f.data[i + 1] = g;
        f.data[i + 2] = b;
        f.data[i + 3] = 255;
    }
    return f;
}

}

TEST(Dedup, IdenticalFramesProduceEqualHashes) {
    auto a = make_solid_frame(64, 64, 100, 150, 200);
    auto b = make_solid_frame(64, 64, 100, 150, 200);
    EXPECT_EQ(dhash(a), dhash(b));
}

TEST(Dedup, DifferentColorsProduceComparableHashes) {
    auto a = make_solid_frame(64, 64, 10,  10,  10);
    auto b = make_solid_frame(64, 64, 240, 240, 240);
    EXPECT_LE(hamming_distance(dhash(a), dhash(b)), 64);
}

TEST(Deduplicator, FirstFrameAlwaysAccepted) {
    Deduplicator d(0.05f);
    auto         f = make_solid_frame(32, 32, 0, 0, 0);
    EXPECT_TRUE(d.accept(f));
}

TEST(Deduplicator, IdenticalSecondFrameRejected) {
    Deduplicator d(0.05f);
    auto         f = make_solid_frame(32, 32, 0, 0, 0);
    d.accept(f);
    EXPECT_FALSE(d.accept(f));
}

TEST(Deduplicator, ResetForgetsHistory) {
    Deduplicator d(0.05f);
    auto         f = make_solid_frame(32, 32, 0, 0, 0);
    d.accept(f);
    d.reset();
    EXPECT_TRUE(d.accept(f));
}
