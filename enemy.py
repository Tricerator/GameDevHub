import arcade
import random

GREEN = 0
BLUE = 1
RED = 2
YELLOW = 3

UPDATES_PER_FRAME = 8

def loadTextures():

    textures = []
    for i in range(3):
        textures.append([])

    pngtextury = ["blue", "red", "green", "yellow"]
    obj = 0
    for png in range(3):
        sheet = arcade.load_spritesheet(f"images/{pngtextury[png]}.png", 56, 88, 10, 30, 0)
        for i in range(0, 10):
            textures[obj].append(sheet[i])
        obj += 1
        print(textures)
    return textures

class Enemy(arcade.Sprite):

    def __init__(self, colour):
        super().__init__()
        self.scale = random.randint(1, 3)
        self.timer_rand = 0
        self.timer_smart = 0
        self.speed = 2 #+ (DIFFICULTY/10)
        self.life = 10
        self.value = 30 + self.scale*10
        self.colour = colour
        self.dir_x = None
        self.dir_y = None

        self.texture = self.colour[0]
        self.cur_texture = 0

    def update(self):
        self.change_x = self.dir_x
        self.change_y = self.dir_y
        self.center_x += self.change_x
        self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 10 * UPDATES_PER_FRAME - 1:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        if frame > 4:
            self.update()
        self.texture = self.colour[frame]

