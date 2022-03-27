import arcade


class BuildingTools(arcade.Sprite):

    def __init__(self, a, b, tile_size):
        super().__init__(a, b)
        self.width = tile_size//3*2
        self.height = tile_size//3*2
