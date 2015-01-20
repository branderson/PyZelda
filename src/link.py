__author__ = 'brad'

import engine
import pygame


class Link(engine.GameObject):
    def __init__(self, image=None, layer=0):
        engine.GameObject.__init__(self, image, layer,  collision_rect=pygame.Rect((3, 4), (10, 11)),
                                   handle_collisions=True, object_type="player", persistent=True)
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

    def add_animations(self, resource_manager):
        self.add_animation('link_walk_up', resource_manager.get_images('link_walk_up'))
        self.add_animation('link_walk_down', resource_manager.get_images('link_walk_down'))
        self.add_animation('link_walk_right', resource_manager.get_images('link_walk_right'))
        self.add_animation('link_walk_left', resource_manager.get_images('link_walk_left'))
        self.add_animation('link_push_up', resource_manager.get_images('link_push_up'))
        self.add_animation('link_push_down', resource_manager.get_images('link_push_down'))
        self.add_animation('link_push_left', resource_manager.get_images('link_push_left'))
        self.add_animation('link_push_right', resource_manager.get_images('link_push_right'))
        self.add_animation('link_shield_walk_up', resource_manager.get_images('link_shield_walk_up'))
        self.add_animation('link_shield_walk_down', resource_manager.get_images('link_shield_walk_down'))
        self.add_animation('link_shield_walk_right', resource_manager.get_images('link_shield_walk_right'))
        self.add_animation('link_shield_walk_left', resource_manager.get_images('link_shield_walk_left'))
        self.add_animation('link_use_shield', resource_manager.get_images('link_use_shield'))
        self.add_animation('link_hop_down', resource_manager.get_images('link_hop_down'))

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