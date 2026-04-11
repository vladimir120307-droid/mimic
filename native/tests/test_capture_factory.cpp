#include "mimic/capture.h"

#include <gtest/gtest.h>

#include <string>

using namespace mimic;

TEST(Capture, FactoryReturnsCapturer) {
    auto cap = make_capturer();
    ASSERT_NE(cap, nullptr);
    EXPECT_FALSE(cap->is_running());
}

TEST(Capture, PlatformNameMatchesBuildHost) {
    std::string name = platform_name();
#if defined(_WIN32)
    EXPECT_EQ(name, "windows");
#elif defined(__APPLE__)
    EXPECT_EQ(name, "macos");
#elif defined(__linux__)
    EXPECT_EQ(name, "linux");
#else
    EXPECT_EQ(name, "unknown");
#endif
}

TEST(Capture, ListDisplaysReturnsAtLeastOne) {
    auto displays = list_displays();
    EXPECT_FALSE(displays.empty());
}

TEST(Capture, VersionStringIsNonEmpty) {
    std::string v = version();
    EXPECT_FALSE(v.empty());
}
