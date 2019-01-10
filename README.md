## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/huangminghuang/conan/mongo-c-driver%3Ahuangminghuang/images/download.svg) ](https://bintray.com/huangminghaung/conan/mongo-c-driver%3Ahuangminghuang/_latestVersion)|[![Build status](https://ci.appveyor.com/api/projects/status/github/huangminghuang/conan-mongo-c-driver?svg=true)](https://ci.appveyor.com/project/huangminghuang/conan-mongo-c-driver)|[![Build Status](https://travis-ci.org/huangminghuang/conan-mongo-c-driver.svg)](https://travis-ci.org/huangminghuang/conan-mongo-c-driver)|


## Usage Information

Unlike the the [Bincrafter recipe for mongo-c-driver](https://bintray.com/bincrafters/public-conan/mongo-c-driver%3Abincrafters/1.11.0%3Astable), this recipe exposes the original libmonogoc-1.0-config.cmake/libbson-1.0-config.cmake installed by mongo-c-driver to useers. The correct usage of the receipe in the CMakeLists.txt should be similar to the following: 

```cmake
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(libmongoc-static-1.0 REQUIRED)
add_executable(example example.cpp)
target_include_directories(example PRIVATE ${MONGO_STATIC_INCLUDE_DIRS})
target_link_libraries(example ${MONGOC_STATIC_LIBRARIES})
target_compile_definitions(example PRIVATE ${MONGOC_STATIC_DEFINITIONS})
 
```
## Conan.io Information

Huangminghuang packages can be found in the following public Conan repository:

[Huangminghuang Public Conan Repository on Bintray](https://bintray.com/huangminghuang/conan)

*Note: You can click the "Set Me Up" button on the Bintray page above for instructions on using packages from this repository.*

## License Information

This package is hosted on [Bintray](https://bintray.com) and contain Open-Source software which is licensed by the software's maintainers.  For each Open-Source package published, the packaging process obtains the required license files along with the original source files from the maintainer, and includes these license files in the generated Conan packages.

The contents of this GIT repository are completely separate from the software being packaged and therefore licensed separately.  The license for all files contained in this GIT repository are defined in the [LICENSE](LICENSE) file in this repository.  The licenses included with this package can be found in the Conan package directories in the following locations, relative to the Conan Cache root (`~/.conan` by default):

### License(s) for packaged software:

    ~/.conan/data/<pkg_name>/<pkg_version>/huangminghuang/package/<random_package_id>/license/<LICENSE_FILES_HERE>

*Note :   The most common filenames for OSS licenses are `LICENSE` AND `COPYING` without file extensions.*

### License for huangminghuang recipe:

    ~/.conan/data/<pkg_name>/<pkg_version>/huangminghuang/export/LICENSE