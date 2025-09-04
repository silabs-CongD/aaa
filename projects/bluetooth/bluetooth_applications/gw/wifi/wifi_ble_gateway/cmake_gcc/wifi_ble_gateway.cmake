set(SDK_PATH "C:/Users/codo/.silabs/slt/installs/conan/p/simpl34b44a756bd4a/p")
set(COPIED_SDK_PATH "simplicity_sdk_2025.6.0")
set(PKG_PATH "C:/Users/codo/.silabs/slt/installs")

add_library(slc OBJECT
    "${SDK_PATH}/platform/common/src/sl_assert.c"
    "${SDK_PATH}/platform/common/src/sl_cmsis_os2_common.c"
    "${SDK_PATH}/platform/service/sl_main/src/rtos/main_retarget.c"
    "${SDK_PATH}/platform/service/sl_main/src/sl_main_init.c"
    "${SDK_PATH}/platform/service/sl_main/src/sl_main_init_memory.c"
    "${SDK_PATH}/platform/service/sl_main/src/sl_main_kernel.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/croutine.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/event_groups.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/list.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/portable/MemMang/heap_4.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/queue.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/stream_buffer.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/tasks.c"
    "${SDK_PATH}/util/third_party/freertos/kernel/timers.c"
    "../app.c"
    "../autogen/sl_event_handler.c"
    "../ble_app.c"
    "../main.c"
    "../wifi_app.c"
)

target_include_directories(slc PUBLIC
   "../config"
   "../autogen"
   "../."
    "${SDK_PATH}/platform/common/inc"
    "${SDK_PATH}/platform/CMSIS/Core/Include"
    "${SDK_PATH}/platform/CMSIS/RTOS2/Include"
    "${SDK_PATH}/util/third_party/freertos/kernel/include"
    "${SDK_PATH}/platform/service/sl_main/inc"
    "${SDK_PATH}/platform/service/sl_main/src"
)

target_compile_definitions(slc PUBLIC
    "SL_SI91X_PRINT_DBG_LOG=1"
    "SL_BOARD_NAME=\"BRD4002A\""
    "SL_BOARD_REV=\"A07\""
    "SL_COMPONENT_CATALOG_PRESENT=1"
    "SL_CODE_COMPONENT_FREERTOS_KERNEL=freertos_kernel"
)

target_link_libraries(slc PUBLIC
    "-Wl,--start-group"
    "gcc"
    "c"
    "m"
    "nosys"
    "-Wl,--end-group"
)
target_compile_options(slc PUBLIC
    $<$<COMPILE_LANGUAGE:C>:-Wall>
    $<$<COMPILE_LANGUAGE:C>:-Wextra>
    $<$<COMPILE_LANGUAGE:C>:-Os>
    $<$<COMPILE_LANGUAGE:C>:-g>
    "$<$<COMPILE_LANGUAGE:C>:SHELL:-Wall -Werror>"
    $<$<COMPILE_LANGUAGE:C>:-fno-lto>
    $<$<COMPILE_LANGUAGE:CXX>:-Wall>
    $<$<COMPILE_LANGUAGE:CXX>:-Wextra>
    $<$<COMPILE_LANGUAGE:CXX>:-Os>
    $<$<COMPILE_LANGUAGE:CXX>:-g>
    "$<$<COMPILE_LANGUAGE:CXX>:SHELL:-Wall -Werror>"
    $<$<COMPILE_LANGUAGE:CXX>:-fno-lto>
)

set(post_build_command ${POST_BUILD_EXE} postbuild "./wifi_ble_gateway.slpb" --parameter build_dir:"$<TARGET_FILE_DIR:wifi_ble_gateway>")
set_property(TARGET slc PROPERTY C_STANDARD 17)
set_property(TARGET slc PROPERTY CXX_STANDARD 17)
set_property(TARGET slc PROPERTY CXX_EXTENSIONS OFF)

target_link_options(slc INTERFACE
    "SHELL:-Xlinker -Map=$<TARGET_FILE_DIR:wifi_ble_gateway>/wifi_ble_gateway.map"
    -Wl,--wrap=main
    -fno-lto
)

# BEGIN_SIMPLICITY_STUDIO_METADATA=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END_SIMPLICITY_STUDIO_METADATA