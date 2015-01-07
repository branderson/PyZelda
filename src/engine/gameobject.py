__author__ = 'brad'
import pygame
import math


class GameObject(pygame.sprite.Sprite, object):

    def __init__(self, image=None, layer=0, masks=None, collision_rect=None, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        if image is None:
            self.image = pygame.Surface((0, 0))
        else:
            self.image = image
        self.flipped_hor = False
        self.flipped_ver = False
        self.visible = True
        self.current_animation = None
        self.animation_frame = 0
        if collision_rect is None:
            collision_rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.image_scaled = None
        self.rect_scaled = self.image.get_rect()
        self.collision_rect = collision_rect
        self.rect_draw = self.image.get_rect()
        self.layer = layer
        self.masks = []
        self.images['image'] = self.image
        self.current_image = self.images['image']
        self.angle = angle
        self.rotate(0)
        if masks is not None:
            for mask in masks:
                self.add_mask(mask)

    def add_mask(self, mask):
        self.masks.append(mask)

    def remove_mask(self, mask):
        if self.masks.count(mask) != 0:
            while self.masks.remove(mask):
                pass

    def add_image(self, key, surface):
        self.images[key] = surface

    def change_image(self, key):
        self.image = self.images[key]
        self.current_image = self.images[key]
        self.rotate(0)

    def remove_image(self, key):
        if key in self.images:
            del self.images[key]

    def add_animation(self, key, image_list):
        self.images[key] = image_list

    def change_animation_frame(self, key, frame):
        self.image = self.images[key][frame]
        self.animation_frame = frame
        self.current_image = self.images[key][frame]
        self.rotate(0)

    def set_animation(self, key, starting_frame=0):
        self.image = self.images[key][starting_frame]
        self.animation_frame = 0
        self.current_animation = key
        self.current_image = self.images[key][starting_frame]
        self.rotate(0)

    def next_frame(self, direction=1):
        if direction == -1:
            self.animation_frame -= 1
        else:
            self.animation_frame += 1

        if self.animation_frame != 0 and self.animation_frame < self.images[self.current_animation].__len__():
            self.image = self.images[self.current_animation][self.animation_frame]
            self.current_image = self.images[self.current_animation][self.animation_frame]
            self.rotate(0)
            return True
        else:
            return False

    def destroy(self):
        self.__del__()
        return True

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def draw(self, surface, x_scale, y_scale, x, y):
        # TODO: May need to change image to current_image. Also go through and make sure using right image consistently
        rect_scaled = pygame.Rect((x-self.rect.x*x_scale, y-self.rect.y*y_scale), (int(self.rect.width*x_scale),
                                                                                   int(self.rect.height*y_scale)))
        surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
                                                         int(self.image.get_height()*y_scale))), rect_scaled)

    # def scale(self, x_scale, y_scale):
    # TODO: Implement GameObject.scale()
    #     self.image_scaled = pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
    #                                                             int(self.image.get_height()*y_scale)))
    #     # self.rect_scaled.inflate_ip(-x_scale, -y_scale)
    #     self.rect = pygame.Rect(self.rect.topleft, (int(self.rect.width*x_scale), int(self.rect.height*y_scale)))
    #     # print(str(self.rect_scaled.x) + " " + str(self.rect_scaled.y))
    #     # pygame.quit()

    def rotate(self, angle):
        self.angle += angle
        rect = self.rect
        flipped_image = pygame.transform.flip(self.current_image, self.flipped_hor, self.flipped_ver)
        # flipped_image = self.image
        self.image = pygame.transform.rotate(flipped_image, self.angle)
        # self.image = pygame.transform.flip(self.image, self.flipped_hor, self.flipped_ver)
        rect.center = self.image.get_rect().center
        self.rect = rect

    # Rotates about center, clipping to original width and height
    # Don't use this, doesn't work
    def rotate_clip(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle
        rect = self.rect
        self.image = pygame.transform.rotate(self.current_image, self.angle)
        rect.center = self.image.get_rect().center
        self.image = self.image.subsurface(rect).copy()

    def flip(self, flip_hor, flip_ver):
        if flip_hor:
            self.flipped_hor = not self.flipped_hor
        if flip_ver:
            self.flipped_ver = not self.flipped_ver
        self.rotate(0)

    @staticmethod
    def tint(input_surface, (r, g, b, a)):
        surface = input_surface.copy()
        surface.lock()
        for x in range(0, surface.get_width() - 1):
            for y in range(0, surface.get_height() - 1):
                new_r = surface.get_at((x, y)).r + r
                if new_r > 255:
                    new_r = 255
                elif new_r < 0:
                    new_r = 0
                new_g = surface.get_at((x, y)).g + g
                if new_g > 255:
                    new_g = 255
                elif new_g < 0:
                    new_g = 0
                new_b = surface.get_at((x, y)).b + b
                if new_b > 255:
                    new_b = 255
                elif new_b < 0:
                    new_b = 0
                new_a = surface.get_at((x, y)).a + a
                if new_a > 255:
                    new_a = 255
                elif new_a < 0:
                    new_a = 0
                surface.set_at((x, y), (new_r, new_g, new_b, new_a))
        surface.unlock()
        return surface