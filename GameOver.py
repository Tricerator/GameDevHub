import arcade
import main

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT ):
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
        game_view = main.GameView()
        game_view.setup()
        self.window.show_view(game_view)
