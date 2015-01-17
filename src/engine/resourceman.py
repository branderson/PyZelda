__author__ = 'brad'
import pygame
# import pyglet.media

class ResourceManager(object):
    def __init__(self, force_pygame=False, muted=False):
        pygame.font.init()
        pygame.mixer.init()
        self.sprites = {}
        self.music = {}
        self.sounds = {}
        self.fonts = {}
        self.force_pygame = True
        self.muted = muted

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

    def add_spritesheet_strip_offsets(self, key, spritesheet, topleft, image_count, per_line, image_size, hor_offset,
                                      ver_offset, colorkey=None):
        self.sprites[key] = spritesheet.load_strip_offsets(topleft, image_count, per_line, image_size, hor_offset,
                                                           ver_offset, colorkey)

    def get_images(self, key):
        return self.sprites[key]

    def add_font(self, key, filename, size):
        self.fonts[key] = pygame.font.Font(filename, size)

    def remove_font(self, key):
        del self.fonts[key]

    def add_music(self, key, filename):
        # if pyglet.media.have_avbin:
        #     self.music[key] = pyglet.media.load(filename)
        self.music[key] = filename

    def remove_music(self, key):
        del self.music[key]

    def play_music(self, key, start=0):
        if not self.muted:
            pygame.mixer.music.load(self.music[key])
            pygame.mixer.music.play(-1, start)
        # pygame.mixer.music.set_pos(start)
        # if pyglet.media.have_avbin and not self.force_pygame:
        #     self.music[key].play()

    def add_sound(self, key, filename):
        # if pyglet.media.have_avbin and not self.force_pygame:
        #     self.sounds[key] = pyglet.media.load(filename, streaming=False)
        # else:
        self.sounds[key] = pygame.mixer.Sound(filename)

    def remove_sound(self, key):
        del self.sounds[key]

    def play_sound(self, key):
        if not self.muted:
            self.sounds[key].play()