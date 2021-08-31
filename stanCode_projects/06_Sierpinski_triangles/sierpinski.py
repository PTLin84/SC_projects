"""
File: sierpinski.py
Name: 林柏廷 Kyle
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause

# Constants
ORDER = 6                  # Controls the order of Sierpinski Triangle
LENGTH = 600               # The length of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150		   # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100         # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950         # The width of the GWindow
WINDOW_HEIGHT = 700        # The height of the GWindow

# Global Variable
window = GWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)  # The canvas to draw Sierpinski Triangle


def main():
	"""
	TODO:
	"""
	sierpinski_triangle(ORDER, LENGTH, UPPER_LEFT_X, UPPER_LEFT_Y)


def sierpinski_triangle(order, length, upper_left_x, upper_left_y):
	"""
	:param order:
	:param length:
	:param upper_left_x:
	:param upper_left_y:
	:return:
	"""
	# base case
	if order == 0:
		return
	# recursive case
	else:
		draw_triangle(upper_left_x, upper_left_y, length)
		sierpinski_triangle(order-1, length/2, upper_left_x, upper_left_y)		# upper left triangle
		sierpinski_triangle(order-1, length/2, upper_left_x+length/2, upper_left_y)		# upper right triangle
		sierpinski_triangle(order-1, length/2, upper_left_x+length/4, upper_left_y+length*0.5*0.866) # bottom triangle


def draw_triangle(x, y, side_length):
	line1 = GLine(x, y, x+side_length, y)
	line2 = GLine(x, y, x+side_length/2, y+side_length*0.866)
	line3 = GLine(x+side_length, y, x+side_length/2, y+side_length*0.866)
	window.add(line1)
	window.add(line2)
	window.add(line3)


if __name__ == '__main__':
	main()