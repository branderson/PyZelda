__author__ = 'brad'

import src.engine as engine

SPRITE_DIR = '../resources/sprite/'


class LinkSword(engine.GameObject):
    def __init__(self, facing):
        self.resource_manager = engine.ResourceManager()
        link_sheet = engine.Spritesheet(SPRITE_DIR + "Link.png")

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_right', link_sheet, (192, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_up', link_sheet, (128, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_down', link_sheet, (64, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_left', link_sheet, (0, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.directions = ['link_sword_right', 'link_sword_up', 'link_sword_left', 'link_sword_down']

        engine.GameObject.__init__(self, image=self.resource_manager.get_images(self.directions[facing]), layer=25,
                                   persistent=True)

        self.add_animation('link_sword_up', self.resource_manager.get_images('link_sword_up'))
        self.add_animation('link_sword_down', self.resource_manager.get_images('link_sword_down'))
        self.add_animation('link_sword_right', self.resource_manager.get_images('link_sword_right'))
        self.add_animation('link_sword_left', self.resource_manager.get_images('link_sword_left'))

        self.set_animation(self.directions[facing], 0)

        self.animation_speed = 30