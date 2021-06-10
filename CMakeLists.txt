cmake_minimum_required(VERSION 2.8)
project(rpi_camera_app)

find_package(pigpio REQUIRED)
include_directories(${pigpio_INCLUDE_DIRS})

add_executable(rpi_camera src/main.cpp)
target_link_libraries(rpi_camera ${pigpio_LIBS} )