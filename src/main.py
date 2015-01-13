#!/usr/bin/env python
__author__ = 'brad'
import sys
import pygame
import engine
import time
from link import Link

from pygame.locals import *

# Screen constants
COORDINATE_WIDTH = 160
COORDINATE_HEIGHT = 128
SCREEN_MULTIPLIER = 3
SCREEN_WIDTH = COORDINATE_WIDTH*SCREEN_MULTIPLIER  # 640  # 480
SCREEN_HEIGHT = (COORDINATE_HEIGHT+16)*SCREEN_MULTIPLIER  # 576  # 432
# Clock constants
TICKS_PER_SECOND = 60.
MAX_FPS = 60
USE_WAIT = True
MAX_FRAME_SKIP = 5
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK,
                  lambda: time.time())
# lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
RESOURCE_DIR = '../resources/'
GUI_MASK = ['gui']
GAME_MASK = ['game']


def main():
    global screen, game_state, game_surface, gui_surface, resource_manager, clock, \
        game_scene, current_width, current_state, pause_state, pause_scene, game_map
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state = engine.State()
    pause_state = engine.State()

    game_surface = engine.CoordinateSurface((SCREEN_WIDTH, (SCREEN_HEIGHT/COORDINATE_HEIGHT)*COORDINATE_HEIGHT),
                                            (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, (SCREEN_HEIGHT/COORDINATE_HEIGHT)*16)),
                                           (COORDINATE_WIDTH, 16))

    game_scene = engine.Scene((2560, 2480))
    pause_scene = engine.Scene((COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_state.add_scene('game', game_scene)
    pause_state.add_scene('pause', pause_scene)
    current_state = game_state
    game_scene.insert_view(game_surface, 'game_view', (0, 0))
    pause_scene.insert_view(pause_surface, 'pause_view', (0, 0), (0, 0), (0, 0, 0, 0))
    current_width = 480

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    link_sheet = engine.Spritesheet(RESOURCE_DIR + "LinkSheet6464192.png")
    overworld_sheet = engine.Spritesheet(RESOURCE_DIR + "OverworldSheet.png")
    resource_manager = engine.ResourceManager()
    resource_manager.add_spritesheet_image('link', link_sheet, ((45, 80), (16, 16)), (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_down', link_sheet, (37, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_up', link_sheet, (66, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_left', link_sheet, (5, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_right', link_sheet, (95, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_push_down', link_sheet, (56, 57), 2, 2, (15, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_push_up', link_sheet, (88, 57), 2, 2, (17, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_push_left', link_sheet, (21, 57), 2, 2, (16, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_push_right', link_sheet, (122, 57), 2, 2, (16, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)

    resource_manager.add_font('gui_font_small', RESOURCE_DIR + "ReturnofGanon.ttf", 20)
    resource_manager.add_font('gui_font_large', RESOURCE_DIR + "ReturnofGanon.ttf", 46)

    game_map = engine.Map(RESOURCE_DIR + 'worlds/grassworldtmx', RESOURCE_DIR + 'OverworldSheet.png')

    while True:
        if not run_game():
            break


def run_game():
    global link, camera, camera_movement, \
        link_movement, room_movement, var, game_map
    var = {'game_ticks': 0, 'can_move': True, 'move_camera': False, 'camera_increment': 0,
           'clear_previous': False}

    camera_movement = {0: (COORDINATE_WIDTH/32, 0), 1: (0, -COORDINATE_HEIGHT/32),  # What the fuck???
                       2: (-COORDINATE_WIDTH/32, 0), 3: (0, COORDINATE_HEIGHT/32)}
    link_movement = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}
    room_movement = {0: (.5, 0), 1: (0, -.5), 2: (-.5, 0), 3: (0, .5)}

    link = Link(resource_manager.get_images('link'), 0)
    camera = engine.GameObject(collision_rect=(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT))),
                               handle_collisions=True, object_type="camera")
    camera.collision_rect.center = camera.rect.center

    link.add_animation('link_walk_up', resource_manager.get_images('link_walk_up'))
    link.add_animation('link_walk_down', resource_manager.get_images('link_walk_down'))
    link.add_animation('link_walk_right', resource_manager.get_images('link_walk_right'))
    link.add_animation('link_walk_left', resource_manager.get_images('link_walk_left'))
    link.add_animation('link_push_up', resource_manager.get_images('link_push_up'))
    link.add_animation('link_push_down', resource_manager.get_images('link_push_down'))
    link.add_animation('link_push_left', resource_manager.get_images('link_push_left'))
    link.add_animation('link_push_right', resource_manager.get_images('link_push_right'))
    link.set_animation('link_walk_down')

    game_scene.insert_object_centered(link, (80, 1984))
    game_scene.insert_object_centered(camera, (80, 1984))
    current_state.update_collisions()
    game_scene.center_view_on_object('game_view', camera)
    game_map.build_world(game_scene, game_scene.view_rects['game_view'])

    # Game loop
    while True:
        clock.tick()
        if clock.update_ready:
            update_clock()
            update_logic()

        if clock.frame_ready:
            # Draw functions
            draw_game()

            # Update display
            pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            handle_event(event)

        pygame.display.set_caption("FPS: " + str(clock.fps))


def update_clock():
        """Update function for use with GameClock."""
        global var, clock

        # sprite_group.clear(screen)  # , eraser_image)
        # sprite_group.update(USE_PREDICTION)
        # handle_collisions()
        var['game_ticks'] += 1
        if var['game_ticks'] >= clock.ticks_per_second:
            # set_caption()
            var['game_ticks'] = 0


def update_logic():
    global camera_movement, link_movement, room_movement, \
        var
    current_state.update_collisions()
    if current_state == game_state:
        game_scene.center_view_on_object('game_view', camera)
        link.animation_counter += 1

        if var['clear_previous']:
            var['clear_previous'] = False
            game_map.clear_world(game_scene, game_scene.view_rects['game_view'])
        if var['can_move']:
            update_room()
        if var['move_camera']:
            move_camera()


def draw_game():
    current_state.update()
    screen.fill((0, 0, 0, 0))
    for scene_key in current_state.scenes.keys():  # Draws each scene in the current state to the screen
        if current_state.scenes[scene_key].active:
            for surface_key in current_state.scenes[scene_key].views.keys():
                surface = current_state.scenes[scene_key].views[surface_key]
                if surface.active:
                    screen.blit(surface.draw(), current_state.scenes[scene_key].view_draw_positions[surface_key])
    if current_state == pause_state:
        message = resource_manager.fonts['default'].render("PAUSE", True, (255, 255, 255, 255))
        screen.blit(message, (SCREEN_WIDTH/2-message.get_rect().width/2, SCREEN_HEIGHT/2-message.get_rect().height/2))
    draw_gui()
    screen.blit(gui_surface, (0, SCREEN_HEIGHT-(SCREEN_HEIGHT/COORDINATE_HEIGHT)*16))
    return


def draw_gui():
    gui_surface.fill((215, 160, 160, 255))
    text_b = resource_manager.fonts['gui_font_small'].render("B", False, (0, 0, 0, 255))
    text_a = resource_manager.fonts['gui_font_small'].render("A", False, (0, 0, 0, 255))
    text_brackets = resource_manager.fonts['gui_font_large'].render("[    ]", False, (0, 0, 0, 255))
    gui_surface.blit(text_b, (3, 3))
    gui_surface.blit(text_brackets, (19, 3))
    gui_surface.blit(text_a, (120, 3))
    gui_surface.blit(text_brackets, (136, 3))


def handle_event(event):
    global current_state, screen, player_var, var
    # Quit the game
    if event.type == KEYDOWN:
        key = event.key
        if key == K_w and link.facing != 1 and var['can_move']:
            link.facing = 1
            link.change_animation = True
        elif key == K_s and link.facing != 3 and var['can_move']:
            link.facing = 3
            link.change_animation = True
        elif key == K_d and link.facing != 0 and var['can_move']:
            link.facing = 0
            link.change_animation = True
        elif key == K_a and link.facing != 2 and var['can_move']:
            link.facing = 2
            link.change_animation = True
        if key == K_TAB:
            if current_state == game_state:
                current_state = pause_state
            else:
                current_state = game_state
        if key == K_ESCAPE:
            terminate()
        if key == K_r:
            game_scene.update_screen_coordinates('game_view', (640, 576))
            screen = pygame.display.set_mode((640, 576))
        if key == K_t:
            game_scene.update_screen_coordinates('game_view', (480, 432))
            screen = pygame.display.set_mode((480, 432))
        if key == K_f:
            pygame.display.toggle_fullscreen()
    return


def load_room():
    global var, game_scene, game_map
    if link.direction == 0:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] += var['camera_increment']
        game_map.build_world(game_scene, new_rect)
    if link.direction == 1:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect)
    if link.direction == 2:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect)
    if link.direction == 3:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] += var['camera_increment']
        game_map.build_world(game_scene, new_rect)


