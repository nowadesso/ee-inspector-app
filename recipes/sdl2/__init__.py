"""Local sdl2 recipe that patches SDL_androidsensor.c for NDK r27+ compatibility."""

import types
from pathlib import Path

import pythonforandroid.recipes.sdl2 as _sdl2


_recipe = _sdl2.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    from pathlib import Path

    # Try several locations where SDL_androidsensor.c might be extracted.
    roots = []
    try:
        roots.append(Path(self.ctx.bootstrap.build_dir))
    except Exception:
        pass

    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("SDL_androidsensor.c"):
            text = p.read_text()
            if "ALooper_pollAll" in text:
                p.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                print(f"EE Inspector Pro: patched {p}")

    return _original_build_arch(arch)


# Bind as a proper method so self is passed correctly.
_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)


recipe = _recipe
