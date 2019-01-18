from conans import ConanFile, CMake, tools
import os

class MongocdriverConan(ConanFile):
    name = "mongo-c-driver"
    version = "1.13.0"
    description = "A high-performance MongoDB driver for C"
    topics = ("conan", "libmongoc", "mongodb")
    url = "http://github.com/huangminghuang/conan-mongo-c-driver"
    homepage = "https://github.com/mongodb/mongo-c-driver"
    author = "Huang-Ming Huang <huangh@objectcomputing.com>"
    license = "MIT"
    exports = ["LICENSE"]
    
    build_policy = "missing"
    
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "with_icu": [True, False]}
    default_options = "shared=False", "with_icu=False"
            
    requires = 'zlib/1.2.11@conan/stable'
    exports_sources = ["package.patch"]
    generators = "cmake_find_package"
    
    no_copy_source = True

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx

    def requirements(self):
        if not tools.os_info.is_macos and not tools.os_info.is_windows:
            self.requires.add("OpenSSL/1.1.1a@conan/stable")
        if self.options.with_icu:
            self.requires.add("icu/63.1@bincrafters/stable")

    def source(self):
        tools.get("https://github.com/mongodb/mongo-c-driver/releases/download/{0}/mongo-c-driver-{0}.tar.gz"
                          .format(self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, 'sources')
        tools.patch(base_path='sources', patch_file="package.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions["ENABLE_EXAMPLES"] = False
        cmake.definitions["ENABLE_AUTOMATIC_INIT_AND_CLEANUP"] = False
        cmake.definitions["ENABLE_BSON"] = "ON"
        cmake.definitions["ENABLE_SASL"] = "OFF"
        cmake.definitions["ENABLE_STATIC"] = "OFF" if self.options.shared else "ON"

        cmake.configure(source_dir=os.path.join(self.source_folder,"sources"))

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
        lib_suffix = "" if self.options.shared else "-static"

        libnames = ['mongoc', 'bson']
        self.cpp_info.libs = [ "{}{}-1.0".format(name, lib_suffix) for name in libnames ]
        self.cpp_info.includedirs.extend( ['include/libmongoc-1.0', 'include/libbson-1.0' ] )
        
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
