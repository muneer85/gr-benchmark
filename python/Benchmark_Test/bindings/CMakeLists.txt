# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT Benchmark_Test_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT Benchmark_Test_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND Benchmark_Test_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(Benchmark_Test
   ../../..
   gr::Benchmark_Test
   "${Benchmark_Test_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET Benchmark_Test_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:Benchmark_Test_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/Benchmark_Test/
)

install(TARGETS Benchmark_Test_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/Benchmark_Test COMPONENT pythonapi)
