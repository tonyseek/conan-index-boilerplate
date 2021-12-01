import os

from conans import ConanFile, CMake, tools


class ConanRecipe(ConanFile):
    name = "demo"
    version = "20211201.1"
    homepage = "https://github.com/tonyseek/cpp-boilerplate"
    url = "https://github.com/tonyseek/cpp-boilerplate"
    exports_sources = ["CMakeLists.txt"]
    topics = ("demo",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    generators = "cmake"
    short_paths = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        args = self.conan_data["sources"][self.version]
        tools.get(**args, destination=self._source_subfolder, strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        include_dir = os.path.join(self._source_subfolder, '/include')
        self.copy("*.h", dst="include", src=include_dir)
        self.copy("*demo.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["demo"]
        self.cpp_info.names['cmake_find_package'] = ["Demo"]
        self.cpp_info.names['cmake_find_package_multi'] = ["Demo"]
