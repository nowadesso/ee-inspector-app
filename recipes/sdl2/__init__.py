"""Local sdl2 recipe that patches SDL_androidsensor.c for NDK r27+ compatibility."""
from pathlib import Path

import pythonforandroid.recipes.sdl2 as _sdl2


# Find the recipe class regardless of its name
_Base = None
for name in dir(_sdl2):
    obj = getattr(_sdl2, name)
    if isinstance(obj, type) and name.endswith("Recipe"):
        _Base = obj
        break

if _Base is None:
    raise ImportError("Could not find SDL2 recipe class in pythonforandroid.recipes.sdl2")


class SDL2Recipe(_Base):

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = Path(self.get_build_dir(arch.arch))

        for f in build_dir.rglob("SDL_androidsensor.c"):
            text = f.read_text()
            if "ALooper_pollAll" in text:
                f.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                print(f"EE Inspector Pro: patched {f}")
            else:
                print(f"EE Inspector Pro: no patch needed for {f}")


recipe = SDL2Recipe()
