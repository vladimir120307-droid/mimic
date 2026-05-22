include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(mimic_tests
    test_dedup.cpp
    test_capture_factory.cpp
)
target_link_libraries(mimic_tests PRIVATE mimic_capture gtest_main)

include(GoogleTest)
gtest_discover_tests(mimic_tests)
