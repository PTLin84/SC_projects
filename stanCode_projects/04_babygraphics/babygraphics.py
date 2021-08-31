"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    spacing = (width - GRAPH_MARGIN_SIZE*2) // len(YEARS)
    return GRAPH_MARGIN_SIZE + spacing * year_index


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################

    top_border_y = GRAPH_MARGIN_SIZE
    bottom_border_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    left_border_x = GRAPH_MARGIN_SIZE
    right_border_x = CANVAS_WIDTH - GRAPH_MARGIN_SIZE

    canvas.create_line(left_border_x, top_border_y, right_border_x, top_border_y)
    canvas.create_line(left_border_x, bottom_border_y, right_border_x, bottom_border_y)

    for ind, year in enumerate(YEARS):
        x = get_x_coordinate(CANVAS_WIDTH, ind)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, bottom_border_y, text=str(year), anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################

    color_ind = 0
    for name in lookup_names:
        if name not in name_data:   # if the name is not in name_data, continue the for loop and go on to the next name
            continue
        nodes = []                  # nodes to connect the dots and draw lines
        for year_ind, year in enumerate(YEARS):
            year = str(year)

            # rank <= 1000
            if str(year) in name_data[name]:
                x = get_x_coordinate(CANVAS_WIDTH, year_ind)
                rank = int(name_data[name][year])
                spacing = (CANVAS_HEIGHT - GRAPH_MARGIN_SIZE*2) / 1000
                y = GRAPH_MARGIN_SIZE + spacing*rank

            # rank > 1000 in that year
            else:
                x = get_x_coordinate(CANVAS_WIDTH, year_ind)
                y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                rank = '*'
            nodes.append((x,y))

            # Add text for every year
            canvas.create_text(x + TEXT_DX, y, text=f'{name} {rank}', anchor=tkinter.SW, fill=COLORS[color_ind])

        # Draw lines, connect adjacent points from nodes
        for i in range(len(nodes)-1):
            canvas.create_line(nodes[i][0], nodes[i][1], nodes[i+1][0], nodes[i+1][1],
                               fill=COLORS[color_ind], width=LINE_WIDTH)

        # Changing color index
        if color_ind < len(COLORS)-1:
            color_ind += 1
        else:
            color_ind = 0


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
