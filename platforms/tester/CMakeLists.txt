add_executable(NoobBoyTester main.cpp)
target_link_libraries(NoobBoyTester PRIVATE NoobBoyCore)

if(NOT ${CMAKE_SYSTEM_NAME} MATCHES "Emscripten")
    target_link_libraries(NoobBoyTester PRIVATE SDL3::SDL3 SDL3_ttf::SDL3_ttf)
endif()

set_target_properties(NoobBoyTester PROPERTIES 
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}"
)
