#!/usr/bin/env python
__author__ = 'brad'
import sys
import pygame
import engine
import specialtiles
import effects
import gui
from link import Link

from pygame.locals import *

# Screen constants
COORDINATE_WIDTH = 160
COORDINATE_HEIGHT = 128
COORDINATE_SIZE = (COORDINATE_WIDTH, COORDINATE_HEIGHT)
SCREEN_MULTIPLIER = 4
SCREEN_WIDTH = COORDINATE_WIDTH*SCREEN_MULTIPLIER  # 640  # 480
SCREEN_HEIGHT = (COORDINATE_HEIGHT+16)*SCREEN_MULTIPLIER  # 576  # 432
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# Clock constants
TICKS_PER_SECOND = 60.
MAX_FPS = 60  # 60
USE_WAIT = True
MAX_FRAME_SKIP = 0
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (TICKS_PER_SECOND, MAX_FPS, USE_WAIT, MAX_FRAME_SKIP, UPDATE_CALLBACK, FRAME_CALLBACK)
                  # lambda: time.time())
# lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
COLORKEY = (64, 64, 192)
RESOURCE_DIR = '../resources/'
SPRITE_DIR = RESOURCE_DIR + 'sprite/'
SOUND_DIR = RESOURCE_DIR + 'sound/'
MUSIC_DIR = RESOURCE_DIR + 'music/wav/'
FONT_DIR = RESOURCE_DIR + 'font/'
EXTENSION = '.wav'
GUI_MASK = ['gui']
GAME_MASK = ['game']
# Game Constants
TRANSITION_SPEED = 2  # Roughly a 1.5


