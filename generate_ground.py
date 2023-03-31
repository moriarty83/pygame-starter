import pygame
import os
import random

pygame.init()

ground = pygame.display.set_mode((1280, 720))


ground_tiles_image = pygame.image.load(os.path.join(
    'assets/spritesheets', 'groundtiles_grayscale.png')).convert_alpha()

tiles = {
    "flat": [32, 0],
    "up_steep": [224, 0],
    "down_steep": [192, 0],
    "up_gentle_start": [192, 64],
    "down_gentle_start": [128, 64],
    "up_gentle_continue": [224, 64],
    "down_gentle_continue": [160, 64],
    "inside": [128, 0]
}

up_flat_tiles = {
    "flat": [32, 0],
    "up_steep": [224, 0],
    "up_gentle_start": [192, 64],
}

down_flat_tiles = {
    "flat": [32, 0],
    "down_steep": [192, 0],
    "down_gentle_start": [128, 64],
}


def get_ground_tile(sheet, type):

    # Types:
    width = 32
    height = 32

    image = pygame.Surface((width, height))
    image = image.convert_alpha()
    image.set_colorkey("black")
    # blit argument 1: image, 2: reder coords, 3: coords from spriteshhet
    image.blit(sheet, (0, 0), (tiles[type][0], tiles[type]
               [1], tiles[type][0]+32, tiles[type][1]+32))
    return image


def build_ground_col(rows):

    global makingRow
    makingRow = True

    toppings = dict(list(tiles.items())[:5])
    height = 8
    topper = random.choice(list(toppings.keys()))
    firstRow = False if len(rows) > 0 else True
    if firstRow == False:
        height = rows[-1]["height"]
        if height > 14:
            topper = random.choice(list(down_flat_tiles.keys()))
        if height < 4:
            topper = random.choice(list(up_flat_tiles.keys()))

        proceed = True if random.randint(
            0, 10) > 3 and height < 15 and height > 3 else False
        gentleSlope = True if firstRow == False and rows[-1]["topper"] == "up_gentle_start" or firstRow == False and rows[-1]["topper"] == "down_gentle_start" else False
        if rows[-1]["topper"] == "up_gentle_start":
            topper = "up_gentle_continue"
        elif rows[-1]["topper"] == "down_gentle_start":
            topper = "down_gentle_continue"

        elif proceed == True or gentleSlope == True:

            if rows[-1]["topper"] == "up_steep":
                topper = "up_steep"
                height += 1
            elif rows[-1]["topper"] == "down_steep":
                topper = "down_steep"
                height -= 1

            elif rows[-1]["topper"] == "up_gentle_continue":
                height += 1
                topper = "up_gentle_start"
            elif rows[-1]["topper"] == "down_gentle_continue":
                height -= 1
                topper = "down_gentle_start"
            else:
                topper = rows[-1]["topper"]
            if height < 3:
                topper = "flat"
                height = 3
            if height > 15:
                topper = "flat"
                height = 15

        elif proceed == False and firstRow == False:
            if rows[-1]["topper"] == "flat":
                if topper == "up_steep" or topper == "up_gentle_start":
                    height += 1
            elif rows[-1]["topper"] == "up_steep" or rows[-1]["topper"] == "up_gentle_continue":
                if topper == "up_steep" or topper == "up_gentle_start":
                    height += 1
            elif rows[-1]["topper"] == "down_steep" or rows[-1]["topper"] == "down_gentle_continue":
                if topper != "up_steep" and topper != "up_gentle_start":

                    height -= 1

    surface = pygame.Surface((32, (height+23)*32))
    for i in range(height+23, -1, -1):
        if i != 0:
            type = "inside"
        else:
            type = topper
        tile = get_ground_tile(ground_tiles_image, type)
        surface.blit(tile, (0, i*32))
    col = {"surface": surface, "height": height, "topper": topper}

    return col
