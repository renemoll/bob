include(FetchContent)

FetchContent_Declare(
  bob-cmake
  GIT_REPOSITORY https://github.com/renemoll/bob-cmake.git
  GIT_TAG        origin/main
  GIT_SHALLOW    true
)

FetchContent_MakeAvailable(bob-cmake)
