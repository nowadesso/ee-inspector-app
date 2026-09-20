"""EE Inspector Pro local Python 3 recipe.

Wraps the official p4a Python3Recipe and disables the lzma and readline
modules, which cannot be compiled against the Android NDK without extra
system libraries. Also patches grpmodule.c to remove calls to
setgrent/getgrent/endgrent that Android's bionic libc does not provide.
"""

from pathlib import Path

from pythonforandroid.recipes.python3 import Python3Recipe as _Base


class Python3Recipe(_Base):
    """Local override of the p4a python3 recipe."""

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)

        build_dir = Path(self.get_build_dir(arch.arch))

        # 1. Comment out lzma and readline entries in every Setup file
        #    so the generated Makefile never tries to build them.
        for name in ("Setup", "Setup.dist", "Setup.local"):
            setup_path = build_dir / "Modules" / name
            if not setup_path.is_file():
                continue
            lines = setup_path.read_text().splitlines()
            out = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("lzma ") or stripped.startswith("readline "):
                    out.append("# disabled by ee-inspector: " + line)
                else:
                    out.append(line)
            setup_path.write_text("\n".join(out) + "\n")
            print(f"EE Inspector Pro: sanitized Modules/{name}")

        # 2. Patch grpmodule.c to remove setgrent/getgrent/endgrent.
        grp_file = build_dir / "Modules" / "grpmodule.c"
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


# p4a requires this module-level name to be defined.
recipe = Python3Recipe()
