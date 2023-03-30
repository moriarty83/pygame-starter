import pygame
from pygame.locals import *

import moderngl
import numpy as np

import os
import sys
import math
from generate_ground import *


pygame.init()


screen = pygame.display.set_mode((1280, 720))
ground = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Lander")

scroll_x_speed = 2.4
scroll_y_speed = 2.4

scroll_height = -1000
player_altitude = 1000
player_rotation_current = 0
player_rotation_new = 0


# BACKGROUND
background_01 = pygame.image.load(os.path.join(
    'assets/backgrounds', 'spr_stars01.png')).convert()
background_01X = 0
background_01X2 = background_01.get_width()
background_01Y = 0
background_01Y2 = background_01.get_height()

# BACKGROUND 2

background_02 = pygame.image.load(os.path.join(
    'assets/backgrounds', 'spr_stars01.png')).convert_alpha()
background_02 = pygame.transform.scale_by(background_02, 2)
background_02X = 0
background_02X2 = background_02.get_width()
background_02Y = 0
background_02Y2 = background_02.get_height()


# GROUND
rows = []
ground_tiles_image = pygame.image.load(os.path.join(
    'assets/spritesheets', 'groundtiles_grayscale.png')).convert_alpha()
groundX = 0
groundX_02 = screen.get_width()


clock = pygame.time.Clock()
running = True
dt = 0

first_load = True

# CREATE PLAYER
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_sprites = [pygame.image.load(os.path.join(
    'assets/spritesheets', 'lander_03_00.png')).convert_alpha(), pygame.image.load(os.path.join(
        'assets/spritesheets', 'lander_03_15.png')).convert_alpha(), pygame.image.load(os.path.join(
            'assets/spritesheets', 'lander_03_30.png')).convert_alpha(), pygame.image.load(os.path.join(
                'assets/spritesheets', 'lander_03_45.png')).convert_alpha(), pygame.image.load(os.path.join(
                    'assets/spritesheets', 'lander_03_60.png')).convert_alpha(), pygame.image.load(os.path.join(
                        'assets/spritesheets', 'lander_03_75.png')).convert_alpha(), pygame.image.load(os.path.join(
                            'assets/spritesheets', 'lander_03_90.png')).convert_alpha(), pygame.image.load(os.path.join(
                                'assets/spritesheets', 'lander_03_105.png')).convert_alpha(), pygame.image.load(os.path.join(
                                    'assets/spritesheets', 'lander_03_120.png')).convert_alpha(), pygame.image.load(os.path.join(
                                        'assets/spritesheets', 'lander_03_135.png')).convert_alpha(), pygame.image.load(os.path.join(
                                            'assets/spritesheets', 'lander_03_150.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                'assets/spritesheets', 'lander_03_165.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                    'assets/spritesheets', 'lander_03_180.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                        'assets/spritesheets', 'lander_03_195.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                            'assets/spritesheets', 'lander_03_210.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                'assets/spritesheets', 'lander_03_225.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                    'assets/spritesheets', 'lander_03_240.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                        'assets/spritesheets', 'lander_03_255.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                            'assets/spritesheets', 'lander_03_270.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                                'assets/spritesheets', 'lander_03_285.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                                    'assets/spritesheets', 'lander_03_300.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                                        'assets/spritesheets', 'lander_03_315.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                                            'assets/spritesheets', 'lander_03_330.png')).convert_alpha(), pygame.image.load(os.path.join(
                                                                                                'assets/spritesheets', 'lander_03_345.png')).convert_alpha()]

for sprite in player_sprites:
    sprite = pygame.transform.scale_by(sprite, 2)
    sprite.set_colorkey("black")


def redrawWindow():
    global player_sprites
    global player_rotation_current
    global player_rotation_new
    # draws our first background_01 image
    screen.blit(background_01, (background_01X, background_01Y))
    screen.blit(background_01, (background_01X2, background_01Y))

    screen.blit(background_01, (background_01X, background_01Y2))
    screen.blit(background_01, (background_01X2, background_01Y2))

    # screen.blit(background_02, (background_02X, background_02Y))
    # # draws the seconf background_02 image
    # screen.blit(background_02, (background_02X2, background_02Y2))
    for i in range(len(rows)):
        screen.blit(
            rows[i]['surface'], (i*32+groundX, screen.get_height()-rows[i]['surface'].get_height()+(scroll_height*-1)))

    active_player_sprite = math.floor(player_rotation_current % 360 / 15)

    screen.blit(player_sprites[active_player_sprite], (player_pos))
    pygame.display.update()  # updates the screen

# screen.get_height()-rows[i]['surface'].get_height()


def updateBackground():
    global player_rotation

    global background_01X
    global background_01X2
    global background_02X
    global background_02X2

    global background_01Y
    global background_01Y2
    global background_02Y
    global background_02Y2

    global groundX

    background_01X -= scroll_x_speed
    background_01X2 -= scroll_x_speed
    background_02X -= scroll_x_speed * 2
    background_02X2 -= scroll_x_speed * 2

    background_01Y -= scroll_y_speed
    background_01Y2 -= scroll_y_speed
    background_02Y -= scroll_y_speed * 2
    background_02Y2 -= scroll_y_speed * 2

    groundX -= scroll_x_speed * 2.5

    if scroll_x_speed > 0:
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

    if scroll_y_speed > 0:
        if background_01Y < background_01.get_height() * -1:
            background_01Y = background_01.get_height()
        if background_01Y2 < background_01.get_height() * -1:
            background_01Y2 = background_01.get_height()
        if background_02Y < background_02.get_height() * -1:
            background_02Y = background_02.get_height()
        if background_02Y2 < background_02.get_height() * -1:
            background_02Y2 = background_02.get_height()
    else:
        if background_01Y > background_01.get_height() * 1:
            background_01Y = -background_01.get_height()
        if background_01Y2 > background_01.get_height() * 1:
            background_01Y2 = -background_01.get_height()
        if background_02Y > background_02.get_height() * 1:
            background_02Y = -background_02.get_height()
        if background_02Y2 > background_02.get_height() * 1:
            background_02Y2 = -background_02.get_height()


while running:
    redrawWindow()
    updateBackground()

    if first_load:
        for i in range(math.ceil(screen.get_width()/32)):
            rows.append(build_ground_col(rows))
        first_load = False
    if len(rows) * 32 < screen.get_width()-32 + groundX*-1:
        rows.append(build_ground_col(rows))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        scroll_y_speed -= 1 * dt

    if keys[pygame.K_s]:
        scroll_y_speed += 1 * dt
    if keys[pygame.K_a]:
        player_rotation_current -= 15

    if keys[pygame.K_d]:
        player_rotation_current += 15

    if (scroll_height >= 0):
        scroll_height = 0
        scroll_y_speed = 0 if scroll_y_speed >= 0 else scroll_y_speed
    scroll_height += scroll_y_speed
    player_altitude -= scroll_y_speed

    pygame.display.update()
    print("pr_current:", player_rotation_current)
    print("pr_new:", player_rotation_new)

    dt = clock.tick(60) / 1000

pygame.quit
