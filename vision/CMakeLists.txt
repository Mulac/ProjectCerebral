cmake_minimum_required(VERSION 3.15)
project(vision)

set(CMAKE_CXX_STANDARD 14)

find_package( OpenCV REQUIRED)

add_executable(vision main.cpp)
target_link_libraries( vision ${OpenCV_LIBS} )