"""Local sdl2 recipe that patches SDL_androidsensor.c for NDK r27+ compatibility."""

import types
from pathlib import Path

import pythonforandroid.recipes.sdl2 as _sdl2


_recipe = _sdl2.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    try:
        build_dir = Path(self.ctx.bootstrap.build_dir)
    except Exception:
        build_dir = None

    if build_dir and build_dir.exists():
        for f in build_dir.rglob("SDL_androidsensor.c"):
            text = f.read_text()
            if "ALooper_pollAll" in text:
                f.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                print(f"EE Inspector Pro: patched {f}")

    return _original_build_arch(arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
