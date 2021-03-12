from conans import ConanFile, AutoToolsBuildEnvironment, tools


class LazylpsolverlibsConan(ConanFile):
    name = "lazylpsolverlibs"
    version = "1.1.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Lazylpsolverlibs here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    keep_imports = True
    exports_sources = (
        "configure.ac",
        "Makefile.am",
        "lazylpsolverlibs*",
        "autogen.sh",
        "helpers*",
        "lib*",
        "share*",
        "README",
        "AUTHORS",
        "INSTALL",
        "ChangeLog",
        "NEWS",
    )

    def build(self):
        if tools.os_info.is_linux:
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                args = ["--with-pic", "--enable-static", "--disable-shared"]

                if self.settings.build_type == "Debug":
                    args.append("--enable-debug")

                with tools.chdir(self.source_folder):
                    self.run("autoreconf -i")
                    self.run(f"./configure {' '.join(args)}")
                    self.run("make all")

    def package(self):
        self.copy("xprs.h", dst="include", src="lazylpsolverlibs")
        if tools.os_info.is_linux:
            self.copy("lazylpsolverlibs.h", dst="include", src="lazylpsolverlibs")
            self.copy("lib/.libs/liblazyxprs.a", dst="lib", keep_path=False)

    def package_info(self):
        if tools.os_info.is_linux:
            self.cpp_info.libs = ["liblazyxprs.a"]