from pythonforandroid.recipe import Recipe


class Python3Recipe(Recipe):
    version = "3.12.10"
    url = "https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
    depends = ["hostpython3", "sqlite3", "openssl", "libffi"]
    patches = ["patches/disable_grp.patch"]


recipe = Python3Recipe()
