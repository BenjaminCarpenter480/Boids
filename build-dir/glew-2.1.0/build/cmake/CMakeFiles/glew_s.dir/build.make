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
include glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/depend.make

# Include the progress variables for this target.
include glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/progress.make

# Include the compile flags for this target's objects.
include glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/flags.make

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/flags.make
glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o: ../glew-2.1.0/src/glew.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/benjamin/Desktop/SpaceObject/GLProj/build-dir/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/glew_s.dir/__/__/src/glew.c.o   -c /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/glew.c

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/glew_s.dir/__/__/src/glew.c.i"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/glew.c > CMakeFiles/glew_s.dir/__/__/src/glew.c.i

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/glew_s.dir/__/__/src/glew.c.s"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/src/glew.c -o CMakeFiles/glew_s.dir/__/__/src/glew.c.s

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.requires:

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.requires

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.provides: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.requires
	$(MAKE) -f glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/build.make glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.provides.build
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.provides

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.provides.build: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o


# Object files for target glew_s
glew_s_OBJECTS = \
"CMakeFiles/glew_s.dir/__/__/src/glew.c.o"

# External object files for target glew_s
glew_s_EXTERNAL_OBJECTS =

lib/libGLEWd.a: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o
lib/libGLEWd.a: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/build.make
lib/libGLEWd.a: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/benjamin/Desktop/SpaceObject/GLProj/build-dir/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library ../../../lib/libGLEWd.a"
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && $(CMAKE_COMMAND) -P CMakeFiles/glew_s.dir/cmake_clean_target.cmake
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/glew_s.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/build: lib/libGLEWd.a

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/build

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/requires: glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/__/__/src/glew.c.o.requires

.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/requires

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/clean:
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake && $(CMAKE_COMMAND) -P CMakeFiles/glew_s.dir/cmake_clean.cmake
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/clean

glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/depend:
	cd /home/benjamin/Desktop/SpaceObject/GLProj/build-dir && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/benjamin/Desktop/SpaceObject/GLProj /home/benjamin/Desktop/SpaceObject/GLProj/glew-2.1.0/build/cmake /home/benjamin/Desktop/SpaceObject/GLProj/build-dir /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake /home/benjamin/Desktop/SpaceObject/GLProj/build-dir/glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : glew-2.1.0/build/cmake/CMakeFiles/glew_s.dir/depend

