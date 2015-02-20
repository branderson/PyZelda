__author__ = 'brad'

import engine
import pygame

from pygame.locals import *

RESOURCE_DIR = '../resources/'
SPRITE_DIR = RESOURCE_DIR + 'sprite/'
SOUND_DIR = RESOURCE_DIR + 'sound/'


class Link(engine.GameObject):
    def __init__(self, layer=0):
        self.resource_manager = engine.ResourceManager()
        link_sheet = engine.Spritesheet(SPRITE_DIR + "Link.png")

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_down', link_sheet, (32, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_up', link_sheet, (64, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_left', link_sheet, (0, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_right', link_sheet, (96, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_down', link_sheet, (32, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_up', link_sheet, (64, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_left', link_sheet, (0, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_right', link_sheet, (96, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_down', link_sheet, (32, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_up', link_sheet, (64, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_left', link_sheet, (0, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # These two might be messed up
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_right', link_sheet, (96, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_down', link_sheet, (32, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # Needs to be fixed
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_up', link_sheet, (64, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_left', link_sheet, (0, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # Take a look at black spot
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_right', link_sheet, (96, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_hop_down', link_sheet, (0, 64), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_fall', link_sheet, (0, 96), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        engine.GameObject.__init__(self, self.resource_manager.get_images('link_walk_down'), layer,
                                   collision_rect=pygame.Rect((3, 4), (10, 11)),
                                   handle_collisions=True, object_type="player", persistent=True)

        # Add animations to Link
        self.add_animation('link_walk_up', self.resource_manager.get_images('link_walk_up'))
        self.add_animation('link_walk_down', self.resource_manager.get_images('link_walk_down'))
        self.add_animation('link_walk_right', self.resource_manager.get_images('link_walk_right'))
        self.add_animation('link_walk_left', self.resource_manager.get_images('link_walk_left'))
        self.add_animation('link_push_up', self.resource_manager.get_images('link_push_up'))
        self.add_animation('link_push_down', self.resource_manager.get_images('link_push_down'))
        self.add_animation('link_push_left', self.resource_manager.get_images('link_push_left'))
        self.add_animation('link_push_right', self.resource_manager.get_images('link_push_right'))
        self.add_animation('link_shield_walk_up', self.resource_manager.get_images('link_shield_walk_up'))
        self.add_animation('link_shield_walk_down', self.resource_manager.get_images('link_shield_walk_down'))
        self.add_animation('link_shield_walk_right', self.resource_manager.get_images('link_shield_walk_right'))
        self.add_animation('link_shield_walk_left', self.resource_manager.get_images('link_shield_walk_left'))
        self.add_animation('link_use_shield_up', self.resource_manager.get_images('link_use_shield_up'))
        self.add_animation('link_use_shield_down', self.resource_manager.get_images('link_use_shield_down'))
        self.add_animation('link_use_shield_left', self.resource_manager.get_images('link_use_shield_left'))
        self.add_animation('link_use_shield_right', self.resource_manager.get_images('link_use_shield_right'))
        self.add_animation('link_hop_down', self.resource_manager.get_images('link_hop_down'))
        self.add_animation('link_fall', self.resource_manager.get_images('link_fall'))

        # Group animations
        self.link_walk = ["link_walk_right", "link_walk_up", "link_walk_left", "link_walk_down"]
        self.link_push = ["link_push_right", "link_push_up", "link_push_left", "link_push_down"]
        self.link_shield_walk = ["link_shield_walk_right", "link_shield_walk_up", "link_shield_walk_left", "link_shield_walk_down"]
        self.link_use_shield = ["link_use_shield_right", "link_use_shield_up", "link_use_shield_left", "link_use_shield_down"]

        # Add sounds to Link
        self.resource_manager.add_sound('link_hop', SOUND_DIR + 'LA_Link_Jump.wav')
        self.resource_manager.add_sound('link_shield', SOUND_DIR + 'LA_Shield.wav')
        self.resource_manager.add_sound('link_fall', SOUND_DIR + 'LA_Fall.wav')

        # Configure Link's properties
        self.speed = 1.25  # 1.25
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}
        self.direction = 3
        self.facing = 3
        self.moves = []
        self.change_animation = False
        self.shield = False
        self.left = None
        self.right = None
        self.state = "walking"
        self.hop_frame = 0
        self.controllable = True
        self.no_clip = False
        self.direction_held = False
        self.interaction_rect = None  # self.collision_rect.copy()

        # Link's States
        # self.walk = WalkingState()
        # self.collide = CollidingState()
        # self.shield = ShieldState()
        self._state = WalkingState(self)

    def update_interactions(self):
        if self.facing == 0:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x+self.collision_rect.width,
                                                 self.position[1]+self.collision_rect.y),
                                                (1, self.collision_rect.height))
        elif self.facing == 1:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x,
                                                 self.position[1]+self.collision_rect.y-1),
                                                (self.collision_rect.width, 1))
        elif self.facing == 2:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x-1,
                                                 self.position[1]+self.collision_rect.y),
                                                (1, self.collision_rect.height))
        elif self.facing == 3:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x,
                                                 self.position[1]+self.collision_rect.y+self.collision_rect.height),
                                                (self.collision_rect.width, 1))

    def play_sound(self, key):
        self.resource_manager.play_sound(key)

    def hop(self, moved):
        if self.hop_frame < 3:
            if self.animation_counter >= 7:
                # print(str(self.hop_frame))
                self.next_frame(1)
                self.animation_counter = 0
                self.hop_frame += 1
        else:
            self.set_animation('link_walk_down', 0)
        if not moved:
            self.controllable = True
            # self.hopping = False
            self.state = "walking"
            self.change_animation = True
            self.hop_frame = 0

    def set_speed(self, speed):
        self.speed = speed
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}

    def handle_input(self, game_scene):
        if self._state is not None:
            self._state.handle_input(self, game_scene)
            self.update_interactions()


