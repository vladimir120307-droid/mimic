#include "mimic/dedup.h"

#include <algorithm>

namespace mimic {

Deduplicator::Deduplicator(float threshold)
    : threshold_(std::clamp(threshold, 0.0f, 1.0f)) {}

bool Deduplicator::accept(const Frame& frame) {
    const uint64_t h = dhash(frame);
    if (!last_hash_) {
        last_hash_ = h;
        return true;
    }
    const int  dist     = hamming_distance(*last_hash_, h);
    const auto max_bits = 64.0f;
    const auto fraction = static_cast<float>(dist) / max_bits;
    if (fraction >= threshold_) {
        last_hash_ = h;
        return true;
    }
    return false;
}

void Deduplicator::reset() {
    last_hash_.reset();
}

}
