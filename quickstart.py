import pygame
from pygame.locals import *

import os
import math
from generate_ground import *
from player import *


pygame.init()
all_sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((1280, 720))
ground = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Lander")

scroll_x_speed = 0
scroll_y_speed = 0

scroll_height = -1000


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
gravity = 1


clock = pygame.time.Clock()
running = True
dt = 0

first_load = True

# CREATE PLAYER
player = Player(screen)


def redrawWindow():

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
            rows[i].surface, (i*32+groundX, screen.get_height()-rows[i].surface.get_height()+(23*32)+(scroll_height*-1)))
        rows[i].rect = (i*32+groundX, screen.get_height() -
                        rows[i].surface.get_height()+(23*32)+(scroll_height*-1), 32, 32)
        pygame.draw.rect(screen, "blue", (rows[i].rect), width=3)

    screen.blit(player.active_sprite, (player.position))
    pygame.draw.rect(screen, "red", (player.rect), width=3)

    pygame.display.update()  # updates the screen

# screen.get_height()-rows[i]['surface'].get_height()


def updateBackground():

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
            new_row = GroundColSprite(rows)
            rows.append(new_row)
            ground_sprites.add(new_row)
        first_load = False
    if len(rows) * 32 < screen.get_width()-32 + groundX*-1:
        new_row = GroundColSprite(rows)
        rows.append(new_row)
        ground_sprites.add(new_row)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        thrust = player.calculate_thrust()
        scroll_y_speed += 3 * dt * thrust.y
        scroll_x_speed += 3 * dt * thrust.x

    if keys[pygame.K_s]:
        thrust = player.calculate_thrust()
        scroll_y_speed -= 3 * dt * thrust.y
        scroll_x_speed -= 3 * dt * thrust.x
    if keys[pygame.K_a]:
        player.rotate(-15)

    if keys[pygame.K_d]:
        player.rotate(15)

    scroll_height += scroll_y_speed
    scroll_y_speed += 1 * dt * gravity

    pygame.display.update()

    collision = pygame.sprite.spritecollideany(player, ground_sprites)
    print(rows[0].rect)

    dt = clock.tick(60) / 1000

pygame.quit
