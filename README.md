## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/huangminghuang/conan/mongo-c-driver%3Ahuangminghuang/images/download.svg) ](https://bintray.com/huangminghuang/conan/mongo-c-driver%3Ahuangminghuang/_latestVersion)|[![Build status](https://ci.appveyor.com/api/projects/status/github/huangminghuang/conan-mongo-c-driver?svg=true)](https://ci.appveyor.com/project/huangminghuang/conan-mongo-c-driver)|[![Build Status](https://travis-ci.com/huangminghuang/conan-mongo-c-driver.svg?branch=master)](https://travis-ci.com/huangminghuang/conan-mongo-c-driver)|


## Basic setup

    $ conan remote add huang https://api.bintray.com/conan/huangminghuang/conan 
    $ conan install mongo-c-driver/1.13.0@huangminghuang/stable
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    mongo-c-driver/1.13.0@huangminghuang/stable

    [options]
    mongo-c-driver:shared=False
    
    [generators]
    cmake
    cmake_paths


Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.cmake* from the *cmake* generator and *conan_paths.cmake* from *cmake_paths* generator with all the paths and variables that you need to link with your dependencies.

## CMake setup

### using cmake_paths generator
Unlike the the [Bincrafter recipe for mongo-c-driver](https://bintray.com/bincrafters/public-conan/mongo-c-driver%3Abincrafters/1.11.0%3Astable), this recipe exports the original libmonogoc-static-1.0-config.cmake/libbson-static-1.0-config.cmake installed by mongo-c-driver so you can use the *cmake_paths* generator without modifying your existing *CMakefiles.txt*.

*CMakeLists.txt*

    find_package(libmongoc-static-1.0 REQUIRED)
    add_executable(example example.cpp)
    target_include_directories(example PRIVATE ${MONGO_STATIC_INCLUDE_DIRS})
    target_link_libraries(example ${MONGOC_STATIC_LIBRARIES})
    target_compile_definitions(example PRIVATE ${MONGOC_STATIC_DEFINITIONS})
 

The *conan_paths.cmake* can be specified as a toolchain file when invoking cmake:

```bash
$ mkdir build && cd build
$ conan install ..
$ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -DCMAKE_BUILD_TYPE=Release
$ cmake --build .
```

### using cmake generator

*CMakeLists.txt*

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(TARGETS)

    add_executable(example example.cpp)
    target_link_libraries(example CONAN_PKG::mongo-c-driver)
 
  
```bash
$ mkdir build && cd build
$ conan install ..
$ cmake .. -DCMAKE_BUILD_TYPE=Release
$ cmake --build .
```

