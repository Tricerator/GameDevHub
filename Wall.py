import arcade

class Wall(arcade.Sprite):

    def __init__(self,a,b):
        super().__init__(a,b)
        self.lives = 30
