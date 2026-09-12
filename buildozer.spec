[app]

title = EE Inspector Pro
package.name = eeinspectorpro
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_dirs = 
version = 0.1
requirements = python3,kivymd,requests,numpy==1.26.5,opencv
android.permissions = INTERNET,CAMERA,BLUETOOTH_SCAN,BLUETOOTH_CONNECT
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.minapi = 24
android.accept_sdk_license = 1
p4a.local_recipes = ./recipes 
log_level = 2
warn_on_root = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
# (int) Display warning if buildozer is run as root (0 = no warning, 1 = warning)
warn_on_root = 1
# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = .buildozer
# (str) Path to the bin directory (working directory for binary generation)
bin_dir = bin

[buildozer_mode]

# (bool) If set to True, Buildozer will not ask for confirmation before deleting the .buildozer folder
no_build_cache = False
