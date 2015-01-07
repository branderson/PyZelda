__author__ = 'brad'
import pygame


class ResourceManager(object):
    def __init__(self):
        pygame.font.init()
        self.sprites = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}

    def add_image(self, key, filename):
        try:
            self.sprites[key] = pygame.image.load(filename).convert_alpha()
            return True
        except:
            return False

    def remove_image(self, key):
        del self.sprites[key]

    def add_image_list(self, key, filenames):
        self.sprites[key] = []
        for filename in filenames:
            try:
                self.sprites[key].append(pygame.image.load(filename).convert_alpha())
            except:
                pass

    def add_spritesheet_image(self, key, spritesheet, rectangle, colorkey=None):
        self.sprites[key] = spritesheet.image_at(rectangle, colorkey)

    def add_spritesheet_image_list(self, key, spritesheet, rectangle_list, colorkey=None):
        self.sprites[key] = spritesheet.images_at(rectangle_list, colorkey)

    def add_spritesheet_strip(self, key, spritesheet, rect, image_count, colorkey=None):
        self.sprites[key] = spritesheet.load_strip(rect, image_count, colorkey)

    def get_images(self, key):
        return self.sprites[key]

    def add_font(self, key, filename, size):
        self.fonts[key] = pygame.font.Font(filename, size)

    def remove_font(self, key):
        del self.fonts[key]