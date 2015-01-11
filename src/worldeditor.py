__author__ = 'brad'
import pygame
import sys
import engine
from pygame.locals import *

RESOURCE_DIR = '../resources/'


def main():
    global screen, world, application_surface, toolbox, buttons
    pygame.init()

    world = open(RESOURCE_DIR + "worlds/overworld")

    screen = pygame.display.set_mode((1250, 480))
    resource_manager = engine.ResourceManager()
    application_surface = pygame.Surface((1250, 480))
    toolbox = engine.CoordinateSurface((384, 480), (384, 480))
    toolbox.fill((255, 255, 255))

    overworld_sheet = engine.Spritesheet(RESOURCE_DIR + "OverworldSheet.png")
    resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)
    buttons = []

    for i in xrange(0, 25):
        for j in xrange(0, 24):
            buttons.append(Button(resource_manager.get_images('overworld_tiles')[j+i*24], j+i*24))

    # Draw buttons to toolbox
    button = 0
    for i in xrange(0, 25):
        for j in xrange(0, 24):
            toolbox.insert_object(buttons[button], (j*16, i*16))
            button += 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                world.close()
                pygame.quit()
                sys.exit()
            handle_event(event)
        draw()
        pygame.display.flip()


def handle_event(event):
    global buttons
    if event.type == MOUSEBUTTONDOWN:
        if True:
            for button in buttons:
                if pygame.Rect(toolbox.check_position(button), (button.rect.width,
                                                                button.rect.height)).collidepoint(event.pos):
                    print(button.value)


def draw():
    global screen, application_surface, toolbox
    toolbox.update()
    application_surface.blit(toolbox.draw(), (0, 0))
    screen.blit(application_surface, (0, 0))


class Button(engine.GameObject):
    def __init__(self, image, value):
        engine.GameObject.__init__(self, image)
        self.value = value


if __name__ == '__main__':
    main()