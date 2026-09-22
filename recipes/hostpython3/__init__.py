"""Local hostpython3 recipe that installs setuptools with distutils shim."""

import types
from pathlib import Path

import pythonforandroid.recipes.hostpython3 as _hostpython3


_recipe = _hostpython3.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    result = _original_build_arch(self, arch)
    
    # Find the host python binary and install setuptools into it.
    build_dir = Path(self.get_build_dir(arch.arch))
    hostpython = build_dir / "native-build" / "python3"
    
    if hostpython.is_file():
        import subprocess
        try:
            subprocess.check_call([
                str(hostpython), "-m", "pip", "install", "--upgrade", "setuptools"
            ])
            print("EE Inspector Pro: installed setuptools into hostpython")
        except Exception as e:
            print(f"EE Inspector Pro: failed to install setuptools: {e}")
    
    return result


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
