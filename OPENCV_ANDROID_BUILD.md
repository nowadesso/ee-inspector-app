# OpenCV Android build

This project intentionally builds OpenCV from source with python-for-android instead of installing `opencv-contrib-python-headless` from PyPI.

Why: PyPI's `opencv-contrib-python-headless` wheels are desktop/Linux wheels, not Android wheels. python-for-android requires a recipe for compiled Android dependencies.

Included:
- `recipes/opencv` — OpenCV 4.12.0 + Python `cv2` bindings
- `recipes/opencv_extras` — OpenCV Contrib modules 4.12.0
- `numpy` dependency
- `p4a.local_recipes = ./recipes`

The old `p4a_requirements = pip==21.3.1` was removed because it can break the modern Python-for-Android build environment.
