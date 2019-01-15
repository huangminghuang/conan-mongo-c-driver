import platform, os
from conans.client.run_environment import RunEnvironment

from conans import ConanFile, CMake, tools


class MongocdriverTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        
    def test(self):
        os.chdir('bin')
        re = RunEnvironment(self)
        with tools.environment_append(re.vars):
            if platform.system() == "Darwin":
                lpath = os.environ["DYLD_LIBRARY_PATH"]
                self.run('DYLD_LIBRARY_PATH=%s ./example' % (lpath))
            else:
                self.run(".%sexample" % os.sep)
