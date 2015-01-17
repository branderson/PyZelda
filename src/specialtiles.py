__author__ = 'brad'

import engine


class ShortGrass(engine.GameObject):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('tile_set')[229],
                                   layer=-500, handle_collisions=True, object_type="short_grass")


class BigBeachGrass(engine.GameObject):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('tile_set')[254],
                                   layer=-500, handle_collisions=True, object_type="big_beach_grass")


class Hole(engine.GameObject):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('tile_set')[232],
                                   layer=-500, handle_collisions=True, object_type="big_beach_grass", solid=True)