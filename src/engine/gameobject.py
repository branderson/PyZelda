__author__ = 'brad'
import pygame
import math


class GameObject(pygame.sprite.Sprite, object):

    def __init__(self, image=None, layer=0, masks=None, collision_rect=None, angle=0, position=(0, 0),
                 handle_collisions=False, object_type=None, properties=None, visible=True, persistent=False,
                 tile_id = None):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        self.images['image'] = {}
        self.images['image'][0] = []
        if image is None:
            self.images['image'][0].append(pygame.Surface((0, 0)))
        else:
            self.images['image'][0].append(image)
        self.flipped_hor = False
        self.flipped_ver = False
        self.visible = visible
        self.current_animation = None
        self.animation_frame = 0
        self.animation_speed = 15  # How many frames to wait between frames
        self.animation_counter = 0
        self.frame_ready = False
        self.current_image = self.images['image']
        self.current_key = 'image'
        if collision_rect is None:
            self.collision_rect = self.images['image'][0][0].get_rect()
        else:
            self.collision_rect = collision_rect
        self.rect = self.images['image'][0][0].get_rect()
        # self.rect_scaled = self.rect.copy()
        # self.rect_draw = self.images['image'].get_rect()
        self.layer = layer
        self.masks = []
        # self.images['image'] = self.image
        self.angle = angle
        self.position = position
        self.handle_collisions = handle_collisions
        self.object_type = object_type
        self.persistent = persistent
        self.updated = True
        self.updated_sprite = False
        self.solid = False
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties
            for object_property in properties.keys():
                if object_property == "solid":
                    # if properties[property] == "True":
                    self.solid = True
                    self.handle_collisions = True
                if object_property == "object_type":
                    self.object_type = properties[object_property]
        self.tile_id = tile_id
        # self.rotate(0)
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
        self.images[key] = {}
        self.images[key][0] = []
        self.images[key][0].append(surface)

    def change_image(self, key):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key]
        self.current_image = self.images[key]
        self.current_key = key
        self.animation_frame = 0
        # self.rotate(0)

    def remove_image(self, key):
        if key in self.images:
            del self.images[key]

    def add_animation(self, key, image_list):
        self.images[key] = {}
        self.images[key][0] = image_list

    def set_animation_frame(self, frame):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key][frame]
        self.animation_frame = frame
        # self.current_image = self.images[key][frame]
        # self.rotate(0)

    def set_animation(self, key, starting_frame=0):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key][starting_frame]
        self.animation_frame = starting_frame
        self.current_animation = key
        # self.current_image = self.images[key][starting_frame]
        self.current_key = key
        # self.rotate(0)

    def next_frame(self, direction=1):
        self.updated = True
        self.updated_sprite = True
        if direction == -1:
            self.animation_frame -= 1
            if self.animation_frame < 0:
                # self.animation_frame = self.images[self.current_animation].__len__()-1
                self.animation_frame = len(self.images[self.current_animation][0])-1
        else:
            self.animation_frame += 1
            if self.animation_frame > len(self.images[self.current_animation][0])-1:
                self.animation_frame = 0
        if self.animation_frame < len(self.images[self.current_animation][0]):
            # self.image = self.images[self.current_animation][self.animation_frame]
            # self.current_image = self.images[self.current_animation][self.animation_frame]
            # self.rotate(0)
            return True
        else:
            return False

    def destroy(self):
        del self
        return True

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def draw(self, surface, position, (x, y)):   # , x_scale, y_scale, x, y):
        # TODO: May need to change image to current_image. Also go through and make sure using right image consistently
        # rect_scaled = pygame.Rect((x-self.rect.x*x_scale, y-self.rect.y*y_scale), (int(self.rect.width*x_scale),
        #                                                                            int(self.rect.height*y_scale)))
        # surface.blit(pygame.transform.scale(self.image, (int(self.image.get_width()*x_scale),
        #                                                  int(self.image.get_height()*y_scale))), rect_scaled
            # print("drawing " + self.object_type)
        key = (surface.x_scale, surface.y_scale)
        try:
            surface.blit(self.images[self.current_key][key][self.animation_frame],
                         (x, y, self.images[self.current_key][key][self.animation_frame].get_width(),
                          self.images[self.current_key][key][self.animation_frame].get_height()))
        except IndexError:
            print(str(self.animation_frame) + " " + str(len(self.images[self.current_key][key])))
        self.updated = False
        self.updated_sprite = False

    def scale_to_view(self, scaling):
        self.updated = True
        # print("Scaling")
        for image_list in self.images.keys():
            self.images[image_list][scaling] = []
            for image in xrange(0, len(self.images[image_list][0])):
                self.images[image_list][scaling].append(pygame.transform.scale(self.images[image_list][0][image],
                    (int(self.images[image_list][0][image].get_width()*scaling[0]),
                     int(self.images[image_list][0][image].get_height()*scaling[1]))))
                # self.images[image_list][0][image][scaling] = pygame.transform.scale(self.images[image_list][image],
                #                                                                  (int(self.images[image_list][image].get_width()*scaling[0]),
                #                                                                   int(self.images[image_list][image].get_height()*scaling[1])))

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

    def update(self, can_update):
        if self.animation_speed > 0:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.frame_ready = True
            if self.frame_ready and can_update:
                self.next_frame(1)
                self.animation_counter = 0
                self.frame_ready = False
