"""EE Inspector Pro local Python 3 recipe."""

from pathlib import Path

from pythonforandroid.recipes.python3 import Python3Recipe as _Base


class Python3Recipe(_Base):

    patches = []

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = Path(self.get_build_dir(arch.arch))
        modules_dir = build_dir / "Modules"

        # Append a *disabled* section to Setup.dist. CPython's configure
        # reads Setup.dist to generate the Makefile, so adding to it here
        # (in prebuild_arch, before configure runs) makes our disables
        # take effect.
        if modules_dir.is_dir():
            setup_dist = modules_dir / "Setup.dist"
            if setup_dist.is_file():
                text = setup_dist.read_text()
                if "_uuid _uuidmodule.c" not in text:
                    text += (
                        "\n*disabled*\n"
                        "_uuid _uuidmodule.c\n"
                        "readline readline.c\n"
                        "lzma _lzmamodule.c\n"
                    )
                    setup_dist.write_text(text)
                    print("EE Inspector Pro: appended *disabled* to Setup.dist")

        # Patch grpmodule.c
        grp_file = modules_dir / "grpmodule.c"
        if grp_file.is_file():
            src = grp_file.read_text()
            marker = "grp_getgrall_impl(PyObject *module)"
            idx = src.find(marker)
            if idx >= 0:
                brace = src.find("{", idx)
                if brace >= 0:
                    depth = 0
                    end = -1
                    for i in range(brace, len(src)):
                        c = src[i]
                        if c == "{":
                            depth += 1
                        elif c == "}":
                            depth -= 1
                            if depth == 0:
                                end = i + 1
                                break
                    if end > 0:
                        replacement = (
                            "grp_getgrall_impl(PyObject *module)\n"
                            "{\n"
                            "    PyObject *d = PyDict_New();\n"
                            "    if (d == NULL)\n"
                            "        return NULL;\n"
                            "    return d;\n"
                            "}"
                        )
                        src = src[:idx] + replacement + src[end:]
                        grp_file.write_text(src)
                        print("EE Inspector Pro: patched grpmodule.c")


recipe = Python3Recipe()
