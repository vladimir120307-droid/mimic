#include "mimic/capture.h"

#include <memory>

namespace mimic {

#if defined(_WIN32)
std::unique_ptr<Capturer> make_windows_capturer();
#elif defined(__APPLE__)
std::unique_ptr<Capturer> make_macos_capturer();
#elif defined(__linux__)
std::unique_ptr<Capturer> make_linux_capturer();
#endif

std::unique_ptr<Capturer> make_capturer() {
#if defined(_WIN32)
    return make_windows_capturer();
#elif defined(__APPLE__)
    return make_macos_capturer();
#elif defined(__linux__)
    return make_linux_capturer();
#else
    return nullptr;
#endif
}

const char* platform_name() {
#if defined(_WIN32)
    return "windows";
#elif defined(__APPLE__)
    return "macos";
#elif defined(__linux__)
    return "linux";
#else
    return "unknown";
#endif
}

const char* version() {
    return "0.1.0";
}

}
