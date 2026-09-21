from pythonforandroid.recipes.sdl2 import SDL2Recipe as _Base


class SDL2Recipe(_Base):
    version = '2.28.5'
    url = 'http://mirror.koddos.net/blfs/conglomeration/SDL/SDL2-{version}.tar.gz'


recipe = SDL2Recipe()