def main():
    global screen, game_state, game_surface, gui_surface, resource_manager, clock, \
        game_scene, current_width, current_state, pause_state, pause_scene, game_map, overworld_sheet, hud
    # pygame.mixer.pre_init(frequency=44100, size=-8)
    pygame.init()
    pygame.register_quit(has_quit)

    # Set up the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_state = engine.State()
    pause_state = engine.State()

    game_surface = engine.CoordinateSurface((SCREEN_WIDTH, (SCREEN_HEIGHT/COORDINATE_HEIGHT)*COORDINATE_HEIGHT),
                                            (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    pause_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
                                             (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    # gui_surface = engine.CoordinateSurface(pygame.Rect((0, 0), (SCREEN_WIDTH, (SCREEN_HEIGHT/COORDINATE_HEIGHT)*16)),
    #                                        (COORDINATE_WIDTH, 16))
    hud = gui.HUD((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_scene = engine.Scene((2560, 2048))
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

    overworld_sheet = engine.Spritesheet(SPRITE_DIR + "OverworldSheet.png")
    resource_manager = engine.ResourceManager()

    resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)

    resource_manager.add_font('gui_font_small', FONT_DIR + "ReturnofGanon.ttf", 20)
    resource_manager.add_font('gui_font_large', FONT_DIR + "ReturnofGanon.ttf", 46)

    # Music
    resource_manager.add_music('overworld', MUSIC_DIR + '10. Overworld' + EXTENSION)
    resource_manager.add_music('mabe_village', MUSIC_DIR + '11. Mabe Village' + EXTENSION)
    resource_manager.add_music('mysterious_forest', MUSIC_DIR + '16. Mysterious Forest' + EXTENSION)
    resource_manager.play_music('mabe_village')
    # resource_manager.play_music(MUSIC_DIR + '10. Overworld.ogg', 6.3)

    # Sounds

    game_map = engine.Map(RESOURCE_DIR + 'worlds/grassworldtmx', SPRITE_DIR + 'OverworldSheet.png')

    while True:
        if not run_game():
            print("Back in main, breaking and quiting pygame")
            break
    # pygame.quit()
    # Locks up here


def run_game():
    global link, camera, camera_movement, \
        link_movement, room_movement, var, game_map, force_exit, textboxes
    var = {'game_ticks': 0, 'can_move': True, 'move_camera': False, 'camera_increment': 0,
           'clear_previous': False, 'current_frame': 0, 'animation_frames': 0, 'camera_position': (1, 11),
           'short_grass_drawn': False, 'invert': True}

    force_exit = False

    # textbox = gui.TextBox("Mysterious\nForest\n(It's a little\nbit mysterious)", (SCREEN_WIDTH, SCREEN_HEIGHT),
    #                       (COORDINATE_WIDTH, COORDINATE_HEIGHT))
    textboxes = []
    # textboxes.append(textbox)

    link = Link(0)
    camera = engine.GameObject(collision_rect=(pygame.Rect((0, 0), (COORDINATE_WIDTH, COORDINATE_HEIGHT))),
                               handle_collisions=True, object_type="camera", persistent=True)
    camera.collision_rect.center = camera.rect.center

    link.set_animation('link_walk_down')

    camera_movement = {0: (TRANSITION_SPEED*(COORDINATE_WIDTH/32), 0), 1: (0, -TRANSITION_SPEED*(COORDINATE_HEIGHT/32)),
                       2: (-TRANSITION_SPEED*(COORDINATE_WIDTH/32), 0), 3: (0, TRANSITION_SPEED*(COORDINATE_HEIGHT/32))}
    room_movement = {0: (TRANSITION_SPEED*.5, 0), 1: (0, -TRANSITION_SPEED*.5),
                     2: (-TRANSITION_SPEED*.5, 0), 3: (0, TRANSITION_SPEED*.5)}

    game_scene.insert_object_centered(link, (112+COORDINATE_WIDTH*var['camera_position'][0],
                                             80+COORDINATE_HEIGHT*var['camera_position'][1]))
    game_scene.insert_object_centered(camera, (80+COORDINATE_WIDTH*var['camera_position'][0],
                                               64+COORDINATE_HEIGHT*var['camera_position'][1]))
    current_state.update_collisions()
    game_scene.center_view_on_object('game_view', camera)
    game_map.build_world(game_scene, game_scene.view_rects['game_view'])
    build_world()

    # Game loop
    while True:
        if force_exit:
            print("Exit has been forced, ending run_game")
            return False
        clock.tick()
        if clock.update_ready:
            update_clock()
            update_logic()
            resource_manager.update_sound()

        if clock.frame_ready:
            # Draw functions
            draw_game()

            # Update display
            pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            handle_event(event)

        pygame.display.set_caption("FPS: " + str(clock.fps))


def update_clock():
        """Update function for use with GameClock."""
        global var, clock

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
        link.update(0)

        if var['clear_previous']:
            var['clear_previous'] = False
            var['invert'] = True
            game_map.clear_tiles(game_scene, game_scene.view_rects['game_view'], kill_all=True)
            # if not link.hopping:
            if link.state != "hopping":
                link.controllable = True
            game_scene.update_all = False
        if var['can_move']:
            update_room()
        if var['move_camera']:
            move_camera()


def draw_game():
    current_state.update(colorkey=COLORKEY)
    # screen.fill((0, 0, 0, 0))
    draw_gui()
    for scene_key in current_state.scenes.keys():  # Draws each scene in the current state to the screen
        if current_state.scenes[scene_key].active:
            for surface_key in current_state.scenes[scene_key].views.keys():
                surface = current_state.scenes[scene_key].views[surface_key]
                if surface.active:
                    screen.blit(surface.draw(), current_state.scenes[scene_key].view_draw_positions[surface_key])
    if current_state == pause_state:
        message = resource_manager.fonts['default'].render("PAUSE", True, (255, 255, 255, 255))
        screen.blit(message, (SCREEN_WIDTH/2-message.get_rect().width/2, SCREEN_HEIGHT/2-message.get_rect().height/2))
    screen.blit(hud, (0, SCREEN_HEIGHT-(SCREEN_HEIGHT/COORDINATE_HEIGHT)*16))
    return


def draw_gui():
    hud.fill((255, 255, 139, 255))
    text_b = resource_manager.fonts['gui_font_small'].render("B", False, (0, 0, 0, 255))
    text_a = resource_manager.fonts['gui_font_small'].render("A", False, (0, 0, 0, 255))
    text_brackets = resource_manager.fonts['gui_font_large'].render("[    ]", False, (0, 0, 0, 255))
    hud.blit(text_b, (3, 3))
    hud.blit(text_brackets, (19, 3))
    hud.blit(text_a, (120, 3))
    hud.blit(text_brackets, (136, 3))
    for textbox in textboxes:
        textbox.update_text()
        if game_surface.check_position(link)[1] > COORDINATE_HEIGHT/2:
            game_surface.blit(textbox, (8*SCREEN_MULTIPLIER, 8*SCREEN_MULTIPLIER))
        else:
            game_surface.blit(textbox, (8*SCREEN_MULTIPLIER, (COORDINATE_HEIGHT/2+16)*SCREEN_MULTIPLIER))


def handle_event(event):
    global current_state, screen, var, textboxes
    # Quit the game
    if event.type == KEYDOWN:
        key = event.key
        if link.controllable:
            if key == K_SPACE:
                for game_object in game_scene.check_collision_rect_objects(link.interaction_rect):
                    if game_object.object_type == "Signs":
                        link.controllable = False
                        justify = "center"
                        if "justify" in game_object.properties:
                            justify = game_object.properties["justify"]
                        textboxes.append(gui.TextBox(game_object.properties["text"], SCREEN_SIZE, COORDINATE_SIZE, justify))
            elif key == K_g:
                link.shield = not link.shield
                if link.shield:
                    link.set_animation(link.link_shield_walk[link.facing], 0)
                else:
                    link.set_animation(link.link_walk[link.facing], 0)
            elif key == K_n:
                link.no_clip = not link.no_clip
        if key == K_TAB:
            if current_state == game_state:
                current_state = pause_state
            else:
                current_state = game_state
        if key == K_SPACE:
            for textbox in textboxes:
                if textbox.waiting:
                    textbox.scrolling = True
                if textbox.finished:
                    textboxes.remove(textbox)
                    del textbox
                    game_scene.update_all = True
                    game_scene.update('game_view')
                    game_scene.update_all = False
                    link.controllable = True
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
    link.controllable = False
    var['invert'] = False
    if link.direction == 0:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] += var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 1:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 2:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 3:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] += var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    build_world()


def build_world():
    global game_map
    for game_object in game_scene.list_objects():
        for object_property in game_object.properties.keys():
            # if object_property == "object_type":
                # Build special objects
                # object_type = game_object.properties[object_property]
                # if object_type == "big_beach_grass":
                #     game_scene.remove_object(game_object)
                    # game_scene.insert_object(specialtiles.BigBeachGrass(game_map.resource_manager), coordinate)
                # if object_type == "half_post":
                #     game_object.collision_rect = pygame.Rect((8, 0), (8, 16))
            # if object_property == "collision_rect":
            #     crect_list = map(int, game_object.properties[object_property].split(','))
            #     game_object.collision_rect = pygame.Rect(crect_list)
            pass


def test_music_change():
    for game_object in game_scene.check_object_collision_objects(link):
        if game_object.object_type == "music_zone":
            if resource_manager.current_key != game_object.properties["song"]:
                resource_manager.play_music(game_object.properties["song"])


def update_room():
    update_player()
    update_animated_tiles()


def update_player():
    global var, resource_manager

    moved = False
    action = False
    #
    # # Move link if keys are pressed
    # key = pygame.key.get_pressed()
    # if link.controllable:
    #     # If not holding a movement key
    #     if key[K_b] and link.shield:
    #         if link.state != "using_shield":
    #             if link.state != "colliding":
    #                 link.play_sound('link_shield')
    #             link.state = "using_shield"
    #             link.change_animation = True
    #             # TODO Add second frame to shield animations and put animation_frame 0 here
    #         action = True
    #     if not key[K_a] and not key[K_d] and not key[K_w] and not key[K_s] and not key[K_b]:
    #         link.set_animation_frame(0)
    #     # If holding a movement key
    #     else:
    #         if key[K_a] and not key[K_d]:
    #             if not key[K_w] and not key[K_s] and link.facing != 2:
    #                 link.facing = 2
    #                 link.change_animation = True
    #             link.direction = 2
    #             link.moves.append(2)
    #             moved = True
    #         elif key[K_d] and not key[K_a]:
    #             if not key[K_w] and not key[K_s] and link.facing != 0:
    #                 link.facing = 0
    #                 link.change_animation = True
    #             link.direction = 0
    #             link.moves.append(0)
    #             moved = True
    #         if key[K_s] and not key[K_w]:
    #             if not key[K_d] and not key[K_a] and link.facing != 3:
    #                 link.facing = 3
    #                 link.change_animation = True
    #             link.direction = 3
    #             link.moves.append(3)
    #             moved = True
    #         elif key[K_w] and not key[K_s]:
    #             if not key[K_d] and not key[K_a] and link.facing != 1:
    #                 link.facing = 1
    #                 link.change_animation = True
    #             link.direction = 1
    #             link.moves.append(1)
    #             moved = True

        # Execute all movement keys held and check for collisions in each direction
        # if moved:
        #     not_colliding_any = True
        #     hop_encountered = False
        #     on_short_grass = False
        #     for move_direction in link.moves:
        #         if link.controllable:
        #             not_colliding_direction = True
        #             previous_position = link.position
        #             game_scene.increment_object(link, link.movement[move_direction])
        #             for game_object in game_scene.check_object_collision_objects(link):
        #                 # Regular collisions, stop movement
        #                 if game_object.solid and not link.no_clip:
        #                     if link.state != "colliding":
        #                         link.state = "colliding"
        #                         link.change_animation = True
        #                     not_colliding_direction = False
        #                     not_colliding_any = False
        #                     break
        #
        #                 # Holes
        #                 if game_object.object_type == "hole":
        #                     link.state = "slipping"
        #                     not_colliding_any = False
        #                     if game_scene.check_contain_object(game_object, link):
        #                         link.state = "falling"
        #                         link.change_animation = True
        #
        #                 # Jump spots
        #                 if game_object.object_type == "Jumps":
        #                     link.controllable = False
        #                     hop_encountered = True
        #
        #                 # Short grass
        #                 if game_object.object_type == "short_grass" or game_object.object_type == "short_forest_grass":
        #                     if not var['short_grass_drawn']:
        #                         if game_object.object_type == "short_grass":
        #                             game_scene.insert_object(effects.ShortGrass(), link.position)
        #                         elif game_object.object_type == "short_forest_grass":
        #                             game_scene.insert_object(effects.ShortForestGrass(), link.position)
        #                         var['short_grass_drawn'] = True
        #                     on_short_grass = True
        #
        #                 # Stairs
        #                 if "slow" in game_object.properties:
        #                     link.set_speed(float(game_object.properties["slow"]))
        #                 else:
        #                     link.set_speed(float(1.25))
        #
        #             # Move is ok, execute
        #             if not not_colliding_direction:
        #                 game_scene.move_object(link, previous_position)
        #
        #     # Move short grass and update animations
        #     if on_short_grass:
        #         for game_object in game_scene.list_objects():
        #             if game_object.object_type == "effect_short_grass" or \
        #                game_object.object_type == "effect_short_forest_grass":
        #                 game_scene.move_object(game_object, link.position)
        #                 game_object.update()
        #     else:
        #         for game_object in game_scene.list_objects():
        #             if game_object.object_type == "effect_short_grass" or \
        #                game_object.object_type == "effect_short_forest_grass":
        #                 game_scene.remove_object(game_object)
        #         var['short_grass_drawn'] = False
        #
        #     # Step passed with no hard collisions or hole encounters
        #     if not_colliding_any:
        #         if hop_encountered:
        #             link.play_sound("link_hop")
        #             link.state = "hopping"
        #             link.animation_counter = 0
        #             link.change_animation = True
        #         if link.state == "colliding" or link.state == "slipping":
        #             link.state = "walking"
        #             link.controllable = True
        #             link.change_animation = True
        #     elif link.state == "slipping":
        #         # TODO: Fall toward hole
        #         pass
        #     if link.state == "falling":
        #         link.controllable = False
        #         print("Link died")
        #     link.moves = []

    if link.controllable:
        link.handle_input(game_scene)

        # if moved:
        #     link.update(True)
        # elif action:
        #     link.update(False)
        # else:
        #     link.state = "walking"
        #     link.change_animation = True
    # else:
    #     if link.state == "hopping":
    #         moved = False
    #         for game_object in game_scene.check_object_collision_objects(link):
    #             if game_object.solid or game_object.object_type == "Jumps":
    #                 game_scene.increment_object(link, (0, 1))
    #                 moved = True
    #         link.hop(moved)

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
    # link.handle_animations()


def update_animated_tiles():
    global game_scene, var
    # if var['animation_frames'] >= 15:
    #     var['animation_frames'] = 0
    #     var['current_frame'] += 1
    # if var['current_frame'] > 3:
    #     var['current_frame'] = 0
    # var['animation_frames'] += 1
    for game_object in game_scene.list_objects():
        if game_object.animate:
            game_object.update()
            if var['current_frame'] != game_object.animation_frame:
                var['current_frame'] = game_object.animation_frame


def move_camera():
    if var['camera_increment'] > 0:
        game_scene.update_all = True
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
        test_music_change()


def terminate():
    global force_exit
    force_exit = True
    print("Forcing exit from run_game")
    # pygame.quit()
    # sys.exit()


def has_quit():
    print("Pygame has quit")


# if __name__ == '__main__':
#     main()
#     print("Exited main")
main()
print("Exited main")

print("We're at the very end of execution")
sys.exit()