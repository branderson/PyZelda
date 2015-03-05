__author__ = 'brad'

import src.engine as engine
from pygame import Rect

SPRITE_DIR = '../resources/sprite/'


class LinkSword(engine.GameObject):
    def __init__(self, facing, mode="slash"):
        self.resource_manager = engine.ResourceManager()
        link_sheet = engine.Spritesheet(SPRITE_DIR + "Link.png")

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_right', link_sheet, (192, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_up', link_sheet, (128, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_down', link_sheet, (64, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_left', link_sheet, (0, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_spin_clockwise', link_sheet, (0, 144), 8, 8, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_spin_counter', link_sheet, (0, 160), 8, 8, (16, 16), 0, 0, (64, 64, 192))
        self.directions = ['link_sword_right', 'link_sword_up', 'link_sword_left', 'link_sword_down']

        engine.GameObject.__init__(self, image=self.resource_manager.get_images(self.directions[facing]), layer=25,
                                   persistent=True)

        self.add_animation('link_sword_up', self.resource_manager.get_images('link_sword_up'))
        self.add_animation('link_sword_down', self.resource_manager.get_images('link_sword_down'))
        self.add_animation('link_sword_right', self.resource_manager.get_images('link_sword_right'))
        self.add_animation('link_sword_left', self.resource_manager.get_images('link_sword_left'))
        self.add_animation('link_sword_spin_clockwise', self.resource_manager.get_images('link_sword_spin_clockwise'))
        self.add_animation('link_sword_spin_counter', self.resource_manager.get_images('link_sword_spin_counter'))

        self.set_animation(self.directions[facing], 0)

        self.animation_speed = 30

        self.facing = facing
        self.handle_collisions = True
        frame_col = {'up': ((3, 10), (1, 6)),
                     'ur': ((0, 6), (10, 10)),
                     'right': ((0, 11), (6, 1)),
                     'dr': ((0, 0), (10, 10)),
                     'down': ((11, 0), (1, 6)),
                     'dl': ((6, 0), (10, 10)),
                     'left': ((10, 11), (6, 1)),
                     'ul': ((6, 6), (10, 10)),
                     'right_upper': ((0, 3), (6, 1)),
                     'nu': ((0, 16), (0, 0)), 'nr': ((0, 10), (0, 0)), 'nd': ((0, 0), (0, 0)), 'nl': ((16, 10), (0, 0))}
        self.collision_rects = {'link_sword_up': [Rect(frame_col['right_upper']), Rect(frame_col['ur']), Rect(frame_col['up'])],
                                'link_sword_down': [Rect(frame_col['left']), Rect(frame_col['dl']), Rect(frame_col['down'])],
                                'link_sword_right': [Rect(frame_col['up']), Rect(frame_col['ur']), Rect(frame_col['right'])],
                                'link_sword_left': [Rect(frame_col['up']), Rect(frame_col['ul']), Rect(frame_col['left'])],
                                'link_sword_spin_clockwise': [Rect(frame_col['dr']), Rect(frame_col['down']),
                                                              Rect(frame_col['dl']), Rect(frame_col['left']),
                                                              Rect(frame_col['ul']), Rect(frame_col['up']),
                                                              Rect(frame_col['ur']), Rect(frame_col['right'])],
                                'link_sword_spin_counter': [Rect(frame_col['dl']), Rect(frame_col['down']),
                                                            Rect(frame_col['dr']), Rect(frame_col['right']),
                                                            Rect(frame_col['ur']), Rect(frame_col['up']),
                                                            Rect(frame_col['ul']), Rect(frame_col['left'])]}

    def update_collisions(self):
        self.collision_rect = self.collision_rects[self.current_key][self.animation_frame]