# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/benjamin/Desktop/SpaceObject/GLProj

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/benjamin/Desktop/SpaceObject/GLProj/build-dir

# Include any dependencies generated for this target.
include glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/depend.make

# Include the progress variables for this target.
include glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/progress.make

# Include the compile flags for this target's objects.
include glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/flags.make

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/flags.make
glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o: ../glew-2.1.0/src/visualinfo.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/benjamin/Desktop/SpaceObject/GLProj/build-dir/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o   -c /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/visualinfo.c

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.i"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/visualinfo.c > CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.i

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.s"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/visualinfo.c -o CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.s

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.requires:

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.requires

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.provides: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.requires
	$(MAKE) -f glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/build.make glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.provides.build
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.provides

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.provides.build: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o


# Object files for target visualinfo
visualinfo_OBJECTS = \
"CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o"

# External object files for target visualinfo
visualinfo_EXTERNAL_OBJECTS =

bin/visualinfo: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o
bin/visualinfo: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/build.make
bin/visualinfo: lib/libGLEWd.so.2.1.0
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libSM.so
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libICE.so
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libX11.so
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libXext.so
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libGL.so
bin/visualinfo: /usr/lib/x86_64-linux-gnu/libGLU.so
bin/visualinfo: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/benjamin/Desktop/SpaceObject/GLProj/build-dir/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ../../../bin/visualinfo"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/visualinfo.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/build: bin/visualinfo

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/build

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/requires: glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/__/__/src/visualinfo.c.o.requires

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/requires

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/clean:
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && $(CMAKE_COMMAND) -P CMakeFiles/visualinfo.dir/cmake_clean.cmake
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/clean

glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/depend:
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/benjamin/Desktop/SpaceObject/GLProj /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/build/cmake /home/benjamin/Desktop/SpaceObject/GLProj/build-dir /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/visualinfo.dir/depend

