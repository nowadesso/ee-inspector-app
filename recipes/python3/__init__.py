from pythonforandroid.recipe import TargetPythonRecipe


class Python3Recipe(TargetPythonRecipe):
    version = "3.12.10"
    url = "https://www.python.org/ftp/python/{version}/Python-{version}.tgz"

    depends = [
        "hostpython3",
        "sqlite3",
        "openssl",
        "libffi",
    ]

    patches = ["patches/disable_grp.patch"]

    def include_root(self, arch_name):
        from os.path import join
        return join(
            self.get_build_dir(arch_name),
            "android-build",
            "android-root",
            "include",
            "python3.12",
        )

    def link_root(self, arch_name):
        from os.path import join
        return join(
            self.get_build_dir(arch_name),
            "android-build",
        )

    @property
    def link_version(self):
        return "3.12"

    def get_python_root(self, arch):
        from os.path import join
        return join(
            self.get_build_dir(arch.arch),
            "android-build",
            "android-root",
        )


recipe = Python3Recipe()
