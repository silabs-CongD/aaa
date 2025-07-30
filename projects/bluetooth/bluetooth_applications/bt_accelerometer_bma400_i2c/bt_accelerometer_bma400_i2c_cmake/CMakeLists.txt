# Define minimal required version of CMake.
cmake_minimum_required(VERSION "3.25")

# Project definition
project(
	bt_accelerometer_bma400_i2c
	VERSION 1.0
	LANGUAGES C CXX ASM
)

# Include the definition of the slc_bt_accelerometer_bma400_i2c target,
# which contains the content of the SLC project
include(bt_accelerometer_bma400_i2c.cmake)

add_executable(bt_accelerometer_bma400_i2c
    # Add additional sources here
)

target_include_directories(bt_accelerometer_bma400_i2c PUBLIC
    # Add additional include paths here
)

target_compile_definitions(bt_accelerometer_bma400_i2c PUBLIC
    # Add additional macros here
)

target_compile_options(bt_accelerometer_bma400_i2c PUBLIC
    # Set additional compiler flags here
)

target_link_options(bt_accelerometer_bma400_i2c PUBLIC
    # Set additional linker flags here
)

# Link with the content defined in the SLC project
target_link_libraries(bt_accelerometer_bma400_i2c PRIVATE
    slc_bt_accelerometer_bma400_i2c
)

# Include managed project content if available
include(bt_accelerometer_bma400_i2c_project.cmake OPTIONAL RESULT_VARIABLE managed_project)
if(managed_project)
    message(STATUS "Using managed project content from ${managed_project}")
endif()

# Force the gcc linker command
set_target_properties(bt_accelerometer_bma400_i2c PROPERTIES LINKER_LANGUAGE C)

# Create .bin, .hex and .s37 artifacts after building the project
add_custom_command(TARGET bt_accelerometer_bma400_i2c
    POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_SREC_CMD} "$<TARGET_FILE:bt_accelerometer_bma400_i2c>" "$<TARGET_FILE_DIR:bt_accelerometer_bma400_i2c>/$<TARGET_FILE_BASE_NAME:bt_accelerometer_bma400_i2c>.s37"
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_IHEX_CMD} "$<TARGET_FILE:bt_accelerometer_bma400_i2c>" "$<TARGET_FILE_DIR:bt_accelerometer_bma400_i2c>/$<TARGET_FILE_BASE_NAME:bt_accelerometer_bma400_i2c>.hex"
    COMMAND ${CMAKE_OBJCOPY} ${OBJCOPY_BIN_CMD}  "$<TARGET_FILE:bt_accelerometer_bma400_i2c>" "$<TARGET_FILE_DIR:bt_accelerometer_bma400_i2c>/$<TARGET_FILE_BASE_NAME:bt_accelerometer_bma400_i2c>.bin" 
)

# Run post-build pipeline to perform additional post-processing
if(post_build_command)
add_custom_command(TARGET bt_accelerometer_bma400_i2c
    POST_BUILD
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/..
    COMMAND ${post_build_command}
)
endif()