__author__ = 'brad'

import pygame
from resourceman import ResourceManager
from spritesheet import Spritesheet
from gameobject import GameObject
import xml.etree.ElementTree as ET


class Map(object):
    def __init__(self, filename, tile_set):
        """Takes an XML world file and a tile set and creates a map from it"""
        # Load the tile set
        self.resource_manager = ResourceManager()
        self.tile_set = Spritesheet(tile_set)  # Could eventually allow for multiple tile sets by making a list
        self.resource_manager.add_spritesheet_strip_offsets('tile_set', self.tile_set, (1, 1), 600, 24, (16, 16), 1, 1)

        # Read the XML file
        tree = ET.parse(filename)
        root = tree.getroot()
        self.width = int(root.get("width"))
        self.height = int(root.get("height"))
        self.tile_width = int(root.get("tilewidth"))
        self.tile_height = int(root.get("tileheight"))

        # Read in the layers
        self.layers = {}

        for layer in root.findall("layer"):
            # print(layer.get("name"))
            tile_list = []
            for tile in layer.find("data").findall("tile"):
                # print(tile.get("gid"))
                tile_list.append(int(tile.get("gid")))
            self.layers[layer.get("name")] = tile_list

        # Read in the collision boxes
        self.object_layers = {}

        for layer in root.findall("objectgroup"):
            rect_list = []
            for object_rect in layer.findall("object"):
                try:
                    rect_list.append(pygame.Rect(int(object_rect.get("x")),  # /self.tile_width,
                                                 int(object_rect.get("y")),  # /self.tile_height,
                                                 int(object_rect.get("width")),  # /self.tile_width,
                                                 int(object_rect.get("height"))))  # /self.tile_height))
                except TypeError:
                    print("There was a problem loading object at " + str(int(object_rect.get("x"))/self.tile_width)
                          + ", " + str(int(object_rect.get("y"))/self.tile_height))
            self.object_layers[layer.get("name")] = rect_list

    def get_tile_index(self, layer_name, x_tile, y_tile):
        index = self.width*y_tile+x_tile
        try:
            return self.layers[layer_name][index]-1
        except IndexError:
            return 0

    def build_world(self, scene, view_rect=None):
        # This will be deprecated shortly
        # print("Starting build")
        self.clear_collisions(scene)
        objects = 0
        tiles = 0
        if view_rect is None:
            row = 0
            for layer_name in self.layers.keys():
                while row < self.height:
                    for tile in xrange(0, self.width):
                        current_tile = self.get_tile_index(layer_name, tile, row)
                        if current_tile != -1:
                            scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                           [current_tile], -1000, object_type=layer_name),
                                                (16*tile, 16*row))
                        # print(str(row) + " " + str(tile))
                    row += 1
        else:
            tile_rect = (view_rect.x/self.tile_width, view_rect.y/self.tile_height,
                         view_rect.width/self.tile_width, view_rect.height/self.tile_height)

            # print(str(view_rect[0]) + " " + str(view_rect[1]) + " " + str(view_rect[2]) + " " + str(view_rect[3]))

            # Build the map tiles
            for layer_name in self.layers.keys():
                row = 0
                while row < tile_rect[3]:
                    for tile in xrange(0, tile_rect[2]):
                        current_tile = self.get_tile_index(layer_name, tile_rect[0]+tile, tile_rect[1]+row)
                        if current_tile != -1:
                            # Allow it to determine whether objects already exist and just make them visible if they do
                            scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                           [current_tile], -1000, object_type=layer_name),
                                                (16*(tile_rect[0]+tile), 16*(tile_rect[1]+row)))
                            tiles += 1
                        # print(str(row) + " " + str(tile))
                    row += 1

            # Build the object layers
            for layer_name in self.object_layers.keys():
                for object_rect in self.object_layers[layer_name]:
                    if object_rect.colliderect(view_rect):  # tile_rect):
                        scene.insert_object(GameObject(collision_rect=pygame.Rect(0, 0, object_rect[2], object_rect[3]),
                                                       handle_collisions=True, object_type=layer_name, visible=False),
                                            (object_rect[0], object_rect[1]))
                        objects += 1
        # print("Added " + str(tiles) + " tiles")
        # print("Added " + str(objects) + " objects")
        # print("Ending build")

    @staticmethod
    def clear_tiles(scene, view_rect, kill_all=False):
        # print("Starting to clear tiles")
        # handle_all_collisions = scene.handle_all_collisions
        # scene.handle_all_collisions = True
        # scene.update_collisions()
        # scene.handle_all_collisions = handle_all_collisions
        objects = 0
        for coordinate in scene.coordinate_array.keys():
            for game_object in scene.coordinate_array[coordinate]:
                if game_object.object_type == "Map Tiles":
                    object_rect = pygame.Rect(scene.check_position(game_object), (game_object.rect.width,
                                                                                  game_object.rect.height))
                    # try:
                    #     object_rect = scene.collision_array[game_object]
                    # except KeyError:
                    #     print("an object failed to clear")
                    if not object_rect.colliderect(view_rect):
                        if kill_all:
                            scene.remove_object(game_object)
                        else:
                            game_object.visible = False
                    objects += 1
        # scene.update_collisions()
        # print("There were " + str(objects) + " tiles")
        # print("Ending clear tiles")

    @staticmethod
    def clear_collisions(scene, kill_all=False):
        # print("Starting to clear objects")
        objects = 0
        for coordinate in scene.coordinate_array.keys():
            for game_object in scene.coordinate_array[coordinate]:
                if not game_object.persistent and game_object.object_type != "Map Tiles":
                    scene.remove_object(game_object)
                objects += 1
        # print("There were " + str(objects) + " objects")
        # print("Ending clear objects")