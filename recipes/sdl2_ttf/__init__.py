"""Diagnostic: print pragma lines from hb.hh to find the exact pattern."""

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
            print(f"EE Inspector Pro: inspecting {f}")
            for i, line in enumerate(f.read_text().splitlines(), start=1):
                if "diagnostic" in line or "cast-function-type" in line:
                    print(f"  line {i}: {line!r}")

    return _original_build_arch(arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
