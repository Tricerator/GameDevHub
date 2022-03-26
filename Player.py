import arcade

UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

IDLE_TEX = 0
WALKING_TEX = 1
COMBAT_TEX = 2
HOOD_IDLE_TEX = 3
HOOD_WALKING_TEX = 4
HOOD_COMBAT_TEX = 5
SWORD_IDLE_TEX = 6
SWORD_WALKING_TEX = 7
SWORD_COMBAT_TEX = 8


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.stamina = 10
        self.max_health = 100
        self.health = self.max_health
        self.viewP = [0,0]
        self.coins = 0

        '''
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
        '''
        
        self.character_face_direction = 0

        self.scale = 1
        self.cur_texture = 0

        self.is_attacking = False
        self.attack_texture = 0

        self.all_textures = []
        for i in range(9):
            self.all_textures.append([[]])

        indexes = [0,8,4,12,12,20,16,24,24,32,28,36]


        """
                TEXTURY INQUISITORA PRO ANIMACI
        """
        pngtextury = ["inquisitor", "hood", "sword"]
        obj = 0
        for png in range(3):
            self.sheet = arcade.load_spritesheet(f"images/{pngtextury[png]}.png", 128, 64, 12, 60, 0)
            self.sheet1 = arcade.load_spritesheet(f"images/{pngtextury[png]}1.png", 128, 64, 12, 60, 0)
            mi, ma = 0, 1
            for j in range(3):
                for i in range(indexes[mi], indexes[ma]):
                    self.all_textures[obj].append([self.sheet[i]])
                index = 0
                del self.all_textures[obj][0]
                mi += 2
                ma += 2
                for i in range(indexes[mi], indexes[ma]):
                    self.all_textures[obj][index].append(self.sheet1[i])
                    index += 1
                obj += 1
                mi += 2
                ma += 2

            '''
            for i in range(12, 20):
                self.all_textures[obj].append([self.sheet[i]])
            index = 0
            del self.all_textures[obj][0]
            for i in range(16, 24):
                self.all_textures[obj][index].append(self.sheet1[i])
                index += 1
            obj += 1
            for i in range(24, 32):
                self.all_textures[obj].append([self.sheet[i]])
            index = 0
            del self.all_textures[obj][0]
            for i in range(28,36):
                self.all_textures[obj][index].append(self.sheet1[i])
                index += 1
            obj += 1
            '''

        self.texture = self.all_textures[IDLE_TEX][0][0]
        self.hood = arcade.Sprite("images/hood.png")
        self.hood.texture = self.all_textures[HOOD_IDLE_TEX][0][0]
        self.sword = arcade.Sprite("images/sword.png")
        self.sword.texture = self.all_textures[SWORD_IDLE_TEX][0][0]


    def move(self, key):

        if key == "U":
            self.viewP = [0, 1]
        elif key == "D":
            self.viewP = [0, -1]
        elif key == "L":
            self.viewP = [-1, 0]
        elif key == "R":
            self.viewP = [1, 0]

    def update(self):
        self.hood.center_x = self.center_x
        self.hood.center_y = self.center_y
        self.sword.center_x = self.center_x
        self.sword.center_y = self.center_y

    def update_animation(self, delta_time: float = 1 / 60):


        direction = 0
        if self.viewP[0] == 1:
            direction = 1
        # Idle animation
        if not self.is_attacking:
            if self.change_x == 0 and self.change_y == 0:
                self.cur_texture += 1
                if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                self.texture = self.all_textures[IDLE_TEX][frame][direction]
                self.hood.texture = self.all_textures[HOOD_IDLE_TEX][frame][direction]
                self.sword.texture = self.all_textures[SWORD_IDLE_TEX][frame][direction]
                return


            # Walking animation
            self.cur_texture += 1
            if self.cur_texture > 8 * UPDATES_PER_FRAME - 1:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.all_textures[WALKING_TEX][frame][direction]
            self.hood.texture = self.all_textures[HOOD_WALKING_TEX][frame][direction]
            self.sword.texture = self.all_textures[SWORD_WALKING_TEX][frame][direction]

        else:
            self.attack_texture += 1
            if self.attack_texture > 8 * 4 - 1:
                self.attack_texture = 0
                self.is_attacking = False
            frame = self.attack_texture // 4
            self.texture = self.all_textures[COMBAT_TEX][frame][direction]
            self.hood.texture = self.all_textures[HOOD_COMBAT_TEX][frame][direction]
            self.sword.texture = self.all_textures[SWORD_COMBAT_TEX][frame][direction]



