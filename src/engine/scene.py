__author__ = 'brad'

import pygame
import math
from coordsurface import CoordinateSurface


class Scene(object):
    def __init__(self, scene_size, update_all=False, handle_all_collisions=False):
        self.coordinate_array = {}
        self.collision_array = {}
        self.views = {}
        self.view_rects = {}
        self.view_draw_positions = {}
        self.view_update_values = {}
        self.active = True
        self.scene_width = scene_size[0]
        self.scene_height = scene_size[1]
        self.update_all = update_all
        self.handle_all_collisions = handle_all_collisions

    def insert_view(self, surface, key, view_scene_position, view_draw_position=None, fill=None, masks=None,
                    view_size=None):
        if view_size is None:
            view_size = (surface.coordinate_width, surface.coordinate_height)
        self.views[key] = surface
        self.view_rects[key] = pygame.Rect(view_scene_position, view_size)
        if view_draw_position is None:
            self.view_draw_positions[key] = (0, 0)
        else:
            self.view_draw_positions[key] = view_draw_position
        self.view_update_values[key] = (fill, masks)

    def remove_view(self, key):
        if key in self.views:
            del self.views[key]
            del self.view_rects[key]
            del self.view_draw_positions[key]
            del self.view_update_values[key]

    def pan_view(self, key, increment):
        self.view_rects[key].x += increment[0]
        self.view_rects[key].y += increment[1]

    def move_view(self, key, coordinate):
        self.view_rects[key].topleft = coordinate

    def center_view_on_object(self, key, game_object):
        current_view = self.view_rects[key]
        self.view_rects[key] = pygame.Rect((self.check_position(game_object)[0] -
                                            current_view.width/2 +
                                            game_object.rect.width/2,
                                            self.check_position(game_object)[1] -
                                            current_view.height/2 + game_object.rect.height/2),
                                           (current_view.width,
                                            current_view.height))

    def insert_object(self, game_object, coordinate):
        game_object.updated = True
        if coordinate[0] > self.scene_width or coordinate[1] > self.scene_height:
            return False
        if coordinate in self.coordinate_array:
            self.coordinate_array[coordinate].append(game_object)
        else:
            self.coordinate_array[coordinate] = [game_object]
        game_object.position = coordinate
        self.update_collisions()
        return True

    def insert_object_centered(self, game_object, coordinate):
        adjusted_x = coordinate[0] - game_object.rect.centerx
        adjusted_y = coordinate[1] - game_object.rect.centery
        self.insert_object(game_object, (adjusted_x, adjusted_y))

    def remove_object(self, game_object):
        self.coordinate_array[game_object.position].remove(game_object)
        del game_object
        # game_object.destroy()
        # for key in self.coordinate_array.keys():
        #     # for view in self.views.keys():
        #     #     if self.views[view].check_position(game_object) is not None:
        #     #         self.views[view].remove_object(game_object)
        #     if self.coordinate_array[key].count(game_object) > 0:
        #         self.coordinate_array[key].remove(game_object)
        #         if self.coordinate_array[key] == 0:
        #             del self.coordinate_array[key]
        #         try:
        #             game_object.delete()
        #         except:
        #             pass
        #         self.update_collisions()
        #         return True
        # return False

    def clear(self, key=0):
        # TODO: Make default value clear all views, also switch to view.clear()
        for coordinate in self.coordinate_array.keys():
            del self.coordinate_array[coordinate]
        for game_object in self.coordinate_array.keys():
            if self.views[key].checkPosition(game_object) is not None:
                self.views[key].remove_object(game_object)
        self.update_collisions()

    def check_collision(self, coordinate, game_object=None):
        """Checks if any object at position, or if game_object at position"""
        if game_object is None:
            for rect in self.collision_array.viewitems():
                if rect.collidepoint(coordinate):
                    return True
                else:
                    return False
        else:
            if game_object in self.collision_array:
                if self.collision_array[game_object].collidepoint(coordinate):
                    return True
            return False

    def check_collision_objects(self, coordinate):
        """Returns a list of game objects at position"""
        object_list = []
        for game_object in self.collision_array:
            if self.collision_array[game_object].collidepoint(coordinate):
                object_list.append(game_object)
        return object_list

    def check_object_collision_objects(self, game_object):
        """Returns a list of game objects that collide with object"""
        object_list = []
        for test_object in self.collision_array:
            if self.collision_array[game_object].colliderect(self.collision_array[test_object]):
                object_list.append(test_object)
        return object_list

    def check_object_collision(self, game_object1, game_object2):
        """Checks whether two objects collide"""
        # TODO: Add exception if KeyError
        if self.collision_array[game_object1].colliderect(self.collision_array[game_object2]):
            return True
        else:
            return False

    def check_contain_object(self, game_object1, game_object2):
        """Checks whether game_object1 totally contains game_object2"""
        if not self.collision_array[game_object1].collidepoint(self.collision_array[game_object2].topleft):
            return False
        if not self.collision_array[game_object1].collidepoint(self.collision_array[game_object2].topright):
            return False
        if not self.collision_array[game_object1].collidepoint(self.collision_array[game_object2].bottomleft):
            return False
        if not self.collision_array[game_object1].collidepoint(self.collision_array[game_object2].bottomright):
            return False
        else:
            return True

    def move_object(self, game_object, coordinate):
        game_object.updated = True
        position = game_object.position
        # handle_all_collisions = self.handle_all_collisions
        # self.handle_all_collisions = True
        # self.update_collisions()
        # self.handle_all_collisions = handle_all_collisions
        for object_coordinate in self.coordinate_array.keys():
            for other_object in self.coordinate_array[object_coordinate]:
                moved_object_rect = pygame.Rect(position, (game_object.rect.width, game_object.rect.height))
                other_object_rect = pygame.Rect(other_object.position,
                                                (other_object.rect.width,
                                                 other_object.rect.height))
                if other_object_rect.colliderect(moved_object_rect):
                    other_object.updated = True
        if position is not None:
            if coordinate in self.coordinate_array:
                self.coordinate_array[coordinate].append(game_object)
            else:
                self.coordinate_array[coordinate] = [game_object]
            if len(self.coordinate_array[position]) == 0:
                del self.coordinate_array[position]
            self.coordinate_array[position].remove(game_object)
            # for other_object in self.check_collision_objects(coordinate):
            #     other_object.updated = True
            game_object.position = coordinate
            self.update_collisions()
            return True
        else:
            return False

    def increment_object(self, game_object, increment):
        return self.move_object(game_object, (game_object.position[0] + increment[0],
                                              game_object.position[1] + increment[1]))

    def increment_object_radial(self, game_object, increment):
        x_increment = math.cos(math.radians(game_object.angle))*increment
        y_increment = math.sin(math.radians(game_object.angle))*increment
        return self.increment_object(game_object, (x_increment, y_increment))

    @staticmethod
    def check_position(game_object):
        # for key in self.coordinate_array.keys():
        #     if self.coordinate_array[key].count(game_object) > 0:
        #         return key
        return game_object.position
        # return None

    def update(self, key=0, fill=None, masks=None):
        # TODO: Make default key update all views
        self.views[key].clear()
        update_collisions = False
        remove_keys = []
        for coordinate in self.coordinate_array.keys():
            if not self.coordinate_array[coordinate]:
                remove_keys.append(coordinate)
        for coordinate in remove_keys:
            self.coordinate_array.pop(coordinate)
        # print(str(len(self.coordinate_array.keys())))
        for coordinate in self.coordinate_array.keys():
            for game_object in self.coordinate_array[coordinate]:
                if game_object.updated_sprite:
                    update_collisions = True
        if update_collisions:
            self.update_collisions()
        for coordinate in self.coordinate_array.keys():
            for game_object in self.coordinate_array[coordinate]:
                add_object = False
                object_rect = pygame.Rect(self.check_position(game_object), (game_object.rect.width,
                                                                             game_object.rect.height))
                # self.collision_array[game_object] = object_rect
                if self.view_rects[key].colliderect(object_rect) and game_object.visible:
                    if masks is None:
                        add_object = True
                    else:
                        for mask in masks:
                            if game_object.masks.count(mask) != 0:
                                add_object = True
                    if add_object and self.views[key].active:
                        if game_object.updated:
                            # if game_object.updated_sprite:
                            game_object.rect = pygame.Rect((0, 0), (game_object.images[game_object.current_key][0]
                                                                    [game_object.animation_frame].get_width(),
                                                                    game_object.images[game_object.current_key][0]
                                                                    [game_object.animation_frame].get_height()))
                            # handle_all_collisions = self.handle_all_collisions
                            # self.handle_all_collisions = True
                            # self.update_collisions()
                            # self.handle_all_collisions = handle_all_collisions
                            for object_coordinate in self.coordinate_array.keys():
                                for other_object in self.coordinate_array[object_coordinate]:
                                    collide_object_rect = pygame.Rect(game_object.position,
                                                                      (game_object.rect.width,
                                                                       game_object.rect.height))
                                    other_object_rect = pygame.Rect(other_object.position,
                                                                    (other_object.rect.width,
                                                                     other_object.rect.height))
                                    # if self.collision_array[other_object].colliderect(collide_object_rect):
                                    if other_object_rect.colliderect(collide_object_rect):
                                        other_object.updated = True
                                    #     if other_object.object_type == "half_post":
                                    #         print("Half post updated")
                            # self.update_collisions()
                        if self.update_all:
                            game_object.updated = True
                        self.views[key].insert_object(game_object, (self.check_position(game_object)[0] -
                                                                    self.view_rects[key].x,
                                                                    self.check_position(game_object)[1] -
                                                                    self.view_rects[key].y))
        self.views[key].update(fill, masks)

    def update_collisions(self):
        self.collision_array = {}
        # objects = []
        for key in self.coordinate_array.keys():
            for game_object in self.coordinate_array[key]:
                # objects.append(game_object)
                if (game_object.handle_collisions or self.handle_all_collisions):  # and game_object.updated:
                    # collide_rect = pygame.Rect((self.check_position(game_object)[0] + game_object.rect.width/2 -
                    #                             game_object.collision_rect.width/2, self.check_position(game_object)[1] +
                    #                             game_object.rect.height/2 - game_object.collision_rect.height/2),
                    #                            (game_object.collision_rect.width,
                    #                             game_object.collision_rect.height))
                    collide_rect = pygame.Rect((game_object.position[0]+game_object.collision_rect.x,
                                                game_object.position[1]+game_object.collision_rect.y),
                                               (game_object.collision_rect.width, game_object.collision_rect.height))
                    self.collision_array[game_object] = collide_rect
        # remove_objects = []
        # for game_object in self.collision_array.keys():
        #     in_objects = False
        #     for test_object in objects:
        #         if game_object == test_object:
        #             in_objects = True
        #     if not in_objects:
        #         remove_objects.append(game_object)
        # for game_object in remove_objects:
        #     self.collision_array.pop(game_object)

    def update_screen_coordinates(self, key, new_size):
        self.views[key].update_screen_coordinates(new_size)

    def update_objects(self):
        for view in self.views:
            view.update_objects()