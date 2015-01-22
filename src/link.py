__author__ = 'brad'

import engine
import pygame

RESOURCE_DIR = '../resources/'
SPRITE_DIR = RESOURCE_DIR + 'sprite/'
SOUND_DIR = RESOURCE_DIR + 'sound/'


class Link(engine.GameObject):
    def __init__(self, layer=0):
        self.resource_manager = engine.ResourceManager()
        link_sheet = engine.Spritesheet(SPRITE_DIR + "LinkSheet6464192.png")

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_down', link_sheet, (37, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_up', link_sheet, (66, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_left', link_sheet, (5, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_right', link_sheet, (95, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_down', link_sheet, (56, 57), 2, 2, (15, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_up', link_sheet, (88, 57), 2, 2, (17, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_left', link_sheet, (21, 57), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_right', link_sheet, (122, 57), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_down', link_sheet, (131, 81), 2, 2, (17, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_up', link_sheet, (166, 81), 2, 2, (18, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_left', link_sheet, (97, 81), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # These two might be messed up
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_right', link_sheet, (204, 81), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield', link_sheet, (26, 81), 4, 4, (17, 16), 0, 0, (64, 64, 192))  # Needs to be fixed
        self.resource_manager.add_spritesheet_strip_offsets('link_hop_down', link_sheet, (287, 132), 3, 3, (17, 16), 0, 0, (64, 64, 192))
        engine.GameObject.__init__(self, self.resource_manager.get_images('link_walk_down'), layer,
                                   collision_rect=pygame.Rect((3, 4), (10, 11)),
                                   handle_collisions=True, object_type="player", persistent=True)

        # Add animations to Link
        self.add_animation('link_walk_up', self.resource_manager.get_images('link_walk_up'))
        self.add_animation('link_walk_down', self.resource_manager.get_images('link_walk_down'))
        self.add_animation('link_walk_right', self.resource_manager.get_images('link_walk_right'))
        self.add_animation('link_walk_left', self.resource_manager.get_images('link_walk_left'))
        self.add_animation('link_push_up', self.resource_manager.get_images('link_push_up'))
        self.add_animation('link_push_down', self.resource_manager.get_images('link_push_down'))
        self.add_animation('link_push_left', self.resource_manager.get_images('link_push_left'))
        self.add_animation('link_push_right', self.resource_manager.get_images('link_push_right'))
        self.add_animation('link_shield_walk_up', self.resource_manager.get_images('link_shield_walk_up'))
        self.add_animation('link_shield_walk_down', self.resource_manager.get_images('link_shield_walk_down'))
        self.add_animation('link_shield_walk_right', self.resource_manager.get_images('link_shield_walk_right'))
        self.add_animation('link_shield_walk_left', self.resource_manager.get_images('link_shield_walk_left'))
        self.add_animation('link_use_shield', self.resource_manager.get_images('link_use_shield'))
        self.add_animation('link_hop_down', self.resource_manager.get_images('link_hop_down'))

        # Add sounds to Link
        self.resource_manager.add_sound('link_hop', SOUND_DIR + 'LA_Link_Jump.wav')
        self.resource_manager.add_sound('link_shield', SOUND_DIR + 'LA_Shield.wav')

        # Configure Link's properties
        self.direction = 3
        self.facing = 3
        self.moves = []
        self.change_animation = False
        self.shield = False
        self.left = None
        self.right = None
        self.state = "walking"
        self.hop_frame = 0
        self.controllable = True
        self.no_clip = False
        self.direction_held = False

    def handle_animations(self):
        if self.change_animation:  # Later if walking
            if self.state == "hopping":
                self.set_animation('link_hop_down', 0)
            if self.facing == 0:
                # if self.colliding:
                if self.state == "colliding":
                    self.set_animation('link_push_right', 0)
                elif self.state == "using_shield":
                    self.set_animation('link_use_shield', 3)
                elif self.state == "walking":
                    if self.shield:
                        self.set_animation('link_shield_walk_right', 0)
                    else:
                        self.set_animation('link_walk_right', 0)
            elif self.facing == 1:
                # if self.colliding:
                if self.state == "colliding":
                    self.set_animation('link_push_up', 0)
                elif self.state == "using_shield":
                    self.set_animation('link_use_shield', 2)
                # elif self.shield:
                elif self.state == "walking":
                    if self.shield:
                        self.set_animation('link_shield_walk_up', 0)
                    else:
                        self.set_animation('link_walk_up', 0)
            elif self.facing == 2:
                # if self.colliding:
                if self.state == "colliding":
                    self.set_animation('link_push_left', 0)
                elif self.state == "using_shield":
                    self.set_animation('link_use_shield', 0)
                elif self.state == "walking":
                    # if self.shield:
                    #     self.set_animation('link_shield_walk_left', 0)
                    # else:
                    self.set_animation('link_walk_left', 0)
            elif self.facing == 3:
                # if self.colliding:
                if self.state == "colliding":
                    self.set_animation('link_push_down', 0)
                elif self.state == "using_shield":
                    self.set_animation('link_use_shield', 1)
                # elif self.shield and not self.hopping:
                # else:
                elif self.state == "walking":
                    if self.shield:
                        self.set_animation('link_shield_walk_down', 0)
                    else:
                        self.set_animation('link_walk_down', 0)

            # Set animation speeds
            # if self.colliding:
            if self.state == "colliding":
                self.animation_speed = 15
            elif self.state == "using_shield":
                pygame.Rect((3, 4), (10, 12))
                self.animation_speed = 0  # 0 means don't animate
            else:
                if self.state == "walking":
                    self.collision_rect = pygame.Rect((3, 4), (10, 11))
                self.animation_speed = 15

            self.change_animation = False

    def play_sound(self, key):
        self.resource_manager.play_sound(key)

    def hop(self, moved):
        if self.hop_frame < 3:
            if self.animation_counter >= 7:
                # print(str(self.hop_frame))
                self.next_frame(1)
                self.animation_counter = 0
                self.hop_frame += 1
        else:
            self.set_animation('link_walk_down', 0)
        if not moved:
            self.controllable = True
            # self.hopping = False
            self.state = "walking"
            self.change_animation = True
            self.hop_frame = 0