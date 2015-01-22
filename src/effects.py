__author__ = 'brad'

import engine

RESOURCE_DIR = '../resources/'
SPRITE_DIR = RESOURCE_DIR + 'sprite/'


class AbstractEffect(engine.GameObject):
    def __init__(self, object_type):
        self.resource_manager = engine.ResourceManager()
        self.effect_sheet = engine.Spritesheet(SPRITE_DIR + "Effects.png")
        engine.GameObject.__init__(self, layer=100, object_type=object_type)


class ShortGrass(AbstractEffect):
    def __init__(self):
        AbstractEffect.__init__(self, 'effect_short_grass')
        self.resource_manager.add_spritesheet_strip_offsets('effect_short_grass', self.effect_sheet,
                                                            (0, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.add_animation('image', self.resource_manager.get_images('effect_short_grass'))
        self.set_animation('image')


class ShortForestGrass(AbstractEffect):
    def __init__(self):
        AbstractEffect.__init__(self, 'effect_short_forest_grass')
        self.resource_manager.add_spritesheet_strip_offsets('effect_short_forest_grass', self.effect_sheet,
                                                            (0, 17), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.add_animation('image', self.resource_manager.get_images('effect_short_forest_grass'))
        self.set_animation('image')