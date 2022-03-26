import arcade

UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1


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
        
        
        self.character_face_direction = RIGHT_FACING

        self.idle_textures = []
        self.walking_textures = []
        self.combat_textures = [] # 4d pole?

        self.scale = 1
        self.cur_texture = 0

        self.textures_sheet = arcade.load_spritesheet(f"images/player.png", 128, 64, 12, 60, 0)
        for i in range(8):
            self.idle_textures.append(self.textures_sheet[i])
        for i in range(12, 20):
            self.walking_textures.append(self.textures_sheet[i])

        self.texture = self.textures_sheet[0]



    def move(self,key):

        if key == "U":
            self.viewP = [0, 1]
        elif key == "D":
            self.viewP = [0, -1]
        elif key == "L":
            self.viewP = [-1, 0]
        elif key == "R":
            self.viewP = [1, 0]
        
        

    def update_animation(self, delta_time: float = 1 / 60):

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
                self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                direction = self.character_face_direction
                self.texture = self.idle_textures[frame]#[direction]
            return


        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walking_textures[frame]#[direction]
