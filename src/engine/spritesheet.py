__author__ = 'brad'

import pygame


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load image at location
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x, y, x+offset, y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a list of images
    def images_at(self, rectangle_list, colorkey=None):
        return [self.image_at(rectangle, colorkey) for rectangle in rectangle_list]

    # Load a strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        rectangle_list = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(rectangle_list, colorkey)