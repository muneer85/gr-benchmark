find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_BENCHMARK_TEST gnuradio-Benchmark_Test)

FIND_PATH(
    GR_BENCHMARK_TEST_INCLUDE_DIRS
    NAMES gnuradio/Benchmark_Test/api.h
    HINTS $ENV{BENCHMARK_TEST_DIR}/include
        ${PC_BENCHMARK_TEST_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_BENCHMARK_TEST_LIBRARIES
    NAMES gnuradio-Benchmark_Test
    HINTS $ENV{BENCHMARK_TEST_DIR}/lib
        ${PC_BENCHMARK_TEST_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-Benchmark_TestTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_BENCHMARK_TEST DEFAULT_MSG GR_BENCHMARK_TEST_LIBRARIES GR_BENCHMARK_TEST_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_BENCHMARK_TEST_LIBRARIES GR_BENCHMARK_TEST_INCLUDE_DIRS)
