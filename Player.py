import arcade


class Player(arcade.Sprite):


    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.stamina = 10
        self.max_health = 10000
        self.health = self.max_health