def update_room():
    update_player()


def update_player():
    global var
    # Make link not turn if new button pressed

    moved = False

    # Move link if keys are pressed
    key = pygame.key.get_pressed()
    previous_position = link.position
    if key[K_a] and not key[K_d]:
        if not key[K_w] and not key[K_s] and link.facing != 2:
            link.facing = 2
            link.change_animation = True
        link.direction = 2
        game_scene.increment_object(link, link_movement[link.direction])
        moved = True
    elif key[K_d] and not key[K_a]:
        if not key[K_w] and not key[K_s] and link.facing != 0:
            link.facing = 0
            link.change_animation = True
        link.direction = 0
        game_scene.increment_object(link, link_movement[link.direction])
        moved = True
    if key[K_s] and not key[K_w]:
        if not key[K_d] and not key[K_a] and link.facing != 3:
            link.facing = 3
            link.change_animation = True
        link.direction = 3
        game_scene.increment_object(link, link_movement[link.direction])
        moved = True
    elif key[K_w] and not key[K_s]:
        if not key[K_d] and not key[K_a] and link.facing != 1:
            link.facing = 1
            link.change_animation = True
        link.direction = 1
        game_scene.increment_object(link, link_movement[link.direction])
        moved = True
    if moved:
        not_colliding = True
        for game_object in game_scene.check_object_collision_objects(link):
            if game_object.object_type == "Regular Collisions":
                if not link.colliding:
                    link.colliding = True
                    link.change_animation = True
                not_colliding = False
                game_scene.move_object(link, previous_position)
        if not_colliding:
            if link.colliding:
                link.colliding = False
                link.change_animation = True
    if moved and link.animation_counter >= 4:
        link.next_frame(1)
        link.animation_counter = 0

    # Check for collision with edge of screen
    if camera.position[0] - link.position[0] > COORDINATE_WIDTH/2:
        link.direction = 2
        var['camera_increment'] = COORDINATE_WIDTH
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif link.position[0]+link.rect.width - camera.position[0] > COORDINATE_WIDTH/2:
        link.direction = 0
        var['camera_increment'] = COORDINATE_WIDTH
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif camera.position[1] - link.position[1] > COORDINATE_HEIGHT/2:
        link.direction = 1
        var['camera_increment'] = COORDINATE_HEIGHT
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif link.position[1]+link.rect.height - camera.position[1] > COORDINATE_HEIGHT/2:
        link.direction = 3
        var['camera_increment'] = COORDINATE_HEIGHT
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return

    # Handle animations
    if link.change_animation:  # Later if walking
        if link.facing == 0:
            if link.colliding:
                link.set_animation('link_push_right', 0)
            else:
                link.set_animation('link_walk_right', 0)
        elif link.facing == 1:
            if link.colliding:
                link.set_animation('link_push_up', 0)
            else:
                link.set_animation('link_walk_up', 0)
        elif link.facing == 2:
            if link.colliding:
                link.set_animation('link_push_left', 0)
            else:
                link.set_animation('link_walk_left', 0)
        elif link.facing == 3:
            if link.colliding:
                link.set_animation('link_push_down', 0)
            else:
                link.set_animation('link_walk_down', 0)
        link.change_animation = False


def move_camera():
    if var['camera_increment'] > 0:
        game_scene.increment_object(camera, camera_movement[link.direction])
        # print(str(camera_movement[player_var['direction']][1]))
        game_scene.increment_object(link, room_movement[link.direction])
        if link.direction == 1 or link.direction == 3:
            var['camera_increment'] -= abs(camera_movement[link.direction][1])
        else:
            var['camera_increment'] -= abs(camera_movement[link.direction][0])
    else:
        var['move_camera'] = False
        var['can_move'] = True
        var['clear_previous'] = True


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()