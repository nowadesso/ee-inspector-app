"""Local sdl2_ttf recipe that patches HarfBuzz pragma for Clang 16+."""

import types
from pathlib import Path

import pythonforandroid.recipes.sdl2_ttf as _sdl2_ttf


_recipe = _sdl2_ttf.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    try:
        build_dir = Path(self.ctx.bootstrap.build_dir)
    except Exception:
        build_dir = None

    if build_dir and build_dir.exists():
        for f in build_dir.rglob("hb.hh"):
            text = f.read_text()
            if 'diagnostic error "-Wcast-function-type-strict"' not in text:
                print(f"EE Inspector Pro: hb.hh already fixed or pattern not found: {f}")
                continue
            text = text.replace(
                '#pragma GCC diagnostic error "-Wcast-function-type-strict"',
                '#pragma GCC diagnostic ignored "-Wcast-function-type-strict"'
            )
            f.write_text(text)
            print(f"EE Inspector Pro: fixed pragma in {f}")

    return _original_build_arch(arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