class WalkingState(engine.ObjectState):
    def __init__(self, link):
        engine.ObjectState.__init__(self)
        # Change animations
        if not link.shield:
            link.set_animation(link.link_walk[link.facing], 0)
        else:
            link.set_animation(link.link_shield_walk[link.facing], 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False

        if key[K_b] and link.shield:
            link.play_sound('link_shield')
            link._state = ShieldState(link)

        # Gather movement directions
        if not key[K_a] and not key[K_d] and not key[K_w] and not key[K_s] and not key[K_b]:
            link.set_animation_frame(0)
        else:
            if key[K_a] and not key[K_d]:
                if not key[K_w] and not key[K_s] and link.facing != 2:
                    link.facing = 2
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 2
                moves.append(2)
                moved = True
            elif key[K_d] and not key[K_a]:
                if not key[K_w] and not key[K_s] and link.facing != 0:
                    link.facing = 0
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 0
                moves.append(0)
                moved = True
            if key[K_s] and not key[K_w]:
                if not key[K_d] and not key[K_a] and link.facing != 3:
                    link.facing = 3
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 3
                moves.append(3)
                moved = True
            elif key[K_w] and not key[K_s]:
                if not key[K_d] and not key[K_a] and link.facing != 1:
                    link.facing = 1
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 1
                moves.append(1)
                moved = True

        # Execute movements
        if moved:
            for move_direction in moves:
                previous_position = link.position
                link.increment(link.movement[move_direction])
                for game_object in game_scene.check_object_collision_objects(link):
                    # Regular collisions, stop movement
                    if game_object.solid and not link.no_clip:
                        link.move(previous_position)
                        link._state = CollidingState(link)

                    # Stairs
                    if "slow" in game_object.properties:
                        link.set_speed(float(game_object.properties["slow"]))
                    else:
                        link.set_speed(float(1.25))

            link.update()

    def update(self, link):
        pass


class CollidingState(engine.ObjectState):
    def __init__(self, link):
        engine.ObjectState.__init__(self)
        link.set_animation(link.link_push[link.facing], 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False

        if key[K_a] and not key[K_d]:
            if not key[K_w] and not key[K_s] and link.facing != 2:
                link.facing = 2
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 2
            moves.append(2)
            moved = True
        elif key[K_d] and not key[K_a]:
            if not key[K_w] and not key[K_s] and link.facing != 0:
                link.facing = 0
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 0
            moves.append(0)
            moved = True
        if key[K_s] and not key[K_w]:
            if not key[K_d] and not key[K_a] and link.facing != 3:
                link.facing = 3
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 3
            moves.append(3)
            moved = True
        elif key[K_w] and not key[K_s]:
            if not key[K_d] and not key[K_a] and link.facing != 1:
                link.facing = 1
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 1
            moves.append(1)
            moved = True

        not_colliding_any = True
        if moved:
            for move_direction in moves:
                not_colliding_direction = True
                previous_position = link.position
                link.increment(link.movement[move_direction])
                for game_object in game_scene.check_object_collision_objects(link):
                    # Regular collisions, stop movement
                    if game_object.solid and not link.no_clip:
                        not_colliding_direction = False
                        not_colliding_any = False

                    # Stairs
                    if "slow" in game_object.properties:
                        link.set_speed(float(game_object.properties["slow"]))
                    else:
                        link.set_speed(float(1.25))

                if not not_colliding_direction:
                    link.move(previous_position)
            link.update()
        if not_colliding_any:
            link._state = WalkingState(link)

    def update(self, game_object):
        pass


class HoppingState(engine.ObjectState):
    def __init__(self):
        engine.ObjectState.__init__(self)

    def handle_input(self, game_object):
        pass

    def update(self, game_object):
        pass


class SlippingState(engine.ObjectState):
    def __init__(self):
        engine.ObjectState.__init__(self)

    def handle_input(self, game_object):
        pass

    def update(self, game_object):
        pass


class FallingState(engine.ObjectState):
    def __init__(self):
        engine.ObjectState.__init__(self)

    def handle_input(self, game_object):
        pass

    def update(self, game_object):
        pass


class ShieldState(engine.ObjectState):
    def __init__(self, link):
        engine.ObjectState.__init__(self)
        link.set_animation(link.link_use_shield[link.facing], 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        if not key[K_b]:
            link._state = WalkingState(link)

    def update(self, game_object):
        pass