import arcade


UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

class Companion(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.kaboom = False
        self.alive = True
        self.walk = True
        self.exploded = False

        self.character_face_direction = RIGHT_FACING

        self.idle_textures = []
        self.walking_textures = []
        self.kaboom_textures = []

        self.scale = 0.69
        self.cur_texture = 0
        self.boom_texture = 0

        self.textures_sheet = arcade.load_spritesheet(f"images/player.png", 128, 64, 12, 60, 0)
        for i in range(8):
            self.idle_textures.append(self.textures_sheet[i])
        for i in range(12, 20):
            self.walking_textures.append(self.textures_sheet[i])
        for i in range(48, 60):
            self.kaboom_textures.append(self.textures_sheet[i])

        self.texture = self.textures_sheet[0]


    def update(self):
        if self.walk:
            self.center_x += self.change_x
            self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1 / 60):
        # Idle animation
        if self.alive:
            if not self.kaboom:

                # Walking animation
                self.cur_texture += 1
                if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                direction = self.character_face_direction
                self.texture = self.walking_textures[frame]#[direction]

            else:
                self.boom_texture += 1
                if self.boom_texture > 11 * 4 - 1:
                    self.alive = False
                frame = self.boom_texture // 4
                print(frame)
                direction = self.character_face_direction
                self.texture = self.kaboom_textures[frame]  # [direction]