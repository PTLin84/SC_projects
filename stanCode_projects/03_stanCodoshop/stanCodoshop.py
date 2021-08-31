"""
File: stanCodoshop.py
Name: 林柏廷
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------

TODO:
Given several images in a directory, this program returns an image without pedestrians or other moving objects.
(Note that the images should have the same width and height. To get the best performance, all images should be taken
from the exact same position, that means the camera should not move between images.)
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (float): color distance between red, green, and blue pixel values

    """
    return ((pixel.red - red)**2 + (pixel.green - green)**2 + (pixel.blue - blue)**2)**0.5


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    sum_red = sum_green = sum_blue = 0
    # Add up r, g, b values in all pixels
    for pixel in pixels:
        sum_red += pixel.red
        sum_green += pixel.green
        sum_blue += pixel.blue
    num_pixels = len(pixels)
    # Return average r, g, b values, which are the sums divided by the number of pixels (use '//' to get int values)
    return [sum_red//num_pixels, sum_green//num_pixels, sum_blue//num_pixels]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    # The pixel that has the smallest color distance to the average_rgb is the best pixel
    min_distance = float('inf')
    average_rgb = get_average(pixels)   # [r, g, b]
    for pixel in pixels:
        distance = get_pixel_dist(pixel, *average_rgb)
        if distance < min_distance:     # Use '*' to unpack the list
            min_distance = distance
            best_pixel = pixel
    return best_pixel


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    ######## YOUR CODE STARTS HERE #########
    # Write code to populate image and create the 'ghost' effect

    # Use double for loop to go through every pixel in the result image
    for x in range(result.width):
        for y in range(result.height):
            pixel = result.get_pixel(x, y)      # get the pixel object on the blank result image
            original_pixels = []                # initialize a list that stores all pixels at (x,y)
            for image in images:                # put all pixels at (x,y) in all images into the list
                original_pixels.append(image.get_pixel(x, y))   # [pixel_img1(x,y), pixel_img2(x,y), pixel_img3(x,y)]

            best_pixel = get_best_pixel(original_pixels)    # use get_best_pixel function to get the best pixel
            # change the r, g, b values of the result pixel at (x,y) to that of best_pixel
            pixel.red = best_pixel.red
            pixel.green = best_pixel.green
            pixel.blue = best_pixel.blue

    ######## YOUR CODE ENDS HERE ###########
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
