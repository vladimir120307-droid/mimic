#pragma once

#include "mimic/capture.h"

#include <cstdint>
#include <optional>

namespace mimic {

uint64_t dhash(const Frame& frame, int hash_size = 8);

int hamming_distance(uint64_t a, uint64_t b);

class Deduplicator {
public:
    explicit Deduplicator(float threshold = 0.02f);

    bool accept(const Frame& frame);

    void reset();

private:
    std::optional<uint64_t> last_hash_;
    float                   threshold_;
};

}
