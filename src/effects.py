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
        self.resource_manager.add_spritesheet_image('effect_short_grass', self.effect_sheet, ((1, 1), (17, 17)), (64, 64, 192))
        self.add_image('effect_short_grass', self.resource_manager.get_images('effect_short_grass'))
        self.set_image('effect_short_grass')