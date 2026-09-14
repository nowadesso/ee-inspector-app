from multiprocessing import cpu_count
from os.path import join
import sh
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import NDKRecipe
from pythonforandroid.util import current_directory, ensure_dir

class OpenCVRecipe(NDKRecipe):
    version = '4.12.0'
    url = 'https://github.com/opencv/opencv/archive/{version}.zip'
    depends = ['numpy']
    patches = []
    generated_libraries = [
        'libopencv_features2d.so','libopencv_imgproc.so','libopencv_stitching.so',
        'libopencv_calib3d.so','libopencv_flann.so','libopencv_ml.so',
        'libopencv_videoio.so','libopencv_core.so','libopencv_highgui.so',
        'libopencv_objdetect.so','libopencv_video.so','libopencv_dnn.so',
        'libopencv_imgcodecs.so','libopencv_photo.so',
    ]
    def get_lib_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'build', 'lib', arch.arch)
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['ANDROID_NDK'] = self.ctx.ndk_dir
        env['ANDROID_SDK'] = self.ctx.sdk_dir
        return env
    def build_arch(self, arch):
        build_dir = join(self.get_build_dir(arch.arch), 'build')
        ensure_dir(build_dir)
        opencv_extras = []
        if 'opencv_extras' in self.ctx.recipe_build_order:
            d = self.get_recipe('opencv_extras', self.ctx).get_build_dir(arch.arch)
            opencv_extras = [f'-DOPENCV_EXTRA_MODULES_PATH={d}/modules', '-DBUILD_opencv_legacy=OFF']
        with current_directory(build_dir):
            env = self.get_recipe_env(arch)
            py_major = self.ctx.python_recipe.version[0]
            py_inc = self.ctx.python_recipe.include_root(arch.arch)
            site = self.ctx.get_site_packages_dir(arch)
            link_root = self.ctx.python_recipe.link_root(arch.arch)
            link_ver = self.ctx.python_recipe.link_version
            py_lib = join(link_root, f'libpython{link_ver}.so')
            numpy_inc = join(self.ctx.get_python_install_dir(arch.arch), 'numpy/_core/include')
            shprint(sh.cmake,
                '-DP4A=ON', f'-DANDROID_ABI={arch.arch}', f'-DANDROID_STANDALONE_TOOLCHAIN={self.ctx.ndk_dir}',
                f'-DANDROID_NATIVE_API_LEVEL={self.ctx.ndk_api}', f'-DANDROID_EXECUTABLE={env["ANDROID_SDK"]}/tools/android',
                '-DANDROID_SDK_TOOLS_VERSION=6514223','-DANDROID_PROJECTS_SUPPORT_GRADLE=ON',
                f'-DCMAKE_TOOLCHAIN_FILE={join(self.ctx.ndk_dir,"build","cmake","android.toolchain.cmake")}',
                f'-DCMAKE_SHARED_LINKER_FLAGS=-L{link_root} -lpython{link_ver}',
                '-DBUILD_WITH_STANDALONE_TOOLCHAIN=ON','-DBUILD_SHARED_LIBS=ON','-DBUILD_STATIC_LIBS=OFF',
                '-DBUILD_opencv_java=OFF','-DBUILD_opencv_java_bindings_generator=OFF',
                '-DBUILD_TESTS=OFF','-DBUILD_PERF_TESTS=OFF','-DENABLE_TESTING=OFF','-DBUILD_EXAMPLES=OFF','-DBUILD_ANDROID_EXAMPLES=OFF',
                f'-DBUILD_OPENCV_PYTHON{py_major}=ON', f'-DBUILD_OPENCV_PYTHON{"2" if py_major=="3" else "3"}=OFF',
                '-DOPENCV_SKIP_PYTHON_LOADER=ON', f'-DOPENCV_PYTHON{py_major}_INSTALL_PATH={site}',
                f'-DPYTHON_DEFAULT_EXECUTABLE={self.ctx.hostpython}', f'-DPYTHON{py_major}_EXECUTABLE={self.ctx.hostpython}',
                f'-DPYTHON{py_major}_INCLUDE_PATH={py_inc}', f'-DPYTHON{py_major}_LIBRARIES={py_lib}',
                f'-DPYTHON{py_major}_NUMPY_INCLUDE_DIRS={numpy_inc}', f'-DPYTHON{py_major}_PACKAGES_PATH={site}',
                *opencv_extras, self.get_build_dir(arch.arch), _env=env)
            link_txt = f'modules/python{py_major}/CMakeFiles/opencv_python{py_major}.dir/link.txt'
            with open(link_txt, 'r+') as f:
                content=f.read().replace('-version',' '); f.seek(0); f.write(content); f.truncate()
            shprint(sh.make, '-j'+str(cpu_count()), 'opencv_python'+py_major)
            shprint(sh.cmake, '-DCOMPONENT=python', '-P', './cmake_install.cmake')
            sh.cp('-a', sh.glob(f'./lib/{arch.arch}/lib*.so'), self.ctx.get_libs_dir(arch.arch))

recipe = OpenCVRecipe()
