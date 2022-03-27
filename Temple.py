import arcade

class Temple(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.level = 0
        self.textures = []
        self.readTextures()
        self.levelCost = {0: 250, 1: 550, 2: 750, 3: 1250}

    def readTextures(self):

            sheet = arcade.load_spritesheet(f"images/temple.png", 392, 444, 4, 4, 0)
            for i in range(4):
                self.textures.append(sheet[i])
