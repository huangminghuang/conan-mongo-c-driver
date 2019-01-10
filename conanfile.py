from conans import ConanFile, CMake, tools
import os

class MongocdriverConan(ConanFile):
    name = "mongo-c-driver"
    version = "1.10.0"
    description = "A high-performance MongoDB driver for C"
    topics = ("conan", "libmongoc", "mongodb")
    url = "http://github.com/bincrafters/conan-mongo-c-driver"
    homepage = "https://github.com/mongodb/mongo-c-driver"
    author = "Huang-Ming Huang <huangh@objectcomputing.com>"
    license = "MIT"
    exports = ["LICENSE"]
    
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
        
    requires = 'zlib/1.2.11@conan/stable'
    generators = "cmake"

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx

    def requirements(self):
        if not tools.os_info.is_macos and not tools.os_info.is_windows:
            self.requires.add("OpenSSL/1.0.2o@conan/stable")

    def source(self):
        tools.get("https://github.com/mongodb/mongo-c-driver/releases/download/{0}/mongo-c-driver-{0}.tar.gz"
                          .format(self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, 'sources')
        tools.replace_in_file("sources/CMakeLists.txt", "project (mongo-c-driver C)",
                                      '''project (mongo-c-driver C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions["ENABLE_EXAMPLES"] = False
        cmake.definitions["ENABLE_AUTOMATIC_INIT_AND_CLEANUP"] = False
        cmake.definitions["ENABLE_BSON"] = "ON"
        cmake.definitions["ENABLE_SASL"] = "OFF"
        cmake.definitions["ENABLE_STATIC"] = "OFF" if self.options.shared else "ON"

        cmake.configure(source_dir="sources")

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING*", dst="licenses", src="sources")

        # cmake installs all the files
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        lib_suffix = "" if self.options["shared"] else "-static"

        libnames = ['mongoc', 'bson']
        self.cpp_info.libs = [ "{}{}-1.0".format(name, lib_suffix) for name in libnames ]
        self.cpp_info.includedirs.extend( ['include/lib{}'.format(name) for name in self.cpp_info.libs ] )
        self.cpp_info.builddirs = [ "lib/cmake/lib{}".format(name) for name in self.cpp_info.libs ]
        
        if tools.os_info.is_macos:
            self.cpp_info.exelinkflags = ['-framework CoreFoundation', '-framework Security']
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

        if tools.os_info.is_linux:
            self.cpp_info.libs.extend(["rt", "pthread"])

        if not self.options.shared:
            self.cpp_info.defines.extend(['BSON_STATIC', 'MONGOC_STATIC'])

            if tools.os_info.is_linux or tools.os_info.is_macos:
                self.cpp_info.libs.append('resolv')

            if tools.os_info.is_windows:
                self.cpp_info.libs.extend(['ws2_32.lib', 'secur32.lib', 'crypt32.lib', 'BCrypt.lib', 'Dnsapi.lib'])
