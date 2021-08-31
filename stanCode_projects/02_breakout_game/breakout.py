"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

File: breakout_v2.0.py
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

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
import random


FRAME_RATE = 1000 / 120                 # 120 frames per second
SPEEDUP_SCORE1 = 50
SPEEDUP_SCORE2 = 100

# global variables
graphics = BreakoutGraphics()   # initialize game
dx = graphics.get_x_velocity()  # x velocity
dy = graphics.get_y_velocity()  # y velocity


def main():
    global graphics, dx, dy

    # Add animation loop here!
    while True:
        pause(FRAME_RATE)   # control while loop run time

        # check running, if not running, do nothing
        if not graphics.is_running:
            # if lives equal 0, game over
            if graphics.lives == 0 and graphics.is_game_over is False:
                graphics.game_over()
            # if restart is pressed, restart the game (call game_over again)
            if graphics.is_restart:
                graphics.is_restart = False
                graphics.game_over()
                # reset velocity
                dx = graphics.get_x_velocity()  # x velocity
                dy = graphics.get_y_velocity()  # y velocity
            continue        # if lives is not 0, continue the while loop and wait for user clicks

        # check winning
        if graphics.score == graphics.max_score:
            graphics.win_game()
        # check x-direction collision (with the left/right walls of the GWindow)
        if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
            change_x_direction()
        # check y-direction collision (with the top wall of the GWindow, below the score and lives labels)
        if graphics.ball.y <= 40:
            change_y_direction()
        # if fail to catch the ball with the paddle (lose a life)
        if graphics.ball.y >= graphics.window.height:
            graphics.is_running = False
            graphics.ball.x = (graphics.window.width-graphics.ball_radius)/2
            graphics.ball.y = (graphics.window.height-graphics.ball_radius)/2
            # remove a heart image
            graphics.lives -= 1
            graphics.window.remove(graphics.lives_dict[graphics.lives])
            # remove dropping coin
            graphics.remove_coin()
            # reset ball position and velocity
            graphics.initialize_x_velocity()      # only x velocity is reset
            dx = graphics.get_x_velocity()
            # show try again button
            if graphics.lives > 0:
                graphics.try_again_btn.show_btn(graphics)

        # if score reach 50, speed up
        if graphics.score >= SPEEDUP_SCORE1 and graphics.speedup1 is False:
            dy *= 1.5
            graphics.speedup1 = True
        if graphics.score >= SPEEDUP_SCORE2 and graphics.speedup2 is False:
            dy *= 1.5
            graphics.speedup2 = True

        # check collision with GObjects
        check_collision(graphics)

        # update score
        graphics.update_score()

        # move the ball by (dx, dy)
        graphics.ball.move(dx, dy)

        # move the coin by (x, y) if there is a coin
        if graphics.is_coin_dropped:

            if graphics.window.get_object_at(
                    graphics.coin_object.x + graphics.coin_object.width/2,
                    graphics.coin_object.y + graphics.coin_object.height + 1) == graphics.paddle:
                graphics.coin += 1
                graphics.update_coin()
                graphics.window.remove(graphics.coin_object)
                graphics.is_coin_dropped = False
            if graphics.coin_object.y >= graphics.window.height:
                graphics.window.remove(graphics.coin_object)
                graphics.is_coin_dropped = False
            graphics.coin_object.move(0, 5)


def check_collision(g):
    global dx, dy
    # using GWindow.get_object_at to get object (if any) on the four corners of the ball
    corners = [g.window.get_object_at(g.ball.x, g.ball.y),
              g.window.get_object_at(g.ball.x + g.ball.width, g.ball.y),
              g.window.get_object_at(g.ball.x, g.ball.y + g.ball.height),
              g.window.get_object_at(g.ball.x + g.ball.width, g.ball.y + g.ball.height)]
    # 0: upper_left_corner, 1: upper_right_corner, 2: lower_left_corner, 3: lower_right_corner

    # if the object on the corners of the ball is the paddle
    if g.paddle in corners:
        # check that the ball is on top of the paddle
        if g.ball.y + g.ball.height <= g.paddle.y + abs(dy):
            change_y_direction()
    elif g.score_label in corners or g.coin_object in corners or g.coin_label in corners \
            or g.highscore_label in corners or g.life_label in corners:
        pass
    # if the object on the corners of the ball is not the paddle, score, lives labels (i.e., bricks)
    # at least two corners hit an object other than the background image
    elif corners.count(graphics.background) <= 2:
        if (corners[0] and corners[1]) is not graphics.background:   # change y direction if the top two corners are hit
            change_y_direction()
        if (corners[2] and corners[3]) is not graphics.background:   # change y direction if the bottom two corners are hit
            change_y_direction()
        if corners[0] and corners[2] is not graphics.background:   # change x direction if the left two corners are hit
            change_x_direction()
        if corners[1] and corners[3] is not graphics.background:   # change x direction if the right two corners are hit
            change_x_direction()
        remove_bricks(corners)
    # only one corner hit an object other than the background image
    elif corners.count(graphics.background) == 3:
        # find corner of the brick
        # calc x/y distance
        # decides change x/y direction
        for i in range(3):
            corners.remove(graphics.background)
        # len(corners) becomes 1, corners[0] == the brick hit
        find_reflect_dir(corners[0], g)
        remove_bricks(corners)


def find_reflect_dir(brick, g):
    brick_corners = [[brick.x, brick.y],
                     [brick.x+brick.width, brick.y],
                     [brick.x, brick.y+brick.height],
                     [brick.x+brick.width, brick.y+brick.height]]
    # ball in last frame (right before collision)
    ball_center_x = g.ball.x + g.ball.width/2 - dx
    ball_center_y = g.ball.y + g.ball.height/2 - dy
    distance = float('inf')

    for corner in brick_corners:
        if calc_x_distance(ball_center_x, corner[0]) + calc_y_distance(ball_center_y, corner[1]) < distance:
            distance = calc_x_distance(ball_center_x, corner[0]) + calc_y_distance(ball_center_y, corner[1])
            closest_corner = corner

    if calc_x_distance(closest_corner[0], ball_center_x) > calc_y_distance(closest_corner[1], ball_center_y):
        change_x_direction()
    else:
        change_y_direction()


def remove_bricks(corners):
    # use set to create unique list
    uniq_corners = set(corners)
    for brick in uniq_corners:
        if brick != graphics.background and brick is not None:  # remove object that is not background
            graphics.window.remove(brick)
            graphics.score += 1

            # When score + 1, randomly drop a coin (1 in 100 score)
            if random.random() < 0.2 and graphics.is_coin_dropped is False:
                graphics.drop_a_coin(brick.x + brick.width/2 - graphics.coin_object.width/2,
                                     brick.y + brick.height/2 - graphics.coin_object.height/2)


def calc_x_distance(x1, x2):
    return abs(x1-x2)


def calc_y_distance(y1, y2):
    return abs(y1-y2)


def change_x_direction():
    global dx
    dx = -dx


def change_y_direction():
    global dy
    dy = -dy


if __name__ == '__main__':
    main()
