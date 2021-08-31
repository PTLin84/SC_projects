"""
File: 
Name:
----------------------
TODO:
"""

from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gwindow import GWindow
from math import floor


def main():
    """
    Sally the chicken.
    """
    # build window
    window = GWindow(300, 300, title='Sally')
    # build all elements
    eye1 = GOval(15, 15)
    eye2 = GOval(15, 15)
    foot1 = GOval(17, 30)
    foot2 = GOval(17, 30)
    wing1 = GOval(60, 30)
    wing2 = GOval(60, 30)
    face = GOval(120, 120)
    body = GOval(110, 90)
    # build text labels
    title = GLabel('stanCode SC101')
    title.font = '-12'
    name_tag = GLabel('Kyle 21.07.19')
    name_tag.font = '-10'

    # set properties of the elements to filled
    eye1.filled = eye2.filled = face.filled = body.filled = foot1.filled = foot2.filled = wing1.filled = \
        wing2.filled = True
    # set different colors to the elements
    eye1.fill_color = eye2.fill_color = 'black'
    face.fill_color = body.fill_color = wing1.fill_color = wing2.fill_color = 'yellow'
    foot1.fill_color = foot2.fill_color = 'orange'

    # add elements to the window
    window.add(foot1, 150, 210)
    window.add(foot2, 165, 210)
    window.add(body, 105, 130)
    window.add(face, 90, 41)
    window.add(eye1, 132, 71)
    window.add(eye2, 152, 73)
    window.add(wing1, 70, 160)
    window.add(wing2, 180, 160)
    window.add(title, 191, 298)
    window.add(name_tag, 3, 298)
    # draw irregularly shaped mouth
    draw_thick_line([125, 96.5], [152.8, 106.7], 13, 'orangered', 'orangered', window)
    draw_thick_line([152.8, 106.7], [148, 115], 13, 'orangered', 'orangered', window)
    draw_thick_line([148, 115], [123.9, 112], 13, 'orangered', 'orangered', window)


def draw_thick_line(start_position, end_position, size, color, fill_color, window):
    """
    A function that draws thick lines consisted of filled circles.
    :param start_position: An array [x_position, y_position] that indicates starting position.
    :param end_position: An array [x_position, y_position] that indicates ending position.
    :param size: The size of each circle.
    :param color: The color of each circle.
    :param fill_color: The fill_color of each circle.
    :param window: A GWindow object on which the thick lines will be drawn.
    :return: None
    """
    # The numbers of circles required to make the thick line is calculated by the length of the line divided by 12.
    num = floor(((end_position[0] - start_position[0])**2 + (end_position[1] - start_position[1])**2) / 12)
    x = 0
    y = 0
    # A for loop that draws circles from starting point to ending point
    for i in range(num):
        circle = GOval(size, size)      # create a GOval object
        circle.filled = True            # fill the oval
        circle.fill_color = fill_color  # set the fill_color of the oval to designated fill_color
        circle.color = color            # set the color of the oval to designated color
        window.add(circle, start_position[0]+x, start_position[1]+y)    # add the circle to the window
        # increase the value of x and y such that the next circle will be moved a bit towards the ending point
        x += (end_position[0] - start_position[0]) / num
        y += (end_position[1] - start_position[1]) / num


if __name__ == '__main__':
    main()
