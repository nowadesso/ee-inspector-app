"""Local sdl2_ttf recipe that patches HarfBuzz for Clang 16+ compatibility."""

import types
from pathlib import Path

import pythonforandroid.recipes.sdl2_ttf as _sdl2_ttf


_recipe = _sdl2_ttf.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    # Find hb-ft.cc and add a pragma to silence the cast-function-type-strict error.
    try:
        build_dir = Path(self.ctx.bootstrap.build_dir)
    except Exception:
        build_dir = None

    if build_dir and build_dir.exists():
        for f in build_dir.rglob("hb-ft.cc"):
            text = f.read_text()
            if "-Wcast-function-type-strict" in text:
                print(f"EE Inspector Pro: hb-ft.cc already patched: {f}")
                continue
            # Prepend the pragma at the very top of the file.
            patched = (
                '#pragma GCC diagnostic ignored "-Wcast-function-type-strict"\n'
                + text
            )
            f.write_text(patched)
            print(f"EE Inspector Pro: patched {f}")

    return _original_build_arch(arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
