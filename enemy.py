import arcade

class Enemy(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
        self.timer_rand = 0
        self.timer_smart = 0
        self.speed = 2 #+ (DIFFICULTY/10)
        self.life = 10
