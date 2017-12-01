cmake_minimum_required(VERSION 3.8)
project(OptTsp)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

set(SOURCE_FILES main.cpp OptTsp.cpp OptTsp.h)
add_executable(OptTsp ${SOURCE_FILES})
target_link_libraries(OptTsp -lpthread)