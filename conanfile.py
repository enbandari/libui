from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool
import os


class libuiConan(ConanFile):
    name = "libui"
    version = "0.4.1.2"
    description = "Simple and portable GUI library in C that uses the native GUI technologies of each platform it supports."
    topics = ("conan", "libui", "ui", "gui")
    url = "https://github.com/enbandari/conan-libui"
    homepage = "https://github.com/enbandari/libui"
    license = "MIT"
    exports_sources = "*"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = ""


    def system_requirements(self):
        if tools.os_info.with_apt:
            packages = [
                "libgtk-3-dev",
                "libatk1.0-dev",
                "libglib2.0-dev",
                "libpango1.0-dev",
                "libgdk-pixbuf2.0-dev",
                "libcairo2-dev",
                "libpango1.0-dev",
                "libcairo2-dev"
            ]
            if tools.cross_building(self.settings):
                target_arch = {"x86": "i386", "armv7": "arm", "armv7hf": "armhf"}
                conan_arch = str(self.settings.arch)
                packages = ["%s:%s" % (package, target_arch[conan_arch]) for package in packages]
            installer = SystemPackageTool()
            installer.install(" ".join(packages))


    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()


    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if (self.settings.os == "Windows"):
            self.cpp_info.libs.extend([
                "user32",
                "kernel32",
                "gdi32",
                "comctl32",
                "msimg32",
                "comdlg32",
                "d2d1",
                "dwrite",
                "ole32",
                "oleaut32",
                "oleacc",
                "uuid",
                "windowscodecs",
            ])
        elif (self.settings.os == "Linux"):
            self.cpp_info.libs.extend([
                "gtk-3",
                "gdk-3",
                "atk-1.0",
                "gio-2.0",
                "pangocairo-1.0",
                "gdk_pixbuf-2.0",
                "cairo-gobject",
                "pango-1.0",
                "cairo",
                "gobject-2.0",
                "glib-2.0",
            ])
