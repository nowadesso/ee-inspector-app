"""Local sdl2 recipe: patch SDL_androidsensor.c during prebuild for NDK r27+ compat."""

from pathlib import Path

from pythonforandroid.recipes.sdl2 import SDL2Recipe as _Base


class SDL2Recipe(_Base):

    def prebuild_arch(self, arch):
        # Run the parent prebuild first (extracts sources, applies p4a patches)
        super().prebuild_arch(arch)

        build_dir = Path(self.get_build_dir(arch.arch))
        patched_count = 0

        for f in build_dir.rglob("SDL_androidsensor.c"):
            text = f.read_text()
            if "ALooper_pollAll" in text:
                f.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                patched_count += 1
                print(f"EE Inspector Pro: patched {f}")

        if patched_count == 0:
            print("EE Inspector Pro: no SDL_androidsensor.c with ALooper_pollAll found")
        else:
            print(f"EE Inspector Pro: patched {patched_count} file(s)")


recipe = SDL2Recipe()
