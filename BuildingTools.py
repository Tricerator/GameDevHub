import arcade

class BuildingTools(arcade.Sprite):

    def __init__(self,a,b, TILE_SIZE):
        super().__init__(a,b)
        self.width = TILE_SIZE
        self.height = TILE_SIZE