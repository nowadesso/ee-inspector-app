from pythonforandroid.recipe import Recipe

class OpenCVExtrasRecipe(Recipe):
    version = '4.12.0'
    url = 'https://github.com/opencv/opencv_contrib/archive/{version}.zip'
    depends = ['opencv']

recipe = OpenCVExtrasRecipe()
