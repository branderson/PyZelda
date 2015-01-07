#!/usr/bin/env python
__author__ = 'brad'
import sys
import pygame
import engine
import random

from pygame.locals import *

# Screen constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 320
COORDINATE_WIDTH = 320
COORDINATE_HEIGHT = 320
# Clock constants
TICKS_PER_SECOND = 5.
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
    global screen, game_state, game_surface, background_surface, gui_surface, resource_manager, clock, \
        game_scene, current_width, start_pos, current_state, pause_state, pause_scene
    pygame.init()

    # Set up the window
    states = []
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state = engine.State()
    pause_state = engine.State()
    states.append(game_state)
    game_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT)),
                                            (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    background_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT)),
                                                  (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                           (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    start_pos = (COORDINATE_WIDTH/2, COORDINATE_HEIGHT/2)
    game_scene = engine.Scene((COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_scene = engine.Scene((COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_state.add_scene('game', game_scene)
    pause_state.add_scene('pause', pause_scene)
    current_state = game_state
    game_scene.insert_view(game_surface, 'game_view', (0, 0), (SCREEN_WIDTH/2-COORDINATE_WIDTH/2,
                                                               SCREEN_HEIGHT/2-COORDINATE_HEIGHT/2), (0, 0, 0, 0))
    pause_scene.insert_view(pause_surface, 'pause_view', (0, 0), (SCREEN_WIDTH/2-COORDINATE_WIDTH/2,
                                                                  SCREEN_HEIGHT/2-COORDINATE_HEIGHT/2), (0, 0, 0, 0))
    current_width = 800

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    resource_manager = engine.ResourceManager()
    resource_manager.add_image('snake', RESOURCE_DIR + 'spr_SnakeNode_1.png')
    resource_manager.add_image('target', RESOURCE_DIR + 'spr_Target_0.png')
    resource_manager.add_image('grid', RESOURCE_DIR + 'bgr_grid.png')
    resource_manager.add_image('pause', RESOURCE_DIR + '256.jpg')
    resource_manager.add_font('default', None, 86)

    while True:
        if not run_game():
            break


def run_game():
    global sprite_group, game_ticks, snakes, target, can_move, direction, add_snake
    sprite_group = pygame.sprite.Group()
    game_ticks = 0
    can_move = False
    add_snake = False
    direction = 0

    snakes = [engine.GameObject(resource_manager.get_images('snake'), 0)]
    target = engine.GameObject(resource_manager.get_images('target'), -10)
    grid = engine.GameObject(resource_manager.get_images('grid'), -100)
    pause = engine.GameObject(resource_manager.get_images('pause'), 1000)

    game_scene.insert_object(snakes[0], start_pos)
    game_scene.insert_object(target, (0, 0))
    pause_scene.insert_object_centered(pause, (COORDINATE_WIDTH/2, COORDINATE_HEIGHT/2))
    current_state.update_collisions()
    for x in xrange(0, COORDINATE_WIDTH/grid.rect.width):
        for y in xrange(0, COORDINATE_HEIGHT/grid.rect.height):
            background_surface.insert_object(engine.GameObject(resource_manager.get_images('grid'), -100),
                                             (x*grid.rect.width, y*grid.rect.height))
    background_surface.update()
    # background_surface.blit(background_surface, (0, 0))
    # background_surface.clear()
    random.seed()
    randomize_target()

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
    global add_snake, can_move
    current_state.update_collisions()
    if current_state == game_state:
        if game_scene.check_object_collision(snakes[0], target):
            randomize_target()
            add_snake = True
        previous_position = game_scene.check_position(snakes[0])
        if direction == 2:
            game_scene.increment_object(snakes[0], (-snakes[0].rect.width, 0))
        elif direction == 0:
            game_scene.increment_object(snakes[0], (snakes[0].rect.width, 0))
        elif direction == 3:
            game_scene.increment_object(snakes[0], (0, snakes[0].rect.height))
        elif direction == 1:
            game_scene.increment_object(snakes[0], (0, -snakes[0].rect.height))
        if game_scene.check_position(snakes[0])[0] > COORDINATE_WIDTH-1:
            game_scene.move_object(snakes[0], (0, game_scene.check_position(snakes[0])[1]))
        elif game_scene.check_position(snakes[0])[0] < 0:
            game_scene.move_object(snakes[0], (COORDINATE_WIDTH-snakes[0].rect.width,
                                               game_scene.check_position(snakes[0])[1]))
        if game_scene.check_position(snakes[0])[1] > COORDINATE_HEIGHT-1:
            game_scene.move_object(snakes[0], (game_scene.check_position(snakes[0])[0], 0))
        elif game_scene.check_position(snakes[0])[1] < 0:
            game_scene.move_object(snakes[0], (game_scene.check_position(snakes[0])[0],
                                               COORDINATE_HEIGHT-snakes[0].rect.height))

        if add_snake:
            insert_snake()
        for snake in snakes:
            if snake != snakes[0]:
                update_position = game_scene.check_position(snake)
                game_scene.move_object(snake, previous_position)
                previous_position = update_position
        for snake1 in snakes:
            for snake2 in snakes:
                if snake1 != snake2 and game_scene.check_object_collision(snake1, snake2):
                    terminate()
        can_move = True


def draw_game():
    current_state.update()
    # gui_surface.update((0, 0, 0, 0))
    if current_state == game_state:
        screen.blit(background_surface, (SCREEN_WIDTH/2-COORDINATE_WIDTH/2, SCREEN_HEIGHT/2-COORDINATE_HEIGHT/2))
    for scene_key in current_state.scenes.keys():  # Draws each scene in the current state to the screen
        if current_state.scenes[scene_key].active:
            for surface_key in current_state.scenes[scene_key].views.keys():
                surface = current_state.scenes[scene_key].views[surface_key]
                if surface.active:
                    screen.blit(surface, current_state.scenes[scene_key].view_draw_positions[surface_key])
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


def randomize_target():
    target_x = int(random.uniform(0, COORDINATE_WIDTH/target.rect.width))
    target_y = int(random.uniform(0, COORDINATE_HEIGHT/target.rect.height))
    game_scene.move_object(target, (target_x*target.rect.width, target_y*target.rect.height))
    for snake in snakes:
        if game_scene.check_object_collision(snake, target):
            randomize_target()


def insert_snake():
    global add_snake
    snakes.append(engine.GameObject(resource_manager.get_images('snake'), 0))
    snake = snakes[snakes.__len__() - 2]
    if direction == 0:
        game_scene.insert_object(snakes[snakes.__len__() - 1],
                                 (game_scene.check_position(snake)[0]-snake.rect.width, game_scene.check_position(snake)[1]))
    elif direction == 1:
        game_scene.insert_object(snakes[snakes.__len__() - 1],
                            (game_scene.check_position(snake)[0], game_scene.check_position(snake)[1]-snake.rect.height))
    elif direction == 2:
        game_scene.insert_object(snakes[snakes.__len__() - 1],
                            (game_scene.check_position(snake)[0]+snake.rect.width, game_scene.check_position(snake)[1]))
    elif direction == 3:
        game_scene.insert_object(snakes[snakes.__len__() - 1],
                            (game_scene.check_position(snake)[0], game_scene.check_position(snake)[1]+snake.rect.height))
    add_snake = False


main()
if __name__ == '__main__':
    main()