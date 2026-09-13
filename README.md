# ee-inspector-app

## Android build notes

This project intentionally keeps **OpenCV + OpenCV Contrib** through local
python-for-android recipes in `recipes/opencv` and `recipes/opencv_extras`.
Do not replace them with `opencv-contrib-python-headless`, because ordinary
PyPI OpenCV wheels are not Android builds.

The Android build pins:
- python-for-android `master`
- target/host Python 3.12.10
- Kivy 2.3.1
- KivyMD 2.0.0 from its source archive
- OpenCV 4.12.0 + OpenCV Contrib 4.12.0

The GitHub Actions workflow also clears stale python-for-android build state
before rebuilding, which is important after changing KivyMD or Python versions.
