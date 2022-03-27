import random

import arcade

from Background import Background
from BuildingTools import BuildingTools
# from GameOver import GameOverView
from Player import Player
from Wall import Wall
from Companion import Companion
from enemy import Enemy
import enemy as en
from MapGeneration import generateMap

SCREEN_TITLE = "Gummy terror"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TILE_SIZE = 64
MAP_TILE_WIDTH = 100
MAP_TILE_HEIGHT = 100
TOTAL_WIDTH = TILE_SIZE * MAP_TILE_WIDTH
TOTAL_HEIGHT = TILE_SIZE * MAP_TILE_HEIGHT

HORIZONTAL_TILES_COUNT = SCREEN_WIDTH // TILE_SIZE
VERTICAL_TILES_COUNT = SCREEN_HEIGHT // TILE_SIZE  # up down

PLAYER_SPEED = 6
PLAYER_SCALING = 1

ROCK_SCALING = 0.1
ENEMY_SCALING = 1
DIFFICULTY = 5
SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)


class GameView(arcade.View):
    """ Main Window """

    def __init__(self):
        """ Create the variables """
        # Init the parent class
        super().__init__()
        arcade.set_background_color(arcade.csscolor.DARK_RED)
        self.scene = None
        self.player_sprite = None
        # building shit
        self.buildingSquare_sprite = None
        self.buildThorns = False

        self.physics_engine = None

        self.mouse_position_x = 0
        self.mouse_position_y = 0

        self.on_screen_pointer_x = 0
        self.on_screen_pointer_y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.c_pressed = False
        self.b_pressed = False
        self.k_pressed = False
        self.l_pressed = False

        self.music = None

        self.sounds = {}
        self.user_volume = 0.8

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)
        self.gui_camera = None

        self.graphicsTextures = {}
        self.enemy_texture_list = en.loadTextures()

    def setup(self):
        """ Set up everything with the game """
        self.scene = arcade.Scene()

        self.createBackground()

        self.scene.add_sprite_list("Player")
        # self.music = arcade.load_sound("sounds/dark.webm")
        # self.music.play()

        self.player_sprite = Player()
        self.player_sprite.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("Companions")
        self.scene.add_sprite_list("Effects")
        self.scene.add_sprite_list("Projectiles")
        self.scene.add_sprite_list("Walls")
        self.scene.add_sprite_list("Non-walkable things")
        self.scene.add_sprite_list("Monument")
        self.scene.add_sprite_list("Background")
        self.scene.add_sprite_list("Building tools")

        self.sounds["swordAttack"] = arcade.load_sound("sounds/sword_strike2.wav")
        self.sounds["hit"] = arcade.load_sound(":resources:sounds/hurt2.wav")
        self.sounds["wall"] = arcade.load_sound("sounds/wall-crash.wav")
        self.sounds["thorns"] = arcade.load_sound("sounds/thorns.wav")
        self.sounds["clearGround"] = arcade.load_sound(":resources:sounds/upgrade1.wav")



        """for i in range(6):
            rock_sprite = Wall("images/rock.png", ROCK_SCALING)
            rock_sprite.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
            self.scene.add_sprite("Walls", rock_sprite)"""

        self.createWalls(100)

        """enemy_sprite = arcade.Sprite("images/ememy.png", ENEMY_SCALING)
        enemy_sprite.position = [random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)]
        self.scene.add_sprite("Enemies", enemy_sprite)"""

        self.createEnemies(6)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

        self.textures_sheet = arcade.load_spritesheet(f"images/player.png", 128, 64, 12, 60, 0)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

    def createBackground(self):
        imagePath = "images/tiles/cobble/"

        mapList = generateMap(MAP_TILE_WIDTH, MAP_TILE_HEIGHT)
        for row in range(len(mapList)):
            for column in range(len(mapList[row])):
                picName = mapList[row][column]
                if picName == "GGGG" and random.randint(0, 100) > 90:
                    picName = "GGGG2"

                elif picName == "GRGR" and random.randint(0, 100) > 50:
                    picName = "GRGR2"

                elif picName == "RGRG" and random.randint(0, 100) > 50:
                    picName = "RGRG2"

                elif picName == "RRRR" and random.randint(0, 100) > 75:
                    picName = "RRRR2"

                elif picName == "RRRR" and random.randint(0, 100) > 66:
                    picName = "RRRR3"

                if picName == "GGGG2":
                    ANGLE = random.choice([0, 90, 180, 270])

                elif picName == "RRRR2":
                    ANGLE = random.choice([0, 180])

                elif picName == "RRRR3":
                    ANGLE = random.choice([0, 180])

                else:
                    ANGLE = 0

                finalPath = imagePath + picName + ".png"
                background_sprite = Background(finalPath, 1, TILE_SIZE, ANGLE)

                background_sprite.position = [-TOTAL_WIDTH // 2 + column * TILE_SIZE,
                                              -TOTAL_HEIGHT // 2 + row * TILE_SIZE]
                # background_sprite.position = [-TOTAL_WIDTH//2 + column * TILE_SIZE + column, -TOTAL_HEIGHT // 2 + row * TILE_SIZE + row]
                self.scene.add_sprite("Background", background_sprite)

    def createWalls(self, WALL_COUNT_INITIAL):
        image_list = ["images/rocks/2.png", "images/rocks/3.png"]
        for i in range(WALL_COUNT_INITIAL):
            image_no = random.randint(0, len(image_list) - 1)
            # size =
            rock_sprite = Wall(image_list[image_no], 1, TILE_SIZE, 40, 0, 0)

            rock_sprite.position = [random.randint(-TOTAL_WIDTH // 2, TOTAL_WIDTH // 2),
                                    random.randint(-TOTAL_HEIGHT // 2, TOTAL_HEIGHT // 2)]

            self.scene.add_sprite("Walls", rock_sprite)

    def buildWall(self):
        for dictionary in ["Player", "Enemies", "Companions", "Walls", "Non-walkable things", "Monument"]:
            if len(arcade.check_for_collision_with_list(self.buildingSquare_sprite, self.scene[dictionary])) > 0:
                break
        else:
            build = False
            if self.buildThorns and self.player_sprite.coins >= 30:
                self.player_sprite.coins -= 30
                rock_sprite = Wall("images/rocks/spikes.png", 1, TILE_SIZE, 20, 1, 30)
                build = True
            else:
                if self.player_sprite.coins >= 15:
                    self.player_sprite.coins -= 15
                    rock_sprite = Wall("images/rocks/Castle_Wall.webp", 1, TILE_SIZE, 40, 0, 20)
                    build = True
            if build:
                rock_sprite.position = [self.on_screen_pointer_x, self.on_screen_pointer_y]
                self.scene.add_sprite("Walls", rock_sprite)

    def createBuildTool(self):
        self.buildingSquare_sprite = BuildingTools("images/build tools/rect.png", 1, TILE_SIZE)
        self.buildingSquare_sprite.position = [self.player_sprite.center_x + self.mouse_position_x - SCREEN_WIDTH // 2,
                                               self.player_sprite.center_y + self.mouse_position_y - SCREEN_HEIGHT // 2]
        self.scene.add_sprite("Building tools", self.buildingSquare_sprite)

    def createEnemies(self, ENEMY_COUNT_INITIAL):

        for i in range(ENEMY_COUNT_INITIAL):
            colour_scheme = random.choice(self.enemy_texture_list)
            enemy_sprite = Enemy(colour_scheme)
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


            enemy_sprite.phys = arcade.PhysicsEngineSimple(enemy_sprite, self.scene.get_sprite_list("Enemies"))

            self.scene.add_sprite("Enemies", enemy_sprite)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_position_x = x
        self.mouse_position_y = y

        """if self.b_pressed:
            self.buildingSquare_sprite.center_x = self.player_sprite.center_x + self.mouse_position_x - SCREEN_WIDTH//2
            self.buildingSquare_sprite.center_y = self.player_sprite.center_y + self.mouse_position_y - SCREEN_HEIGHT//2"""

    def on_mouse_press(self, x, y, key, modifiers):
        if self.b_pressed:
            self.buildWall()
        else:
            self.attack()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
            self.player_sprite.move("U")
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
            self.player_sprite.move("D")
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
            self.player_sprite.move("L")
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True
            self.player_sprite.move("R")

        elif key == arcade.key.C:
            self.c_pressed = True

        if key == arcade.key.K:
            self.k_pressed = True
        elif key == arcade.key.L:
            self.l_pressed = True

        elif key == arcade.key.B:
            self.b_pressed = not self.b_pressed
            if self.b_pressed:
                self.createBuildTool()
            else:
                self.buildingSquare_sprite.remove_from_sprite_lists()

        if self.b_pressed:
            if key == arcade.key.KEY_2:
                self.buildThorns = True
            if key == arcade.key.KEY_1:
                self.buildThorns = False

        if self.k_pressed:
            if self.user_volume > 0.2:
                self.user_volume -= 0.1
            self.k_pressed = False
        elif self.l_pressed:
            if self.user_volume < 1:
                self.user_volume += 0.1
            self.l_pressed = False

            # self.buildWall()

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
            # self.player_sprite.change_x + 2
            # self.player_sprite.change_y + 2
            self.player_sprite.stamina -= 1

    def attack(self):
        self.sounds["swordAttack"].play(self.user_volume)
        self.player_sprite.is_attacking = True

        addVector = [0, 0]
        if self.player_sprite.viewP[0] < 0:
            addVector[0] = -2
        else:
            addVector[0] = 2
        if self.player_sprite.viewP[1] < 0:
            addVector[1] = -2
        else:
            addVector[1] = 2

            # for enemy in self.scene["Enemies"]:
            # hit = False
            '''
            if self.player_sprite.viewP[0] <= 0:
                if enemy.center_x - (self.player_sprite.center_x + addVector[0]) < 0 and \
                        abs(enemy.center_y - self.player_sprite.center_y) < 10:
                    hit = True
            elif self.player_sprite.viewP[0] > 0:
                if enemy.center_x - (self.player_sprite.center_x + addVector[0]) >= 0 and \
                        abs(enemy.center_y - self.player_sprite.center_y) < 10:
                    hit = True
            elif self.player_sprite.viewP[1] <= 0:
                if enemy.center_y - (self.player_sprite.center_y + addVector[1]) >= 0 and \
                        abs(enemy.center_x - self.player_sprite.center_x) < 10:
                    hit = True
            elif self.player_sprite.viewP[1] > 0:
                if enemy.center_y - (self.player_sprite.center_y + addVector[1]) < 0 and \
                        abs(enemy.center_x - self.player_sprite.center_x) < 10:
                    hit = True
                    '''
        enemies = arcade.check_for_collision_with_list(self.player_sprite.sword, self.scene["Enemies"])
        if len(enemies) > 0:
            for enemy in enemies:

                # if hit:
                s = self.sounds["hit"]
                s.play(self.user_volume)
                enemy.life -= 1
                if enemy.life <= 0:
                    self.player_sprite.coins += 10 * enemy.scale
                    self.scene["Enemies"].remove(enemy)
                    enemy.kill()
                    if len(self.scene["Enemies"]) <= 0:
                        snd =  arcade.load_sound(":resources:sounds/upgrade1.wav")
                        self.sounds["clearGround"].play(self.user_volume)

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
        #     enemy_speedy = 0.5  # + (self.player_sprite.difficulty / 12)
        for enemy in self.scene["Enemies"]:
            y_pos = enemy.center_y
            x_pos = enemy.center_x
            if self.player_sprite.center_y > y_pos:
                enemy.dir_y = 1
            if self.player_sprite.center_x > x_pos:
                enemy.dir_x = 1
            if self.player_sprite.center_y <= y_pos:
                enemy.dir_y = -1
            if self.player_sprite.center_x <= x_pos:
                enemy.dir_x = -1

            if len(arcade.check_for_collision_with_list(enemy, self.scene["Walls"])) > 0:
                enemy.change_x *= -1
                enemy.change_y *= -1
                hitList = arcade.check_for_collision_with_list(enemy, self.scene["Walls"])
                for c in hitList:
                    if c.lives <= 0:
                        choice = ""
                        if c.damage == 0:
                            choice = "wall"

                        else:
                            choice = "thorns"

                        self.sounds[choice].play(self.user_volume)
                        c.kill()
                    c.lives -= 1

                    enemy.life -= c.damage
                    if enemy.life <= 0:
                        enemy.kill()
                        self.player_sprite.coins = enemy.value
                    c.lives -= 1
                # If the enemy hit the left boundary, reverse
            """  elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
            elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                enemy.change_x *= -1
            """
            # enemy.center_x += enemy.change_x
            # enemy.center_y += enemy.change_y
            hitListEnemy = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Enemies"])
            if len(hitListEnemy) > 0:
                for enemy in hitListEnemy:
                    if self.player_sprite.health <= 0:
                        self.player_sprite.kill()
                        view = GameOverView(SCREEN_WIDTH, SCREEN_HEIGHT)
                        self.window.show_view(view)
                    self.player_sprite.health -= enemy.scale
                    if enemy.center_x < self.player_sprite.center_x:
                        enemy.center_x -= 30
                    elif enemy.center_x >= self.player_sprite.center_x:
                        enemy.center_x += 30
                    if enemy.center_y < self.player_sprite.center_y:
                        enemy.center_y -= 30
                    elif enemy.center_y >= self.player_sprite.center_y:
                        enemy.center_y += 30

        self.on_screen_pointer_x = self.player_sprite.center_x + self.mouse_position_x - SCREEN_WIDTH // 2
        self.on_screen_pointer_y = self.player_sprite.center_y + self.mouse_position_y - SCREEN_HEIGHT // 2

        if self.b_pressed:
            self.buildingSquare_sprite.center_x = self.on_screen_pointer_x
            self.buildingSquare_sprite.center_y = self.on_screen_pointer_y

        if self.c_pressed:
            self.c_pressed = False
            if self.player_sprite.coins >= 100:
                companion_sprite = Companion()
                self.player_sprite.coins -= 100
                companion_sprite.position = [self.player_sprite.center_x, self.player_sprite.center_y]
                self.scene.add_sprite("Companions", companion_sprite)

        for creeper in self.scene["Companions"]:
            closest = arcade.get_closest_sprite(creeper, self.scene["Enemies"])
            if closest is not None:
                if creeper.center_x > closest[0].center_x:
                    creeper.change_x = -0.5  # potom private static final SPEED
                elif creeper.center_x < closest[0].center_x:
                    creeper.change_x = 0.5
                if creeper.center_y > closest[0].center_y:
                    creeper.change_y = -0.5  # potom private static final SPEED
                elif creeper.center_y < closest[0].center_y:
                    creeper.change_y = 0.5

            creeper.update()
            creeper.update_animation()

            companioncolider = arcade.check_for_collision_with_list(creeper, self.scene["Enemies"])
            if len(companioncolider) > 0:
                creeper.kaboom = True
                creeper.walk = False
                for c in companioncolider:
                    if creeper.alive and not creeper.exploded:
                        c.life -= 5
                        if c.life <= 0:
                            c.kill()
                            self.player_sprite.coins += c.value
                creeper.exploded = True

        for e in self.scene["Enemies"]:
            e.update_animation()
            e.phys.update()

        self.player_sprite.update()
        self.player_sprite.update_animation()

    def on_draw(self):
        """ Draw everything """
        self.clear()

        self.scene.draw()
        self.player_sprite.hood.draw()
        self.player_sprite.sword.draw()

        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        nums = len(self.scene["Enemies"])
        score_text = f"Coins: {self.player_sprite.coins}\n" + \
                     f"Enemies: {nums}"

        arcade.draw_rectangle_filled(0, 600, 600, 80, arcade.csscolor.BEIGE)
        arcade.draw_text(
            score_text,
            10,
            575,
            arcade.csscolor.BLACK,
            18,
        )
        arcade.draw_text(
            "vol "+str(int(self.user_volume * 100))+"%",
            690,
            575,
            arcade.csscolor.BLACK,
            18,
        )

        for e in self.scene["Enemies"]:
            e.draw_hit_box()


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("images/gameOver.jpg")
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_sized(self.width / 2, self.height / 2,
                                self.width, self.height)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
