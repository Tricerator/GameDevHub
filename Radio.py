import arcade

UPDATES_PER_FRAME = 4

class Radio(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = 1
        self.cur_texture = 0

        self.radio = []
        self.sheet = arcade.load_spritesheet(f"images/radio.png", 236, 168, 8, 8, 0)

        for radio in range(8):
            self.radio.append(self.sheet[radio])

        self.texture = self.radio[0]

    def update_animation(self, delta_time: float = 1 / 60):

        self.cur_texture += 1
        if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.radio[frame]

