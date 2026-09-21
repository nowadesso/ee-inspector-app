from pythonforandroid.recipes.jpeg import JPEGRecipe as _Base


class JPEGRecipe(_Base):

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        # Inject the CMake policy version fix for CMake 4.x
        env['CMAKE_POLICY_VERSION_MINIMUM'] = '3.5'
        return env


recipe = JPEGRecipe()
