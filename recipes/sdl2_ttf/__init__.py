"""Local sdl2_ttf recipe that patches HarfBuzz for Clang 16+ compatibility."""

import types
from pathlib import Path

import pythonforandroid.recipes.sdl2_ttf as _sdl2_ttf


_recipe = _sdl2_ttf.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    # Find hb.hh inside the vendored HarfBuzz source tree.
    # SDL_ttf extracts HarfBuzz into external/harfbuzz/ during ndk-build.
    build_dir = Path(self.ctx.bootstrap.build_dir)

    for hb_hh in build_dir.rglob("hb.hh"):
        text = hb_hh.read_text()
        if "-Wcast-function-type-strict" in text:
            print(f"EE Inspector Pro: hb.hh already patched: {hb_hh}")
            break
        # Insert the pragma right after the last existing pragma line.
        lines = text.splitlines()
        insert_at = None
        for i, line in enumerate(lines):
            if line.strip().startswith("#pragma GCC diagnostic ignored"):
                insert_at = i + 1
        if insert_at is None:
            print(f"EE Inspector Pro: no pragma section found in {hb_hh}")
            break
        lines.insert(insert_at, '#pragma GCC diagnostic ignored "-Wcast-function-type-strict"')
        hb_hh.write_text("\n".join(lines) + "\n")
        print(f"EE Inspector Pro: patched {hb_hh}")
        break

    return _original_build_arch(self, arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
