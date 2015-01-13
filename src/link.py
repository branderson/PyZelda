__author__ = 'brad'

import engine
import pygame


class Link(engine.GameObject):
    def __init__(self, image=None, layer=0):
        engine.GameObject.__init__(self, image, layer, collision_rect=pygame.Rect((3, 3), (10, 10)),
                                   handle_collisions=True, object_type="player")
        self.direction = 3
        self.facing = 3
        self.animation_counter = 0
        self.change_animation = False
        self.colliding = False