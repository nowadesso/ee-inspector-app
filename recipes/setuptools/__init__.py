"""Local setuptools recipe that fixes the distutils import for Python 3.12."""

import types
from pathlib import Path

import pythonforandroid.recipes.setuptools as _setuptools


_recipe = _setuptools.recipe
_original_build_arch = _recipe.build_arch


def _patched_build_arch(self, arch):
    # Patch the setuptools setup.py to import from setuptools
    # instead of distutils, and ensure setuptools is installed.
    build_dir = Path(self.get_build_dir(arch.arch))
    setup_py = build_dir / "setup.py"

    if setup_py.is_file():
        text = setup_py.read_text()
        if "import distutils" in text or "from distutils" in text:
            # Replace distutils imports with setuptools equivalents
            text = text.replace(
                "from distutils.core import setup",
                "from setuptools import setup"
            )
            text = text.replace(
                "import distutils",
                "import setuptools as distutils"
            )
            setup_py.write_text(text)
            print(f"EE Inspector Pro: patched {setup_py}")

    return _original_build_arch(self, arch)


_recipe.build_arch = types.MethodType(_patched_build_arch, _recipe)

recipe = _recipe
