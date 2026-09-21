# Auto-patch p4a's sdl2 recipe to replace ALooper_pollAll with ALooper_pollOnce.
# Loaded by Python at interpreter startup.
try:
    import pythonforandroid.recipes.sdl2 as _sdl2
    _recipe = _sdl2.recipe
    _original_prebuild_arch = _recipe.prebuild_arch

    def _patched_prebuild_arch(self, arch):
        result = _original_prebuild_arch(arch)
        from pathlib import Path
        build_dir = Path(self.get_build_dir(arch.arch))
        for f in build_dir.rglob("SDL_androidsensor.c"):
            text = f.read_text()
            if "ALooper_pollAll" in text:
                f.write_text(text.replace("ALooper_pollAll", "ALooper_pollOnce"))
                print(f"EE Inspector Pro: patched {f}")
        return result

    _recipe.prebuild_arch = _patched_prebuild_arch
    print("EE Inspector Pro: sdl2 patch hook installed via sitecustomize")
except Exception as e:
    print(f"EE Inspector Pro: sdl2 patch hook failed: {e}")
