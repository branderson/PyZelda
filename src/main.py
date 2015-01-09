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

    game_surface = engine.CoordinateSurface((SCREEN_WIDTH, SCREEN_WIDTH), (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                           (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_scene = engine.Scene((2560, 2480))
    pause_scene = engine.Scene((COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_state.add_scene('game', game_scene)
    pause_state.add_scene('pause', pause_scene)
    current_state = game_state
    game_scene.insert_view(game_surface, 'game_view', (0, 0), (0, 0), (0, 0, 0, 0))
    pause_scene.insert_view(pause_surface, 'pause_view', (0, 0), (0, 0), (0, 0, 0, 0))
    current_width = 480

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    link_sheet = engine.Spritesheet(RESOURCE_DIR + "LinkSheet6464192.png")
    resource_manager = engine.ResourceManager()
    resource_manager.add_image('worldmap', RESOURCE_DIR + 'OverworldFull.png')
    resource_manager.add_spritesheet_image('link', link_sheet, ((46, 82), (13, 15)), (64, 64, 192))

    resource_manager.add_font('default', None, 86)

    while True:
        if not run_game():
            break


def run_game():
    global game_ticks, link, worldmap, can_move, direction
    game_ticks = 0
    can_move = False
    direction = 0

    link = engine.GameObject(resource_manager.get_images('link'), 0)
    worldmap = engine.GameObject(resource_manager.get_images('worldmap'), -1000)

    game_scene.insert_object(link, (1000, 1000))
    game_scene.insert_object(worldmap, (0, 0))
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
        global game_ticks, clock

        # sprite_group.clear(screen)  # , eraser_image)
        # sprite_group.update(USE_PREDICTION)
        # handle_collisions()
        game_ticks += 1
        if game_ticks >= clock.ticks_per_second:
            # set_caption()
            game_ticks = 0


def update_logic():
    global can_move
    current_state.update_collisions()
    if current_state == game_state:
        if direction == 2:
            game_scene.increment_object(link, (-link.rect.width, 0))
        elif direction == 0:
            game_scene.increment_object(link, (link.rect.width, 0))
        elif direction == 3:
            game_scene.increment_object(link, (0, link.rect.height))
        elif direction == 1:
            game_scene.increment_object(link, (0, -link.rect.height))

        can_move = True
        game_scene.center_view_on_object('game_view', link)


def draw_game():
    current_state.update()
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
    global direction, can_move, current_state
    # Quit the game
    if event.type == KEYDOWN:
        key = event.key
        if current_state == game_state:
            if key == K_a and direction != 0 and can_move:
                direction = 2
                can_move = False
            elif key == K_d and direction != 2 and can_move:
                direction = 0
                can_move = False
            elif key == K_s and direction != 1 and can_move:
                direction = 3
                can_move = False
            elif key == K_w and direction != 3 and can_move:
                direction = 1
                can_move = False
        if key == K_TAB:
            if current_state == game_state:
                current_state = pause_state
            else:
                current_state = game_state
        if key == K_ESCAPE:
            terminate()
        if key == K_f:
            pygame.display.toggle_fullscreen()
    return


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()