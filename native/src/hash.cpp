#include "mimic/dedup.h"

#include <algorithm>
#include <bit>
#include <cstdint>
#include <vector>

namespace mimic {

namespace {

void rgba_to_gray_resized(const Frame&          frame,
                          int                   target_w,
                          int                   target_h,
                          std::vector<uint8_t>& out) {
    out.assign(static_cast<size_t>(target_w) * target_h, 0);
    if (frame.width <= 0 || frame.height <= 0) return;

    const auto sx = static_cast<float>(frame.width)  / target_w;
    const auto sy = static_cast<float>(frame.height) / target_h;
    const int bpp = 4;

    for (int y = 0; y < target_h; ++y) {
        const int src_y = std::min(frame.height - 1,
                                   static_cast<int>(y * sy));
        const uint8_t* row =
            frame.data.data() + static_cast<size_t>(src_y) * frame.stride;
        for (int x = 0; x < target_w; ++x) {
            const int src_x = std::min(frame.width - 1,
                                       static_cast<int>(x * sx));
            const uint8_t* px = row + src_x * bpp;
            uint8_t b = px[0], g = px[1], r = px[2];
            if (frame.format == PixelFormat::RGBA8) std::swap(b, r);
            out[static_cast<size_t>(y) * target_w + x] =
                static_cast<uint8_t>((r * 299 + g * 587 + b * 114) / 1000);
        }
    }
}

}

uint64_t dhash(const Frame& frame, int hash_size) {
    if (hash_size <= 0 || hash_size > 8) hash_size = 8;
    const int w = hash_size + 1;
    const int h = hash_size;

    std::vector<uint8_t> small;
    rgba_to_gray_resized(frame, w, h, small);

    uint64_t out = 0;
    int bit = 0;
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < hash_size; ++x) {
            const uint8_t left  = small[static_cast<size_t>(y) * w + x];
            const uint8_t right = small[static_cast<size_t>(y) * w + x + 1];
            if (left > right) out |= (uint64_t{1} << bit);
            ++bit;
        }
    }
    return out;
}

int hamming_distance(uint64_t a, uint64_t b) {
    return std::popcount(a ^ b);
}

}
