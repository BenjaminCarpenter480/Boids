cmake_minimum_required(VERSION 3.1)	

project(GLProj)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_BUILD_TYPE Debug)

add_executable(HelloGL main.cpp GLWrap.h testSim.h shader.shader)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/shader.shader
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR})


set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)

add_subdirectory(glfw-3.3.2)

include_directories(glfw-3.3.2/include)


#target_link_libraries(HelloGL glfw ${GLFW_LIBRARIES})


target_link_libraries(HelloGL PRIVATE ${GLFW_LIBRARIES})

#target_link_libraries(HelloGL glfw ${OPENGL_glu_LIBRARY} ${GLFW_LIBRARIES})


find_package(OpenGL REQUIRED)

target_link_libraries(HelloGL OpenGL::GL)

add_subdirectory( ${PROJECT_SOURCE_DIR}/glew-2.1.0/build/cmake )

target_include_directories(HelloGL PRIVATE
    ${PROJECT_SOURCE_DIR}/glew-2.1.0/include
)

target_link_libraries(HelloGL glew glfw )


set(ENV(MESA_GL_VERSION_OVERRIDE "3.3"))
