import os
from conans import ConanFile, tools, CMake


class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.8"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://eigen.tuxfamily.org"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors, \
                   numerical solvers, and related algorithms."
    license = "MPL-2.0"
    topics = ("eigen", "algebra", "linear-algebra", "vector", "numerical")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = ["patches/*"]
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        source_url = "https://gitlab.com/libeigen/eigen"
        sha256 = "146a480b8ed1fb6ac7cd33fec9eb5e8f8f62c3683b3f850094d9d5c35a92419a"
        tools.get("{0}/-/archive/{1}/eigen-{1}.tar.gz".format(source_url, self.version), sha256=sha256)
        os.rename("eigen-{}".format(self.version), self._source_subfolder)
        git = tools.Git(folder="eigen-patch")
        git.clone("https://gist.github.com/be9c216d200977d70140f7070d5fd2fa.git")
        self.run(
            "cd " + self._source_subfolder + " && git apply " + "../eigen-patch/Eigen_{}.patch".format(self.version))

    def package(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["EIGEN_TEST_NOQT"] = True
        cmake.configure(source_folder=self._source_subfolder)
        cmake.install()

        self.copy("COPYING.*", dst="licenses", src=self._source_subfolder)
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Eigen3"
        self.cpp_info.names["cmake_find_package_multi"] = "Eigen3"
        self.cpp_info.names["pkg_config"] = "eigen3"
        self.cpp_info.components["eigen3"].names["cmake_find_package"] = "Eigen"
        self.cpp_info.components["eigen3"].names["cmake_find_package_multi"] = "Eigen"
        self.cpp_info.components["eigen3"].includedirs = [os.path.join("include", "eigen3")]
        if self.settings.os == "Linux":
            self.cpp_info.components["eigen3"].system_libs = ["m"]
