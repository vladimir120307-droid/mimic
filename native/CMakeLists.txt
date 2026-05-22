cmake_minimum_required(VERSION 3.20)
project(mimic_capture
    VERSION 0.1.0
    LANGUAGES CXX
    DESCRIPTION "Native screen-capture core for mimic"
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release)
endif()

option(MIMIC_BUILD_TESTS    "Build unit tests"        ON)
option(MIMIC_BUILD_BINDINGS "Build Python bindings"   ON)
option(MIMIC_WARNINGS_AS_ERRORS "Treat warnings as errors" OFF)

# ---------- Compile options ----------
if(MSVC)
    add_compile_options(/W4 /permissive- /Zc:__cplusplus)
    if(MIMIC_WARNINGS_AS_ERRORS)
        add_compile_options(/WX)
    endif()
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Wshadow -Wconversion)
    if(MIMIC_WARNINGS_AS_ERRORS)
        add_compile_options(-Werror)
    endif()
endif()

# ---------- Platform sources ----------
set(MIMIC_PLATFORM_SOURCES)

if(WIN32)
    list(APPEND MIMIC_PLATFORM_SOURCES src/capture_windows.cpp)
    set(MIMIC_PLATFORM_LIBS dxgi d3d11 dxguid)
elseif(APPLE)
    list(APPEND MIMIC_PLATFORM_SOURCES src/capture_macos.mm)
    find_library(SCREEN_CAPTURE_KIT ScreenCaptureKit)
    find_library(CORE_GRAPHICS      CoreGraphics)
    find_library(CORE_MEDIA         CoreMedia)
    find_library(CORE_VIDEO         CoreVideo)
    find_library(FOUNDATION         Foundation)
    set(MIMIC_PLATFORM_LIBS
        ${SCREEN_CAPTURE_KIT} ${CORE_GRAPHICS} ${CORE_MEDIA}
        ${CORE_VIDEO} ${FOUNDATION}
    )
elseif(UNIX)
    list(APPEND MIMIC_PLATFORM_SOURCES src/capture_linux.cpp)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(PIPEWIRE REQUIRED libpipewire-0.3)
    set(MIMIC_PLATFORM_LIBS ${PIPEWIRE_LIBRARIES})
endif()

# ---------- Core library ----------
add_library(mimic_capture
    src/capture_common.cpp
    src/dedup.cpp
    src/hash.cpp
    ${MIMIC_PLATFORM_SOURCES}
)

target_include_directories(mimic_capture
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(mimic_capture PRIVATE ${MIMIC_PLATFORM_LIBS})

if(APPLE)
    target_compile_options(mimic_capture PRIVATE -fobjc-arc)
endif()

# ---------- Python bindings ----------
if(MIMIC_BUILD_BINDINGS)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
    find_package(pybind11 CONFIG REQUIRED)

    pybind11_add_module(_mimic_capture bindings/python_bindings.cpp)
    target_link_libraries(_mimic_capture PRIVATE mimic_capture)
    set_target_properties(_mimic_capture PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python"
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/python"
    )
endif()

# ---------- Tests ----------
if(MIMIC_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# ---------- Install ----------
include(GNUInstallDirs)
install(TARGETS mimic_capture
    LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
