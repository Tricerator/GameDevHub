import arcade

class Background(arcade.Sprite):

    def __init__(self, a, b, TILE_SIZE, ANGLE):
        super().__init__(a, b)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.angle = ANGLE
