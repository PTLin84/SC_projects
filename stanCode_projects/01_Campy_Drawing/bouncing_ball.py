"""
File: 
Name:
-------------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GLabel
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

# Constants
VX = 3
DELAY = 15
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40

# global variables
running = False                                         # the current status of the program (True: a ball is bouncing)
num_run = 0                                             # the number of runs made
window = GWindow(800, 500, title='bouncing_ball.py')    # a GWindow object
count = GLabel('No. of runs: 0', x=710, y=20)           # a GLabel object that shows current number of runs
count.font = "SansSerif-10"                             # set font style


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    window.add(count)               # add the counting label to the window
    onmouseclicked(bouncing_ball)   # listen to mouse click and call bouncing_ball


def bouncing_ball(e):
    """
    This is a callback function that implement the animation of a bouncing ball.
    :param e: instance of Class "campy.gui.events.mouse.GMouseEvent"
    :return: None
    """
    # global variables that show the status of the program and the number of runs
    global running, num_run
    # return and do nothing if the user clicks when (1) a ball is still bouncing (2) bouncing ball has run 3 times
    if running or num_run >= 3:
        return
    # check if there is a ball at the starting position (which happens if it is not first run)
    check_ball = window.get_object_at(START_X+SIZE/2, START_Y+SIZE/2)
    if check_ball is not None:
        window.remove(check_ball)   # remove the ball at the starting position (created in last call)
    # a new ball is created every time for bouncing
    ball = create_ball()
    window.add(ball)
    # change current status to 'running' and start the animation
    running = True
    # assign initial speed in y-direction
    vy = 0

    # animation part inside the below while loop
    while True:
        # if the ball hit the bottom horizontal line of the window, change the direction of vy
        if ball.y+SIZE >= window.height and vy > 0:     # vy > 0 makes sure the direction of vy changes only once
            vy = -REDUCE*vy     # REDUCE is a coefficient that simulates the effect of non-elastic collisions
        # if the ball hit the right vertical line of the window, end the animation
        if ball.x >= window.width:
            num_run += 1    # number of runs +1
            count.text = 'No. of runs: ' + str(num_run)     # update the counting label
            running = False     # change current status to 'NOT running'
            window.remove(ball)     # remove the ball
            ball = create_ball()    # create a new ball and put it at starting position
            window.add(ball)
            break
        ball.move(VX, vy+GRAVITY)   # normally, the ball moves when the ball has not hit the boundaries of the window
        vy += GRAVITY   # speed in y-direction accelerates by GRAVITY every time
        pause(DELAY)    # slow down the while-loop to make it visible to human eyes


def create_ball():
    """
    :return: A new ball initially at (X, Y) = (START_X, START_Y) (type: GOval object)
    """
    ball = GOval(SIZE, SIZE, x=START_X, y=START_Y)
    ball.filled = True
    ball.fill_color = 'black'
    return ball


if __name__ == "__main__":
    main()
