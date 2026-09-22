[app]

title = EE Inspector Pro
package.name = eeinspectorpro
package.domain = org.yourdomain

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_dirs =

version = 0.1
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1,https://github.com/kivymd/KivyMD/archive/refs/tags/2.0.0.zip,materialyoucolor==3.0.3,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,android,requests,numpy,opencv,opencv_extras
#requirements = python3==3.12.10,hostpython3==3.12.10,kivy==2.3.1,https://github.com/kivymd/KivyMD/archive/refs/tags/2.0.0.zip,materialyoucolor==3.0.3,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,android,requests,numpy,opencv,opencv_extras,liblzma
#requirements = python3==3.12.10,hostpython3==3.12.10,kivy==2.3.1,https://github.com/kivymd/KivyMD/archive/refs/tags/2.0.0.zip,materialyoucolor==3.0.3,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,android,requests,numpy,opencv,opencv_extras

orientation = portrait
fullscreen = 0
gles2 = 1

android.permissions = INTERNET,CAMERA,BLUETOOTH_SCAN,BLUETOOTH_CONNECT
android.api = 33
android.minapi = 24
android.ndk = 28c
android.accept_sdk_license = True
#android.sdk_path = /github/home/.buildozer/android/platform/android-sdk
#android.sdk_path = /github/home/.buildozer/android/platform/android-sdk/cmdline-tools/latest
android.archs = arm64-v8a

buildozer_dir = .buildozer
android.project_dir = .buildozer/android/project

# python-for-android
#p4a.branch = v2024.01.21
p4a.local_recipes = %(source.dir)s/recipes
#p4a.local_recipes = ../../../../recipes

[buildozer]

log_level = 2
warn_on_root = 0
build_dir = .buildozer
bin_dir = bin

[buildozer_mode]

no_build_cache = False
