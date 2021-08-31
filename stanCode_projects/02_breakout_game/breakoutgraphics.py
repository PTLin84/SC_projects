"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

Code for class 'BreakoutGraphics'
File: breakoutgraphics.py
Name: 林柏廷 Kyle

EXTENSIONS:
1. Y speed up 1.5x when scores reach 50/100
2. Coin function, coins randomly fall when bricks are hit.
3. Collect coins to buy skins (different colors for the ball/paddle) in the shop.
4. Score board, coin board, highscore board, life icons.
5. Background image.
6. Bricks color change every new game. (3 different color configurations)
7. Automatically save game data in a .txt file. (coins collected, skins bought, highscore)
8. A Button class in breakoutgraphics.py that helps create all buttons.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage    # for background image
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import math
import random
from json import dump, load     # for game data storage (save data even when user close and reopen the game)


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 50       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 12        # Number of columns of bricks.
BRICK_OFFSET = 60      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

##############################################
# FOR EXTENSION
NUM_LIVES = 3
COIN_SIZE = 15
START_WIDTH = 150
START_HEIGHT = 50
RESTART_WIDTH = 150
RESTART_HEIGHT = 50
TRY_AGAIN_WIDTH = 150
TRY_AGAIN_HEIGHT = 50
SHOP_WIDTH = 150
SHOP_HEIGHT = 50
GAME_OVER_X = 206
GAME_OVER_Y = 400
WINNING_X = 200
WINNING_Y = 400
MAX_SCORE = BRICK_COLS * BRICK_ROWS
PRICE_SKIN1 = 10
PRICE_SKIN2 = 20
PRICE_SKIN3 = 30

# for Button class
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
SKIN_WIDTH = 100
SKIN_HEIGHT = 50
SMALL_BUTTON_WIDTH = 50
SMALL_BUTTON_HEIGHT = 30
RESTART_X = 50
RESTART_Y = 450
START_X = 250
START_Y = 450
TRY_AGAIN_X = 250
TRY_AGAIN_Y = 450
SHOP_X = 450
SHOP_Y = 450
LEAVE_SHOP_X = 450
LEAVE_SHOP_Y = 350
SKIN_OFFSET_X = 25

# for testing the shop functions
INITIAL_COIN = 100


class Button:
    """
    A class that helps create a button with basic methods.
    """
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, small=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = GRect(width, height, x=x, y=y)
        self.label = GLabel(text)
        self.clickable = False
        if small is True:
            self.label.font = 'Helvetica-8-bold'
        else:
            self.label.font = 'Helvetica-18-bold'

    def show_btn(self, g):
        self.clickable = True
        g.window.add(self.rect)
        g.window.add(self.label, x=self.rect.x + self.rect.width / 2 - self.label.width / 2,
                     y=self.rect.y + self.rect.height / 2 + self.label.height / 2 + 3)

    def remove_btn(self, g):
        g.window.remove(self.rect)
        g.window.remove(self.label)
        self.clickable = False

    def is_pressed(self, mouse_event):
        return self.clickable is True and self.rect.x <= mouse_event.x <= \
                self.rect.x + self.rect.width and self.rect.y <= mouse_event.y <= \
                self.rect.y + self.rect.height

    def move_text_x(self, g):
        g.window.remove(self.label)     # avoid invisible object bug
        g.window.add(self.label, x=self.x+self.width/2-self.label.width/2, y=self.label.y)

    def change_text(self, text):
        self.label.text = text

    def change_fill_color(self, color):
        self.rect.filled = True
        self.rect.fill_color = color


