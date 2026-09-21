"""EE Inspector Pro local Python 3 recipe."""

import os
from pathlib import Path

from pythonforandroid.recipes.python3 import Python3Recipe as _Base
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory


class Python3Recipe(_Base):

    # No patches — we ship none.
    patches = []

    # Force-disable these modules at configure time.
    configure_args = [
        "--disable-ipv6",
        "--without-curses",
        "--without-readline",
        "--without-panel",
        "--without-terminfo",
        "--enable-unicode",
        "--with-openssl=",
    ]

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = Path(self.get_build_dir(arch.arch))

        # 1. Neutralize lzma and readline in every Setup file.
        for name in ("Setup", "Setup.dist", "Setup.local"):
            setup_path = build_dir / "Modules" / name
            if not setup_path.is_file():
                continue
            lines = setup_path.read_text().splitlines()
            out = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("readline ") or stripped.startswith("lzma "):
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


recipe = Python3Recipe()
