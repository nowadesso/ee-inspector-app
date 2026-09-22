"""EE Inspector Pro local Python 3 recipe."""

from pathlib import Path

from pythonforandroid.recipes.python3 import Python3Recipe as _Base


class Python3Recipe(_Base):

    def build_arch(self, arch):
        extra = [
            "--without-readline",
            "--without-curses",
            "--without-panel",
            "--without-terminfo",
        ]
        self.configure_args = list(self.configure_args) + [
            f for f in extra if f not in self.configure_args
        ]
        print("EE Inspector Pro: configure_args =", self.configure_args)
        super().build_arch(arch)

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)

        build_dir = Path(self.get_build_dir(arch.arch))
        grp_file = build_dir / "Modules" / "grpmodule.c"
        if grp_file.is_file():
            text = grp_file.read_text()
            # Comment out the calls that don't exist on Android NDK.
            text = text.replace("setgrent();", "/* setgrent(); */")
            text = text.replace("endgrent();", "/* endgrent(); */")
            text = text.replace(
                "while ((p = getgrent()) != NULL) {",
                "while (0) {",
            )
            grp_file.write_text(text)
            print("EE Inspector Pro: neutralised grpmodule.c calls")
