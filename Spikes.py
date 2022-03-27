import arcade

class Spikes(arcade.Sprite):

    def __init__(self, a, b, size, lives, damage, price):
        super().__init__(a, b)
        self.lives = lives
        self.damage = damage
        self.width = size
        self.height = size
        self.price = price

        self.points = None
        self.hit_box = [[-self.width//2 - 5, -self.height // 2 - 5],
                        [-self.width//2 - 5, +self.height // 2 + 5],
                        [+self.width//2 + 5, -self.height // 2 - 5],
                        [+self.width//2 + 5, +self.height // 2 + 5]]