class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # background image
        self.background = GImage('background.png')
        self.window.add(self.background, x=0, y=30)

        # Create a paddle
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle = GRect(self.paddle_width, self.paddle_height, x=(self.window.width-self.paddle_width)/2,
                            y=self.window.height-paddle_offset)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius, x=(self.window.width-ball_radius)/2,
                          y=(self.window.height-ball_radius)/2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball)
        self.ball_radius = ball_radius

        # Default initial velocity for the ball
        self.__dx = self.__dy = 0
        self.initialize_x_velocity()
        self.initialize_y_velocity()

        # Initialize our mouse listeners
        onmouseclicked(self.start_game)
        onmousemoved(self.move_paddle)

        # set brick color index
        self.brick_color_index = 0

        # Draw bricks
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_offset = brick_offset
        self.brick_spacing = brick_spacing

        self.initialize_bricks()

        # speed up variables
        self.speedup1 = False
        self.speedup2 = False

        # labels variables
        self.lives = NUM_LIVES
        self.score = 0
        self.max_score = MAX_SCORE
        self.highscore = 0
        self.coin = INITIAL_COIN
        self.skin = {'0': True, '1': False, '2': False, '3': False}     # json will make keys become strings

        # coin object
        self.coin_object = GImage('coin.png')

        # Initialize coin label
        self.coin_label = GLabel('Coin: 0', x=110, y=28)
        self.coin_label.font = 'Helvetica-14-bold'
        self.window.add(self.coin_label)

        # Initialize highscore label
        self.highscore_label = GLabel('Highscore: 0', x=220, y=25)
        self.highscore_label.font = 'Helvetica-12'
        self.window.add(self.highscore_label)

        # Initialize score label
        self.score_label = GLabel('Score: 0', x=5, y=28)
        self.score_label.font = 'Helvetica-14-bold'
        self.window.add(self.score_label)

        # Initialize lives label
        self.life_label = GLabel('Life:', x=550, y=26)
        self.life_label.font = 'Helvetica-12-bold'
        self.window.add(self.life_label)

        # Initialize lives images
        self.lives_dict = {0: GImage('life.png'),
                           1: GImage('life.png'),
                           2: GImage('life.png'),
                           3: GImage('life.png'),
                           4: GImage('life.png')}
        self.refill_lives()

        # Buttons
        self.start_btn = Button('START', START_X, START_Y)
        self.restart_btn = Button('RESTART', RESTART_X, RESTART_Y)
        self.try_again_btn = Button('TRY AGAIN', TRY_AGAIN_X, TRY_AGAIN_Y)
        self.shop_btn = Button('SHOP', SHOP_X, SHOP_Y)

        self.start_btn.change_fill_color('seashell')
        self.restart_btn.change_fill_color('seashell')
        self.try_again_btn.change_fill_color('seashell')
        self.shop_btn.change_fill_color('seashell')

        self.start_btn.show_btn(self)
        self.shop_btn.show_btn(self)

        # Shop-related Buttons
        self.skin0_btn = Button('', RESTART_X+SKIN_OFFSET_X, RESTART_Y-100, width=SKIN_WIDTH, height=SKIN_HEIGHT, small=True)
        self.skin1_btn = Button('$10', RESTART_X+SKIN_OFFSET_X, RESTART_Y, width=SKIN_WIDTH, height=SKIN_HEIGHT, small=True)
        self.skin2_btn = Button('$20', START_X+SKIN_OFFSET_X, START_Y, width=SKIN_WIDTH, height=SKIN_HEIGHT, small=True)
        self.skin3_btn = Button('$30', SHOP_X+SKIN_OFFSET_X, SHOP_Y, width=SKIN_WIDTH, height=SKIN_HEIGHT, small=True)
        self.leave_shop_btn = Button('LEAVE', LEAVE_SHOP_X, LEAVE_SHOP_Y)

        self.skin0_select_btn = Button('USED', self.skin0_btn.x+SKIN_WIDTH/2-SMALL_BUTTON_WIDTH/2,
                                               RESTART_Y-40, width=SMALL_BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT,
                                               small=True)
        self.skin1_select_btn = Button('BUY', self.skin1_btn.x+SKIN_WIDTH/2-SMALL_BUTTON_WIDTH/2, RESTART_Y+60,
                                       width=SMALL_BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, small=True)
        self.skin2_select_btn = Button('BUY', self.skin2_btn.x+SKIN_WIDTH/2-SMALL_BUTTON_WIDTH/2, START_Y+60,
                                       width=SMALL_BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, small=True)
        self.skin3_select_btn = Button('BUY', self.skin3_btn.x+SKIN_WIDTH/2-SMALL_BUTTON_WIDTH/2, SHOP_Y+60,
                                       width=SMALL_BUTTON_WIDTH, height=SMALL_BUTTON_HEIGHT, small=True)

        # Set skin colors
        self.skin_colors = {0: 'black', 1: 'sienna', 2: 'aqua', 3: 'gold'}
        self.skin0_btn.change_fill_color(self.skin_colors[0])
        self.skin1_btn.change_fill_color(self.skin_colors[1])
        self.skin2_btn.change_fill_color(self.skin_colors[2])
        self.skin3_btn.change_fill_color(self.skin_colors[3])

        # set select btns colors
        self.leave_shop_btn.change_fill_color('seashell')
        self.skin0_select_btn.change_fill_color('seashell')
        self.skin1_select_btn.change_fill_color('seashell')
        self.skin2_select_btn.change_fill_color('seashell')
        self.skin3_select_btn.change_fill_color('seashell')

        # Game Over
        self.game_over_label = GLabel('GAME OVER', x=GAME_OVER_X, y=GAME_OVER_Y)
        self.game_over_label.font = 'Helvetica-30-bold'

        # Winning
        self.winning_label = GLabel('YOU WON!', x=WINNING_X, y=WINNING_Y)
        self.winning_label.font = 'Helvetica-30-bold'

        # Status variables
        self.is_running = False
        self.is_game_over = False
        self.is_restart = False
        self.is_coin_dropped = False
        self.is_in_shop = False
        # self.is_winning = False

        # json game data storage
        self.data = {}
        self.fetch_data()
        self.update_coin()
        self.update_highscore()
        # initial values
        # self.data = {'highscore': self.highscore, 'coin': self.coin, 'skin': self.skin}
        # self.skin = {0: True, 1: False, 2: False, 3: False}

        # Skin-related variables
        self.skin_price = {1: PRICE_SKIN1, 2: PRICE_SKIN2, 3: PRICE_SKIN3}
        self.current_skin = 0
        # current skin: '0': original, '1': skin1, '2': skin2, '3': skin3

        # Check if ths user owns skins, change label text from 'BUY' to 'Select'
        if self.data['skin']['1'] is True:
            self.skin1_select_btn.change_text('SELECT')
            self.skin1_select_btn.move_text_x(self)
            self.skin1_btn.change_text('')
        if self.data['skin']['2'] is True:
            self.skin2_select_btn.change_text('SELECT')
            self.skin2_select_btn.move_text_x(self)
            self.skin2_btn.change_text('')
        if self.data['skin']['3'] is True:
            self.skin3_select_btn.change_text('SELECT')
            self.skin3_select_btn.move_text_x(self)
            self.skin3_btn.change_text('')

    def initialize_bricks(self):
        dict_color = [{0: 'red', 1: 'orange', 2: 'yellow', 3: 'green', 4: 'blue'},
                      {0: 'dimgray', 1: 'burlywood', 2: 'lightgoldenrodyellow', 3: 'antiquewhite', 4: 'aliceblue'},
                      {0: 'peachpuff', 1: 'tomato', 2: 'pink', 3: 'plum', 4: 'thistle'}]
        cur_dict_color = dict_color[self.brick_color_index]
        # set brick color dict
        if self.brick_color_index < 2:
            self.brick_color_index += 1
        else:
            self.brick_color_index = 0
        for i in range(self.brick_rows):
            color = cur_dict_color[math.trunc(i/(self.brick_rows/5))]
            for j in range(self.brick_cols):
                brick = GRect(self.brick_width, self.brick_height, x=j*(self.brick_width+self.brick_spacing),
                              y=self.brick_offset+i*(self.brick_height+self.brick_spacing))
                brick.filled = True
                brick.color = brick.fill_color = color
                self.window.add(brick)

    def remove_all_bricks(self):
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                # To avoid invisible paddle bug, check and do not remove background
                if self.window.get_object_at(
                    x=j*(self.brick_width+self.brick_spacing),
                        y=self.brick_offset+i*(self.brick_height+self.brick_spacing)) == self.background:
                    continue
                self.window.remove(self.window.get_object_at(
                    x=j*(self.brick_width+self.brick_spacing),
                    y=self.brick_offset+i*(self.brick_height+self.brick_spacing)))

    def move_paddle(self, e):
        if e.x < self.paddle_width/2:
            self.paddle.x = 0
            return
        if e.x > self.window.width - self.paddle_width/2:
            self.paddle.x = self.window.width - self.paddle_width
            return
        self.paddle.x = e.x - self.paddle_width/2

    def start_game(self, e):
        """
        Every mouse click will call this method. Depending on the status of different status variable (e.g., is_in_shop),
        the click will then be handled differently.
        :param e: mouse event
        :return: None
        """

        if self.is_running:    # if the game is running, do nothing and return
            return
        # Initial START
        if self.is_game_over is False and self.start_btn.is_pressed(e):
            self.remove_all_buttons()
            self.start_btn.clickable = False
            self.is_running = True
        # Main menu (start / shop options)
        if self.is_game_over is False and self.shop_btn.is_pressed(e):
            self.enter_shop()
        # set running to True if game is not over, so that the animation while loop starts running code
        if self.is_game_over is False and self.try_again_btn.is_pressed(e):
            self.remove_all_buttons()
            self.try_again_btn.clickable = False
            self.is_running = True
        # RESTART button is pressed, restart the game
        if self.is_game_over is True and self.restart_btn.is_pressed(e):
            self.remove_all_buttons()
            self.restart_btn.clickable = False
            self.is_restart = True
            self.lives = NUM_LIVES
            self.refill_lives()
            self.score = 0
            self.update_score()
            self.start_btn.show_btn(self)
            self.shop_btn.show_btn(self)
        # User is in the shop
        if self.is_in_shop:
            if self.skin0_select_btn.is_pressed(e):
                self.render_skin(0)
            if self.skin1_select_btn.is_pressed(e):
                self.buy_skin(1)
            if self.skin2_select_btn.is_pressed(e):
                self.buy_skin(2)
            if self.skin3_select_btn.is_pressed(e):
                self.buy_skin(3)
            if self.leave_shop_btn.is_pressed(e):
                self.leave_shop()

    def buy_skin(self, ind):
        i = str(ind)    # string-typed number
        # User does not own the skin and has enough coins to buy it
        if self.coin >= self.skin_price[ind] and self.data['skin'][i] is False:
            self.coin -= self.skin_price[ind]
            self.data['skin'][i] = True
            # update coin and data
            self.update_coin()
            self.update_data()
            # render skin
            self.render_skin(ind)
        # User selects a skin already owned
        elif self.data['skin'][i] is True:
            # render skin
            self.render_skin(ind)

    def render_skin(self, ind):
        i = str(ind)    # string-typed number
        if self.data['skin'][i] is True:  # if the user owns the skin

            # change ball/paddle color
            self.change_ball_paddle_color(ind)

            # change text of current skin to 'SELECT'
            if self.current_skin == 0:
                # self.skin0_btn.change_text('')
                self.skin0_select_btn.change_text('SELECT')
                self.skin0_select_btn.move_text_x(self)
            if self.current_skin == 1:
                self.skin1_select_btn.change_text('SELECT')
                self.skin1_select_btn.move_text_x(self)
            if self.current_skin == 2:
                self.skin2_select_btn.change_text('SELECT')
                self.skin2_select_btn.move_text_x(self)
            if self.current_skin == 3:
                self.skin3_select_btn.change_text('SELECT')
                self.skin3_select_btn.move_text_x(self)

            # update current skin
            self.current_skin = ind

            # change text of updated current skin to 'USED'
            if self.current_skin == 0:
                self.skin0_select_btn.change_text('USED')
                self.skin0_select_btn.move_text_x(self)
            if self.current_skin == 1:
                self.skin1_btn.change_text('')
                self.skin1_select_btn.change_text('USED')
                self.skin1_select_btn.move_text_x(self)
            if self.current_skin == 2:
                self.skin2_btn.change_text('')
                self.skin2_select_btn.change_text('USED')
                self.skin2_select_btn.move_text_x(self)
            if self.current_skin == 3:
                self.skin3_btn.change_text('')
                self.skin3_select_btn.change_text('USED')
                self.skin3_select_btn.move_text_x(self)

    def change_ball_paddle_color(self, ind):
        self.ball.color = self.ball.fill_color = self.paddle.color = self.paddle.fill_color = self.skin_colors[ind]

    def initialize_x_velocity(self):
        # set x velocity randomly
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() < 0.5:
            self.__dx *= -1

    def initialize_y_velocity(self):
        self.__dy = INITIAL_Y_SPEED

    def fetch_data(self):
        try:
            with open('data.txt', 'r') as data_file:
                self.data = load(data_file)
                self.highscore = self.data['highscore']
                self.coin = self.data['coin']
                self.skin = self.data['skin']
        except OSError:     # File not exist
            # initial value
            self.data = {'highscore': self.highscore, 'coin': self.coin, 'skin': self.skin}

    def update_data(self):
        self.data['coin'] = self.coin
        self.data['highscore'] = self.highscore
        self.data['skin'] = self.skin
        with open('data.txt', 'w') as data_file:
            dump(self.data, data_file)

    def remove_all_buttons(self):
        self.start_btn.remove_btn(self)
        self.restart_btn.remove_btn(self)
        self.try_again_btn.remove_btn(self)
        self.shop_btn.remove_btn(self)
        self.leave_shop_btn.remove_btn(self)
        self.skin0_btn.remove_btn(self)
        self.skin1_btn.remove_btn(self)
        self.skin2_btn.remove_btn(self)
        self.skin3_btn.remove_btn(self)
        self.skin0_select_btn.remove_btn(self)
        self.skin1_select_btn.remove_btn(self)
        self.skin2_select_btn.remove_btn(self)
        self.skin3_select_btn.remove_btn(self)

    def game_over(self):
        """
        A method that handles 'game over' or 'start a new game'
        :return: None
        """
        # Enter game over
        if self.is_game_over is False:
            self.is_game_over = True
            self.window.add(self.game_over_label)
            self.window.remove(self.ball)
            # reset y velocity
            self.initialize_y_velocity()
            self.speedup1 = False
            self.speedup2 = False
            # show restart btn
            self.restart_btn.show_btn(self)
            # update highscore
            if self.score > self.highscore:
                self.highscore = self.score
                self.update_highscore()
            self.update_data()

        # Leave game over (New game)
        else:
            self.is_game_over = False
            self.window.remove(self.game_over_label)    # remove game_over if LOST
            self.window.remove(self.winning_label)      # remove winning if WON
            self.remove_all_bricks()
            # self.window.add(self.background)   #remove this line to avoid invisible paddle bug
            self.window.add(self.ball, x=(self.window.width-self.ball_radius)/2,
                            y=(self.window.height-self.ball_radius)/2)
            self.initialize_bricks()
            self.window.add(self.paddle)

    def win_game(self):
        self.is_running = False
        self.is_game_over = True
        self.window.add(self.winning_label)
        self.window.remove(self.ball)
        # reset y velocity
        self.initialize_y_velocity()
        self.speedup1 = False
        self.speedup2 = False
        # show restart btn
        self.restart_btn.show_btn(self)
        # update highscore
        if self.score > self.highscore:
            self.highscore = self.score
            self.update_highscore()
        self.update_data()
        # remove dropping coin
        self.remove_coin()

    def enter_shop(self):
        self.is_in_shop = True      # important, to know whether the user is in the shop
        self.remove_all_buttons()
        self.leave_shop_btn.show_btn(self)
        self.skin0_btn.show_btn(self)
        self.skin1_btn.show_btn(self)
        self.skin2_btn.show_btn(self)
        self.skin3_btn.show_btn(self)
        self.skin0_select_btn.show_btn(self)
        self.skin1_select_btn.show_btn(self)
        self.skin2_select_btn.show_btn(self)
        self.skin3_select_btn.show_btn(self)

    def leave_shop(self):
        self.remove_all_buttons()
        self.is_in_shop = False
        self.start_btn.show_btn(self)
        self.shop_btn.show_btn(self)

    def drop_a_coin(self, x, y):
        self.window.add(self.coin_object, x=x, y=y)
        self.is_coin_dropped = True

    def update_score(self):
        self.score_label.text = 'Score: ' + str(self.score)

    def update_coin(self):
        self.coin_label.text = 'Coin: ' + str(self.coin)

    def update_highscore(self):
        self.highscore_label.text = 'Highscore: ' + str(self.highscore)

    def refill_lives(self):
        for i in range(NUM_LIVES):
            self.window.add(self.lives_dict[i], x=590+i*20, y=8)

    def remove_coin(self):
        self.window.remove(self.coin_object)
        self.is_coin_dropped = False

    # getter functions for other files to get x/y velocity
    def get_x_velocity(self):
        return self.__dx

    def get_y_velocity(self):
        return self.__dy

