[app]

# (str) Title of your application
title = EE Inspector Pro
# (str) Package name
package.name = eeinspectorpro
# (str) Package domain (needed for android/ios packaging)
package.domain = org.yourdomain
# (str) Source code where the main.py live
source.dir = .
# (list) Source extensions
source.include_exts = py,png,jpg,kv,atlas
# (list) Source folders to include (let empty to include all folders)
source.include_dirs = 
# (str) Application version (maj.min.patch)
version = 0.1
# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,requests,numpy,opencv-python-headless
#requirements = kivymd==2.1.0, kivy, opencv-python-headless, numpy, Pillow
#requirements = python3,kivymd,requests,numpy,opencv
# (str) Custom source folders for requirements
# Sets the source directory for the specified requirements
# e.g. requirements = sqlite3:sqlite
# (str) OUYA Console category
# ouya.category = GAME
# (str) Orientation, one of landscape, sensorLandscape, portrait or sensorPortrait
# (str) Android/additional permissions
android.permissions = INTERNET,CAMERA,BLUETOOTH_SCAN,BLUETOOTH_CONNECT
# (int) Target Android API, should be as high as possible.
android.api = 33
# (int) Min API your APK will support.
android.minapi = 24
# (int) Android NDK API to use. This is the most important setting, it should match the
# *ndk version used by *p4a, which is 28c by default.
# (This is the NDK version bundled with the p4a toolchain)
android.ndk = 28c
# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you don't want to wait it.
android.accept_sdk_license = True
# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
# android.accept_sdk_license = False
# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a
# (int) android logcat filters to see, see logcat_projectfilter
# (int) Project path. Should be the path of your local git repository.
# (str) The path to the buildozer project directory
buildozer_dir = .buildozer
# (str) The path to the bin directory, where the apk will be stored
# (str) The path to the android project directory
android.project_dir = .buildozer/android/project
# (str) The name of the AndroidManifest.xml file to use
# android.manifest = AndroidManifest.xml
# (str) The name of the .apk file to use
# android.apk = main.py
# (str) The name of the .obb file to use
# android.obb = main.py
# (bool) Indicate if the application should be debuggable
# android.debug = True
# (str) The Android NDK version to use
# android.ndk = 23b
# (bool) If True, then skip running the ndk_build
# android.skip_ndk_build = False
# (str) python-for-android branch to use, choices: master, develop
# p4a.branch = master
# (str) python-for-android specific commit
# p4a.commit = HEAD
# (str) python-for-android git clone directory (if empty, it will be cloned from github)
# p4a.source_dir =
# (list) requirements to include, for more information see
#            https://github.com/kivy/python-for-android/blob/master/README.requirements.rst
# p4a.requirements = python3,kivy,sqlite3,pyjnius,openssl,android
# (str) Custom recipes path
p4a.local_recipes = ./recipes

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
# (int) Display warning if buildozer is run as root (0 = no warning, 1 = warning)
warn_on_root = 1
# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer
# (str) Path to the bin directory (working directory for binary generation)
bin_dir = bin
requirements = hostpython3,hostpip3,clang,libc6-dev,libffi-dev,libssl-dev
[buildozer_mode]

# (bool) If set to True, Buildozer will not ask for confirmation before deleting the .buildozer folder
no_build_cache = False
