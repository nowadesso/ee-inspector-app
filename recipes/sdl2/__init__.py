"""Local sdl2 recipe that patches SDL_androidsensor.c for NDK r27+ compatibility."""

from pathlib import Path

import pythonforandroid.recipes.sdl2 as _sdl2


# Get the recipe object p4a already created for sdl2.
_recipe = _sdl2.recipe


# Wrap the existing build_arch method.
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    from pathlib import Path

    # Figure out where SDL2 source was extracted. In recent p4a the sdl2
    # bootstrap keeps the source in the bootstrap build dir. Search widely.
    candidates = [
        Path(self.ctx.bootstrap.build_dir) / "jni" / "SDL" / "src" / "sensor" / "android" / "SDL_androidsensor.c",
    ]
    for root in [
        Path(self.ctx.bootstrap.build_dir),
        Path(self.get_build_dir(arch.arch)) if hasattr(self, 'get_build_dir') else None,
    ]:
        if root is None or not root.exists():
            continue
        for p in root.rglob("SDL_androidsensor.c"):
            if p not in candidates:
                candidates.append(p)

    for path in candidates:
        if path.is_file():
            text = path.read_text()
            if "ALooper_pollAll" in text:
                path.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                print(f"EE Inspector Pro: patched {path}")
            break

    return _original_build_arch(self, arch)


_recipe.build_arch = _patched_build_arch


# Re-export so p4a uses our patched recipe.
recipe = _recipe
