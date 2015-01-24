__author__ = 'brad'

import engine
import pygame


class HUD(engine.CoordinateSurface):
    def __init__(self, screen_width, screen_height):
        engine.CoordinateSurface.__init__(self, pygame.Rect((0, 0), (screen_width, screen_height/8)), (160, 16))