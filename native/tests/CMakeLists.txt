include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

set(MIMIC_TEST_SOURCES
    test_dedup.cpp
    test_capture_factory.cpp
)
if(WIN32)
    list(APPEND MIMIC_TEST_SOURCES test_dxgi_grab.cpp)
endif()

add_executable(mimic_tests ${MIMIC_TEST_SOURCES})
target_link_libraries(mimic_tests PRIVATE mimic_capture gtest_main)

include(GoogleTest)
gtest_discover_tests(mimic_tests)
