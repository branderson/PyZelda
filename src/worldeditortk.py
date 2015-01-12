__author__ = 'brad'

from Tkinter import *
import engine
import pygame

RESOURCE_DIR = '../resources/'


class TileButton(Button):
    def __init__(self, parent, value, image=None, width=16, height=16):
        Button.__init__(self, parent)
        self.config(image=image, width=width, height=height)
        self.value = value


def main():
    global world, resource_manager

    # pygame.init()
    # pygame.display.set_mode((640, 480))

    world = open(RESOURCE_DIR + "worlds/overworld")

    # overworld_sheet = engine.Spritesheet(RESOURCE_DIR + "OverworldSheet.png")
    # resource_manager = engine.ResourceManager()
    # resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)

    # Set up the window
    app = Application()
    app.master.title("World Editor")
    app.pack()
    app.mainloop()


class Application(Frame):
    global resource_manager

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.photo = PhotoImage(file=RESOURCE_DIR + "OverworldSheet.png")
        self.buttons = []
        self.tool_frame = Frame(self)
        self.world_frame = Frame(self)

        for i in xrange(0, 25):
            for j in xrange(0, 24):
                self.buttons.append(TileButton(self.tool_frame, j + i * 24,
                                               image=resource_manager.get_images('overworld_tiles')
                                    [j + i * 24], width=16, height=16))
                self.buttons.append(TileButton(self.tool_frame, j+i*24, PhotoImage(RESOURCE_DIR + "OverworldSheet.png"),
                                               width=16, height=16))
        # self.sprites = Button(self.tool_frame, text="Is it", bg='red')
        # self.world = Canvas(self.world_frame)
        # self.id = self.world.create_image(0, 0, image=self.photo)
        self.world.pack()
        self.sprites.pack()
        self.tool_frame.pack(side="left")
        self.world_frame.pack(side="right")


if __name__ == '__main__':
    main()