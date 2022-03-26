import arcade

TEXTURE_LEFT = 1
TEXTURE_RIGHT = 0


class Player(arcade.Sprite):


    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.stamina = 10
        self.max_health = 100
        self.health = self.max_health
        self.viewP = ""
        self.coins = 0

        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("images/player1.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/player1.png",
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face left.
        self.texture = self.textures[0]




    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]



    def move(self,key):

        if key == "U":
            self.viewP = [0, 1]
        elif key == "D":
            self.viewP = [0, -1]
        elif key == "L":
            self.texture = self.textures[TEXTURE_LEFT]
            self.viewP = [-1, 0]
        elif key == "R":
            self.texture = self.textures[TEXTURE_RIGHT]
            self.viewP = [1, 0]


