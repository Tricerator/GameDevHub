import random
import time

import arcade

from Player import Player
from Wall import Wall
from enemy import Enemy

SCREEN_TITLE = "Gummy terror"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 6
PLAYER_SCALING = 1

ROCK_SCALING = 0.1

ENEMY_SCALING = 1

DIFFICULTY = 5



SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.csscolor.DARK_RED)
        self.scene = None
        self.player_sprite = None

        self.physics_engine = None


        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.music = None

    def setup(self):
        """ Set up everything with the game """
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.music = arcade.load_sound("sounds/dark.webm")
        self.music.play()

        self.player_sprite = Player("images/player1.png", PLAYER_SCALING)
        self.player_sprite.position = [SCREEN_WIDTH//2, SCREEN_HEIGHT//2]
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Companions")
        self.scene.add_sprite_list("Projectiles")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("Non-walkable things")
        self.scene.add_sprite_list("Monument")

        for i in range(6):
            rock_sprite = Wall("images/rock.png", ROCK_SCALING)
            rock_sprite.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
            self.scene.add_sprite("Walls", rock_sprite)

        """enemy_sprite = arcade.Sprite("images/ememy.png", ENEMY_SCALING)
        enemy_sprite.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        self.scene.add_sprite("Enemies", enemy_sprite)"""

        self.createEnemies(6)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

    def createEnemies(self, ENEMY_COUNT_INITIAL):
        image_list = ["images/ememy.png"]
        for i in range(ENEMY_COUNT_INITIAL):
            image_no = random.randint(0, len(image_list) - 1)
            size = random.randint(1,5)
            enemy_sprite = Enemy(image_list[image_no], (size + 5) / 10)
            enemy_sprite.timer_rand = 0
            enemy_sprite.timer_smart = 0
            enemy_sprite.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]

            if self.player_sprite.center_x > enemy_sprite.center_x:
                enemy_sprite.change_x = random.randint(1, 3)
            else:
                enemy_sprite.change_x -= random.randint(1, 3)

            if self.player_sprite.center_y > enemy_sprite.center_y:
                enemy_sprite.change_y = random.randint(1, 3)
            else:
                enemy_sprite.change_y -= random.randint(1, 3)


            enemy_sprite.size = size

            self.scene.add_sprite("Enemies", enemy_sprite)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False

        if key == arcade.key.LCTRL and self.player_sprite.stamina > 0:
            self.player_sprite.change_x + 2
            self.player_sprite.change_y + 2
            self.player_sprite.stamina -= 1

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y += PLAYER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y -= PLAYER_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x -= PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x += PLAYER_SPEED

        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

        self.physics_engine.update()

        arcade.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH / 2,
                            self.player_sprite.center_x + SCREEN_WIDTH / 2,
                            self.player_sprite.center_y - SCREEN_HEIGHT / 2,
                            self.player_sprite.center_y + SCREEN_HEIGHT / 2)


        enemy_speedy = 0.5 # + (self.player_sprite.difficulty / 12)
        for enemy in self.scene["Enemies"]:

            y_pos = enemy.center_y
            x_pos = enemy.center_x

            if self.player_sprite.center_y > y_pos:
                dir_y = 1

            if self.player_sprite.center_x > x_pos:
                dir_x = 1

            if self.player_sprite.center_y <= y_pos:
                dir_y = -1

            if self.player_sprite.center_x <= x_pos:
                dir_x = -1

            enemy.change_x = dir_x * (enemy_speedy ) *(3/enemy.size)
            enemy.change_y = dir_y * (enemy_speedy )*(3/enemy.size)

            if len(arcade.check_for_collision_with_list(enemy, self.scene["Walls"]) )> 0:
                enemy.change_x *= -1
                enemy.change_y *= -1
                hitList = arcade.check_for_collision_with_list(enemy, self.scene["Walls"])
                for c in hitList:
                    if c.lives <= 0:
                       c.kill()
                    c.lives -= 1

                # If the enemy hit the left boundary, reverse
            """  elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
            elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                enemy.change_x *= -1
            """
            enemy.center_x += enemy.change_x
            enemy.center_y += enemy.change_y

            hitListEnemy = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Enemies"])
            if len(hitListEnemy) > 0:
                for enemy in hitListEnemy:
                    if self.player_sprite.health <= 0:
                       self.player_sprite.kill()

                    self.player_sprite.health -= enemy.size

                    if enemy.center_x < self.player_sprite.center_x:
                        enemy.center_x -= 30
                    elif enemy.center_x >= self.player_sprite.center_x:
                        enemy.center_x += 30
                    if enemy.center_y < self.player_sprite.center_y:
                        enemy.center_y -= 30
                    elif enemy.center_y >= self.player_sprite.center_y:
                        enemy.center_y += 30


    def on_draw(self):
        """ Draw everything """
        self.clear()

        self.scene.draw()


def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()