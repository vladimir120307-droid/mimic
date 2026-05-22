#pragma once

#if defined(_WIN32)

#include <stdexcept>
#include <string>
#include <system_error>

#include <windows.h>
#include <wrl/client.h>

namespace mimic::win {

template <typename T>
using ComPtr = Microsoft::WRL::ComPtr<T>;

inline std::string hresult_message(HRESULT hr) {
    return std::system_category().message(static_cast<int>(hr));
}

struct HResultError : std::runtime_error {
    HResultError(HRESULT hr_, const char* what_)
        : std::runtime_error(std::string{what_} + " (HRESULT 0x" +
                             std::to_string(static_cast<unsigned long>(hr_)) + ": " +
                             hresult_message(hr_) + ")"),
          hr{hr_} {}
    HRESULT hr;
};

#define MIMIC_THROW_IF_FAILED(expr)                                              \
    do {                                                                         \
        const HRESULT _mimic_hr = (expr);                                        \
        if (FAILED(_mimic_hr)) {                                                 \
            throw ::mimic::win::HResultError(_mimic_hr, #expr);                  \
        }                                                                        \
    } while (0)

}

#endif
