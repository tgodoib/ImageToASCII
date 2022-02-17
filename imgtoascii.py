import os
import math
from PIL import Image, ImageDraw, ImageFont
from operator import add


class Node:
    """
    Binary tree used to store the chosen characters based on their density
    """
    def __init__(self, d, c):

        self.density = d
        self.char = c

        self.parent = None
        self.left = None
        self.right = None

    def insert(self, d, c):
        if self.density == d:
            pass
        elif d < self.density:
            if self.left is None:
                self.left = Node(d, c)
                self.left.parent = self
            else:
                self.left.insert(d, c)
        elif d > self.density:
            if self.right is None:
                self.right = Node(d, c)
                self.right.parent = self
            else:
                self.right.insert(d, c)

    def search(self, d):
        if self.density == d:
            return self.char
        elif d < self.density:
            if self.left is None:
                return self.char if d - self.density > self.parent.density - d else self.parent.char
            return self.left.search(d)
        elif d > self.density:
            if self.right is None:
                return self.char if self.density - d > d - self.parent.density else self.parent.char
            return self.right.search(d)


def map_to_255(v, min, max):
    """
    :param v: Value to be converted
    :param min: Min value in old scale
    :param max: Max value in old scale
    :return: Value in the new scale
    """
    return 255 * ((v - min) / (max - min))


def gen_densities():
    """
    For every char in the chosen range (33 to 127 and 192 to 256), generates
    a 10px by 10px image with it written. Then it calculates the average brightness
    and stores it in the binary tree.
    :return: ([(char, density)], min_value, max_value)
    """
    den = []

    for i in (list(range(33, 127)) + list(range(192, 256))):
        im = Image.new("HSV", (10, 10), color="black")
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype("UbuntuMono.ttf", size=10)
        d.text((2.5, 0), chr(i), fill=(0, 0, 255), font=font, align="center")

        density = 0
        for j in range(100):
            density += im.getpixel((j % 10, math.floor(j / 10)))[2] / 100
        den.append((chr(i), density))

    den_s = sorted(den, key=lambda x: x[1])
    return den, den_s[0][1], den_s[len(den_s)-1][1]


def calc_brightness(im, i, j, square_size):
    """
    :param im: Image being converted
    :param i: x index
    :param j: y index
    :param square_size: the sample size
    :return: Brightness of the region beginning in (i, j) with length square_size
    """
    color = [0, 0, 0]
    i = square_size*i
    j = square_size*j

    for a in range(square_size):
        for b in range(square_size):
            color = list(map(add, im.getpixel((i + a, j + b)), color))

    return (color[0] + color[1] + color[2]) / (3 * square_size ** 2)


def get_text(img, cols):
    """
    :param img: Image being converted
    :param cols: How many chars should be in one line
    :return: An array containing the lines of the text
    """
    chars, min_brightness, max_brightness = gen_densities()
    tree = Node(map_to_255(chars[0][1], min_brightness, max_brightness), chars[0][0])
    for c in chars:
        tree.insert(map_to_255(c[1], min_brightness, max_brightness), c[0])

    im = Image.open("images/" + img)
    im = im.resize((500, int((500 / im.size[0]) * im.size[1])), Image.ANTIALIAS)

    square_size = im.size[0] // cols
    lines = im.size[1] // square_size

    text = []
    for j in range(0, lines):
        line = ""
        for i in range(0, cols):
            line += tree.search(calc_brightness(im, i, j, square_size))
        text.append(line)

    os.remove("images/" + img)

    return text
