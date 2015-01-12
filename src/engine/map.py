__author__ = 'brad'

import pygame
from resourceman import ResourceManager
from spritesheet import Spritesheet
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
        self.width = root.get("width")
        print(str(self.width))
        self.height = root.get("height")
        print(str(self.height))
        self.tile_width = root.get("tilewidth")
        self.tile_height = root.get("tileheight")
        print(str(self.tile_width) + " " + str(self.tile_height))
        xml_counter = 0

        # for