import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))
ground = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Lander")

# BACKGROUND
background_01 = pygame.image.load(os.path.join(
    'assets/backgrounds', 'spr_stars01.png')).convert()
background_01X = 0
background_01X2 = background_01.get_width()

# BACKGROUND 2
xspeed = 2.4
background_02 = pygame.image.load(os.path.join(
    'assets/backgrounds', 'spr_stars01.png')).convert_alpha()
background_02 = pygame.transform.scale_by(background_02, 2)
background_02X = 0
background_02X2 = background_02.get_width()

# GROUND
rows = []
ground_tiles_image = pygame.image.load(os.path.join(
    'assets/spritesheets', 'groundtiles_grayscale.png')).convert_alpha()
groundX = 0
groundX_02 = screen.get_width()
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
    "down_steep": [224, 0],
    "down_gentle_start": [192, 64],
}

clock = pygame.time.Clock()
running = True
dt = 0

first_load = True

lines = []

# CREATE PLAYER
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# SET START GROUND COORDINATE
ground_start = pygame.Vector2(0, screen.get_height()*3 / 4)


def redrawWindow():
    # draws our first background_01 image
    screen.blit(background_01, (background_01X, 0))
    # draws the seconf background_01 image
    screen.blit(background_01, (background_01X2, 0))
    screen.blit(background_02, (background_02X, 0))
    # # draws the seconf background_02 image
    screen.blit(background_02, (background_02X2, 0))
    for i in range(len(rows)):
        screen.blit(
            rows[i]['surface'], (i*32+groundX, screen.get_height()-rows[i]['surface'].get_height()))
    # pygame.display.update()  # updates the screen


def updateBackground():
    global background_01X
    global background_01X2
    global background_02X
    global background_02X2
    global groundX

    background_01X -= xspeed
    background_01X2 -= xspeed
    background_02X -= xspeed * 2
    background_02X2 -= xspeed * 2
    groundX -= xspeed * 2.5

    if xspeed > 0:
        if background_01X < background_01.get_width() * -1:
            background_01X = background_01.get_width()
        if background_01X2 < background_01.get_width() * -1:
            background_01X2 = background_01.get_width()
        if background_02X < background_02.get_width() * -1:
            background_02X = background_02.get_width()
        if background_02X2 < background_02.get_width() * -1:
            background_02X2 = background_02.get_width()
    else:
        if background_01X > background_01.get_width() * 1:
            background_01X = -background_01.get_width()
        if background_01X2 > background_01.get_width() * 1:
            background_01X2 = -background_01.get_width()
        if background_02X > background_02.get_width() * 1:
            background_02X = -background_02.get_width()
        if background_02X2 > background_02.get_width() * 1:
            background_02X2 = -background_02.get_width()


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


def generate_new_col(forward=True):
    previousCol = rows[-1]


def build_ground_col():
    toppings = dict(list(tiles.items())[:5])
    height = 8
    topper = random.choice(list(toppings.keys()))
    firstRow = False if len(rows) > 0 else True
    if firstRow == False:
        height = rows[-1]["height"]

        proceed = True if random.randint(0, 10) > 3 else False
        gentleSlope = True if firstRow == False and rows[-1]["topper"] == "up_gentle_start" or firstRow == False and rows[-1]["topper"] == "down_gentle_start" else False
        print("proceed: ", proceed)
        if proceed == True or gentleSlope == True:
            if rows[-1]["topper"] == "up_steep":
                topper = "up_steep"
                height += 1
            elif rows[-1]["topper"] == "down_steep":
                topper = "down_steep"
                height -= 1
            if rows[-1]["topper"] == "up_gentle_start":
                topper = "up_gentle_continue"
            elif rows[-1]["topper"] == "down_gentle_start":
                topper = "down_gentle_continue"
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
            print("proceed false, topper is: ", topper)
            if rows[-1]["topper"] == "flat":
                if topper == "up_steep" or topper == "up_gentle_start":
                    height += 1
            elif rows[-1]["topper"] == "up_steep" or rows[-1]["topper"] == "up_gentle_continue":
                if topper == "up_steep" or topper == "up_gentle_start":
                    height += 1
            elif rows[-1]["topper"] == "down_steep" or rows[-1]["topper"] == "down_gentle_continue":
                if topper != "up_steep" or topper != "up_gentle_start":
                    height -= 1
                else:
                    print("topper is upsteep, up gentle or flat")

    surface = pygame.Surface((32, height*32))
    for i in range(height):
        if i != 0:
            type = "inside"
        else:
            type = topper
        tile = get_ground_tile(ground_tiles_image, type)
        surface.blit(tile, (0, i*32))
    col = {"surface": surface, "height": height, "topper": topper}
    return col


while running:
    redrawWindow()
    updateBackground()

    if first_load:
        for i in range(math.ceil(screen.get_width()/32)):
            rows.append(build_ground_col())
        first_load = False
    if len(rows) * 32 < screen.get_width()/2 + groundX*-1:
        rows.append(build_ground_col())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt

    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        xspeed -= 1 * dt

    if keys[pygame.K_d]:
        xspeed += 1 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit
