"""EE Inspector Pro local Python 3 recipe."""

from pathlib import Path

from pythonforandroid.recipes.python3 import Python3Recipe as _Base


class Python3Recipe(_Base):
    """Local override: disable readline, patch grpmodule.c."""

    patches = []

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = Path(self.get_build_dir(arch.arch))

        # Disable readline only (lzma is handled by the liblzma recipe).
        for name in ("Setup", "Setup.dist", "Setup.local"):
            setup_path = build_dir / "Modules" / name
            if not setup_path.is_file():
                continue
            lines = setup_path.read_text().splitlines()
            out = []
            for line in lines:
                if line.strip().startswith("readline "):
                    out.append("# disabled by ee-inspector: " + line)
                else:
                    out.append(line)
            setup_path.write_text("\n".join(out) + "\n")
            print(f"EE Inspector Pro: sanitized Modules/{name}")

        # Patch grpmodule.c
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


recipe = Python3Recipe()
