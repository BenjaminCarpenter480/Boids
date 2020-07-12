#shader vertex
#version 330 core 

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif
#include <chrono>
#include <thread>
layout(location=0) in vec4 position;

void main() {
    std::this_thread::sleep_for(30s);
    gl_Position = position;
};


#shader fragment
#version 330  core
layout(location = 0) out vec4 color;

void main() {
    color = vec4(1.0,0.0,0.0,1.0);
}
