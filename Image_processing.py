
from tkinter import *
from PIL import Image, ImageTk
import os
from draw import *

def rotatePicture(sourceImagePath, targetImagePath):
    img = Image.open(sourceImagePath)  # .convert("L") optional on black and white, in default its with color.
    w, h = img.size
    new_img = img.copy()
    mat = img.load()
    mat_2 = new_img.load()
    for i in range(w):  # Image manipulation for 180 rotate
        for j in range(h):
            mat_2[i, j] = mat[w - i - 1, h - j - 1]
    if targetImagePath != "":  # At all functions, when function gets empty saving path it returns processed image only
        new_img.save(targetImagePath)
    else:
        return new_img


def mirrorPicture(sourceImagePath, targetImagePath):
    img = Image.open(sourceImagePath)  # .convert("L")
    w, h = img.size
    new_img = img.copy()
    mat = img.load()
    mat_2 = new_img.load()
    for i in range(w):
        for j in range(h):  # Image manipulation for width reverse
            mat_2[i, j] = mat[w - i - 1, j]
    if targetImagePath != "":
        new_img.save(targetImagePath)
    else:
        return new_img


def resizePicture(sourceImagePath, targetImagePath):
    img = Image.open(sourceImagePath).convert("L")
    w, h = img.size
    new_img_re = Image.new("L", (int(w / 2), int(h / 2)))  # New image with smaller size.
    mat = img.load()
    mat_2 = new_img_re.load()
    for i in range(int(w / 2)):  # Running on half of both ranges, because the picture size will reduce to quarter size
        for j in range(int(h / 2)):  # Average of 4 pixels
            mat_2[i, j] = (mat[i * 2, j * 2] + mat[i * 2 + 1, j * 2] + mat[i * 2, j * 2 + 1] + mat[
                i * 2 + 1, j * 2 + 1]) // 4
    if targetImagePath != "":
        new_img_re.save(targetImagePath)
    else:
        return new_img_re


def edge(sourceImagePath, targetImagePath, threshold):
    img = Image.open(sourceImagePath).convert("L")
    w, h = img.size
    img_edg = img.copy()
    mat = img.load()
    mat_2 = img_edg.load()
    for i in range(h):
        for j in range(w):
            if i == 0 and j != 0:  # For the first line of pixels checking left pixel or down pixel
                if abs(mat[j, i] - mat[j - 1, i]) > threshold or abs(mat[j, i] - mat[j, i + 1]) > threshold:
                    mat_2[j, i] = 255
                else:
                    mat_2[j, i] = 0
            elif j == 0 and i != 0:  # For first column of pixels checking right pixel or up pixel
                if abs(mat[j, i] - mat[j + 1, i]) > threshold or abs(mat[j, i] - mat[j, i - 1]) > threshold:
                    mat_2[j, i] = 255
                else:
                    mat_2[j, i] = 0
            elif j == 0 and i == 0:  # Checking first left high corner pixel
                if abs(mat[j, i] - mat[j + 1, i]) > threshold or abs(mat[j, i] - mat[j, i + 1]) > threshold:
                    mat_2[j, i] = 255
                else:
                    mat_2[j, i] = 0
            else:  # For all other pixels checking left pixel or up pixel
                if abs(mat[j, i] - mat[j - 1, i]) > threshold or abs(mat[j, i] - mat[j, i - 1]) > threshold:
                    mat_2[j, i] = 255
                else:
                    mat_2[j, i] = 0
    if targetImagePath != "":
        img_edg.save(targetImagePath)
    else:
        return img_edg


# greyscale function converts image to grey values with pixel manipulation.
def grayscale(sourceImagePath, targetImagePath):
    image = Image.open(sourceImagePath)
    width, height = image.size
    # Create new Image and a Pixel Map
    new = Image.new("RGB", (width, height), "white")
    pixels = new.load()

    # Transform to grayscale
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)  # Get Pixel
            # Get R, G, B values (This are int from 0 to 255)
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            # Transform to grayscale, gray values
            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

            # Set Pixel in new image
            pixels[i, j] = (int(gray), int(gray), int(gray))

    if targetImagePath != "":
        new.save(targetImagePath)
    else:
        return new


# Return color value depending on quadrant and saturation used in dither function.
def get_saturation(value, quadrant):
    if value > 223:
        return 255
    elif value > 159:
        if quadrant != 1:
            return 255

        return 0
    elif value > 95:
        if quadrant == 0 or quadrant == 3:
            return 255

        return 0
    elif value > 32:
        if quadrant == 1:
            return 255

        return 0
    else:
        return 0


def get_pixel(image, i, j):  # Get the pixel from the given image, used in dither function
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None
    pixel = image.getpixel((i, j))
    return pixel


# Create a dithered version of the image.
# "Heavy" function please try on one file at a time, works depend on original pic size
def dither(sourceImagePath, targetImagePath):
    image = Image.open(sourceImagePath)
    width, height = image.size

    # Create new Image and a Pixel Map
    new = Image.new("RGB", (width, height), "white")
    pixels = new.load()

    for i in range(0, width, 2):  # Transform to half tones
        for j in range(0, height, 2):
            # Get Pixels
            p1 = get_pixel(image, i, j)
            p2 = get_pixel(image, i, j + 1)
            p3 = get_pixel(image, i + 1, j)
            p4 = get_pixel(image, i + 1, j + 1)

            # Color Saturation by RGB channel
            red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
            green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
            blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

            # Results by channel
            r = [0, 0, 0, 0]
            g = [0, 0, 0, 0]
            b = [0, 0, 0, 0]

            # Get Quadrant Color
            for x in range(0, 4):
                r[x] = get_saturation(red, x)
                g[x] = get_saturation(green, x)
                b[x] = get_saturation(blue, x)

            # Set Dithered Colors
            pixels[i, j] = (r[0], g[0], b[0])
            pixels[i, j + 1] = (r[1], g[1], b[1])
            pixels[i + 1, j] = (r[2], g[2], b[2])
            pixels[i + 1, j + 1] = (r[3], g[3], b[3])
    if targetImagePath != "":
        new.save(targetImagePath)
    else:
        return new


def watermark(sourceImagePath, targetImagePath):
    temp_path='temp.png'
    if targetImagePath =="":
        mask_path=draw(sourceImagePath)
        command='python test.py --image '+sourceImagePath+' --mask '+mask_path+' --output '+temp_path+' --checkpoint_dir model_logs/release_places2_256'
        #os.system(
        #    'python test.py --image examples/places2/case1_input.png --mask examples/places2/case1_mask.png --output examples/places2/case1_output.png --checkpoint_dir model_logs/release_places2_256')
        os.system(command)
    image = Image.open(temp_path)
    if targetImagePath != "":
        image.save(targetImagePath)
    else:
        return image