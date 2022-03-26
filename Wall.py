import arcade

class Wall(arcade.Sprite):

    def __init__(self, a, b, size, lives, damage, price):
        super().__init__(a, b)
        self.lives = lives
        self.damage = damage
        self.width = size
        self.height = size
        self.price = price

