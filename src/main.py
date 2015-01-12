#!/usr/bin/env python
__author__ = 'brad'
import sys
import pygame
import engine
import random

from pygame.locals import *

# Screen constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 432
COORDINATE_WIDTH = 160
COORDINATE_HEIGHT = 144
# Clock constants
TICKS_PER_SECOND = 60.
MAX_FPS = 60
USE_WAIT = True
MAX_FRAME_SKIP = 5
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK,
                  lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
RESOURCE_DIR = '../resources/'
GUI_MASK = ['gui']
GAME_MASK = ['game']


def main():
    global screen, game_state, game_surface, gui_surface, resource_manager, clock, \
        game_scene, current_width, current_state, pause_state, pause_scene
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state = engine.State()
    pause_state = engine.State()

    game_surface = engine.CoordinateSurface((SCREEN_WIDTH, SCREEN_HEIGHT), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                           (COORDINATE_WIDTH, COORDINATE_HEIGHT))
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
    resource_manager.add_image('worldmap', RESOURCE_DIR + 'OverworldFull.png')
    resource_manager.add_spritesheet_image('link', link_sheet, ((45, 80), (16, 16)), (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_down', link_sheet, (37, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_up', link_sheet, (66, 36), 2, 2, (14, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_left', link_sheet, (5, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('link_walk_right', link_sheet, (95, 36), 2, 2, (15, 16), 0, 0, (64, 64, 192))
    resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)

    resource_manager.add_font('default', None, 86)

    map = engine.Map(RESOURCE_DIR + 'worlds/grassworldtmx', RESOURCE_DIR + 'OverworldSheet.png')

    while True:
        if not run_game():
            break


def run_game():
    global link, worldmap, camera, camera_movement, \
        link_movement, room_movement, var, player_var
    var = {'game_ticks': 0, 'can_move': True, 'move_camera': False, 'camera_increment': 0}
    player_var = {'direction': 3, 'facing': 3, 'previous_direction': None, 'animation_counter': 0,
                  'change_animation': False}

    camera_movement = {0: (COORDINATE_WIDTH/32, 0), 1: (0, -COORDINATE_HEIGHT/36),  # What the fuck???
                       2: (-COORDINATE_WIDTH/32, 0), 3: (0, COORDINATE_HEIGHT/32)}
    link_movement = {0: (1, 0), 1: (0, -1), 2: (-1, 0), 3: (0, 1)}
    room_movement = {0: (.5, 0), 1: (0, -.5), 2: (-.5, 0), 3: (0, .5)}

    link = engine.GameObject(resource_manager.get_images('link'), 0, handle_collisions=True)
    # worldmap = engine.GameObject(resource_manager.get_images('worldmap'), -1000)
    camera = engine.GameObject(collision_rect=(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT))),
                               handle_collisions=True)
    camera.collision_rect.center = camera.rect.center

    link.add_animation('link_walk_up', resource_manager.get_images('link_walk_up'))
    link.add_animation('link_walk_down', resource_manager.get_images('link_walk_down'))
    link.add_animation('link_walk_right', resource_manager.get_images('link_walk_right'))
    link.add_animation('link_walk_left', resource_manager.get_images('link_walk_left'))
    link.set_animation('link_walk_down')

    # Build the world
    world = open(RESOURCE_DIR + "worlds/grassworldtmx.txt")
    row = 0
    tiles = []
    for line in world:
        for tile in line.split(","):
            if tile != '' and tile != '0':
                tiles.append(tile)
    # for line in world:
    #     column = 0
    #     for tile in line.split(","):
    #         # if tile != '' and tile != '0':
    #         try:
    #             print(tile)
    #             game_scene.insert_object(engine.GameObject(resource_manager.get_images('overworld_tiles')[int(tile)],
    #                                                        -1000), (16*column, 16*row))
    #         except ValueError:
    #             break
    #         column += 1
    #     row += 1
    world.close()
    print(tiles)
    row = 0
    column = 0
    for tile in tiles:
        if tile != '\n':
            game_scene.insert_object(engine.GameObject(resource_manager.get_images('overworld_tiles')[int(tile)-1],
                                                       -1000), (16*column, 16*row))
            print(str(row) + " " + str(column))
            column += 1
        else:
            row += 1
            column = 0

    game_scene.insert_object_centered(link, (240, 1976))
    game_scene.insert_object_centered(camera, (240, 1976))
    current_state.update_collisions()

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
        var, player_var
    current_state.update_collisions()
    if current_state == game_state:
        game_scene.center_view_on_object('game_view', camera)
        moved = False
        player_var['animation_counter'] += 1
        if var['can_move']:
            # if not game_scene.check_contain_object(camera, link) and \
            #         player_var['previous_direction'] != player_var['direction']:
            if camera.position[0] - link.position[0] > COORDINATE_WIDTH/2:
                player_var['direction'] = 2
                var['camera_increment'] = COORDINATE_WIDTH
                var['move_camera'] = True
                var['can_move'] = False
                return
            elif link.position[0]+link.rect.width - camera.position[0] > COORDINATE_WIDTH/2:
                player_var['direction'] = 0
                var['camera_increment'] = COORDINATE_WIDTH
                var['move_camera'] = True
                var['can_move'] = False
                return
            elif camera.position[1] - link.position[1] > COORDINATE_HEIGHT/2:
                player_var['direction'] = 1
                var['camera_increment'] = COORDINATE_HEIGHT
                var['move_camera'] = True
                var['can_move'] = False
                return
            elif link.position[1]+link.rect.height - camera.position[1] > COORDINATE_HEIGHT/2:
                player_var['direction'] = 3
                var['camera_increment'] = COORDINATE_HEIGHT
                var['move_camera'] = True
                var['can_move'] = False
                return
                # Pause logic
                # if player_var['direction'] == 1 or player_var['direction'] == 3:
                #     var['camera_increment'] = COORDINATE_HEIGHT
                # else:
                #     var['camera_increment'] = COORDINATE_WIDTH
                # var['move_camera'] = True
                # var['can_move'] = False
                # return
            key = pygame.key.get_pressed()
            if key[K_a] and not key[K_d]:
                if not key[K_w] and not key[K_s] and player_var['facing'] != 2:
                    player_var['facing'] = 2
                    player_var['change_animation'] = True
                player_var['direction'] = 2
                game_scene.increment_object(link, link_movement[player_var['direction']])
                moved = True
            elif key[K_d] and not key[K_a]:
                if not key[K_w] and not key[K_s] and player_var['facing'] != 0:
                    player_var['facing'] = 0
                    player_var['change_animation'] = True
                player_var['direction'] = 0
                game_scene.increment_object(link, link_movement[player_var['direction']])
                moved = True
            if key[K_s] and not key[K_w]:
                if not key[K_d] and not key[K_a] and player_var['facing'] != 3:
                    player_var['facing'] = 3
                    player_var['change_animation'] = True
                player_var['direction'] = 3
                game_scene.increment_object(link, link_movement[player_var['direction']])
                moved = True
            elif key[K_w] and not key[K_s]:
                if not key[K_d] and not key[K_a] and player_var['facing'] != 1:
                    player_var['facing'] = 1
                    player_var['change_animation'] = True
                player_var['direction'] = 1
                game_scene.increment_object(link, link_movement[player_var['direction']])
                moved = True
            if moved and player_var['animation_counter'] >= 4:
                link.next_frame(1)
                player_var['animation_counter'] = 0
                player_var['previous_direction'] = None

            # Handle animations
            if player_var['change_animation']:  # Later if walking
                if player_var['facing'] == 0:
                    link.set_animation('link_walk_right', 0)
                elif player_var['facing'] == 1:
                    link.set_animation('link_walk_up', 0)
                elif player_var['facing'] == 2:
                    link.set_animation('link_walk_left', 0)
                elif player_var['facing'] == 3:
                    link.set_animation('link_walk_down', 0)
                player_var['change_animation'] = False


        if var['move_camera']:
            if var['camera_increment'] > 0:
                game_scene.increment_object(camera, camera_movement[player_var['direction']])
                game_scene.increment_object(link, room_movement[player_var['direction']])
                if player_var['direction'] == 1 or player_var['direction'] == 3:
                    var['camera_increment'] -= COORDINATE_HEIGHT/32
                else:
                    var['camera_increment'] -= COORDINATE_WIDTH/32
            else:
                var['move_camera'] = False
                var['can_move'] = True
                player_var['previous_direction'] = player_var['direction']


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
    # screen.blit(gui_surface, (0, 0))
    return


def handle_event(event):
    global current_state, screen, player_var, var
    # Quit the game
    if event.type == KEYDOWN:
        key = event.key
        if key == K_w and player_var['facing'] != 1 and var['can_move']:
            player_var['facing'] = 1
            player_var['change_animation'] = True
        elif key == K_s and player_var['facing'] != 3 and var['can_move']:
            player_var['facing'] = 3
            player_var['change_animation'] = True
        elif key == K_d and player_var['facing'] != 0 and var['can_move']:
            player_var['facing'] = 0
            player_var['change_animation'] = True
        elif key == K_a and player_var['facing'] != 2 and var['can_move']:
            player_var['facing'] = 2
            player_var['change_animation'] = True
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


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()