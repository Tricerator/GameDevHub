import arcade

class Tree(arcade.Sprite):

    def __init__(self, a, b, lives):
        super().__init__(a, b)
        self.lives = lives
        self.points = None

        x = self.width * 0.1
        y = self.height * 0.1
        self.hit_box = [[- x / 2, -self.height // 2],
                        [+ x / 8, -self.height // 2],
                        [+ x / 8, -self.height // 3],
                        [- x / 2, -self.height // 3]]
