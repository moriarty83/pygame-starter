import pygame
import os
import random

pygame.init()

ground = pygame.display.set_mode((1280, 720))

ground_sprites = pygame.sprite.Group()

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

toppings = dict(list(tiles.items())[:5])


class GroundSprite(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__()
        self.width = 32
        self.height = 32
        self.sheet = ground_tiles_image
        self.image = pygame.Surface((self.width, self.height))

        self.type = args[1]
        self.image = self.image.convert_alpha()
        self.image.set_colorkey("black")
        self.type = args[1]
        self.image.blit(self.sheet, (0, 0), (tiles[self.type][0], tiles[self.type]
                                             [1], tiles[self.type][0]+32, tiles[self.type][1]+32))
        self.rect = self.image.get_rect()


class GroundColSprite(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__()
        self.rows = args[0]
        self.height = 8
        self.topper = random.choice(list(toppings.keys()))
        self.first_row = False if len(self.rows) > 0 else True
        if self.first_row == False:
            self.height = self.rows[-1].height
            if self.height > 14:
                self.topper = random.choice(list(down_flat_tiles.keys()))
            if self.height < 4:
                self.topper = random.choice(list(up_flat_tiles.keys()))

            proceed = True if random.randint(
                0, 10) > 3 and self.height < 15 and self.height > 3 else False
            gentleSlope = True if self.first_row == False and self.rows[
                -1].topper == "up_gentle_start" or self.first_row == False and self.rows[-1].topper == "down_gentle_start" else False
            if self.rows[-1].topper == "up_gentle_start":
                self.topper = "up_gentle_continue"
            elif self.rows[-1].topper == "down_gentle_start":
                self.topper = "down_gentle_continue"

            elif proceed == True or gentleSlope == True:

                if self.rows[-1].topper == "up_steep":
                    self.topper = "up_steep"
                    self.height += 1
                elif self.rows[-1].topper == "down_steep":
                    self.topper = "down_steep"
                    self.height -= 1

                elif self.rows[-1].topper == "up_gentle_continue":
                    self.height += 1
                    self.topper = "up_gentle_start"
                elif self.rows[-1].topper == "down_gentle_continue":
                    self.height -= 1
                    self.topper = "down_gentle_start"
                else:
                    self.topper = self.rows[-1].topper
                if self.height < 3:
                    self.topper = "flat"
                    self.height = 3
                if self.height > 15:
                    self.topper = "flat"
                    self.height = 15

            elif proceed == False and self.first_row == False:
                if self.rows[-1].topper == "flat":
                    if self.topper == "up_steep" or self.topper == "up_gentle_start":
                        self.height += 1
                elif self.rows[-1].topper == "up_steep" or self.rows[-1].topper == "up_gentle_continue":
                    if self.topper == "up_steep" or self.topper == "up_gentle_start":
                        self.height += 1
                elif self.rows[-1].topper == "down_steep" or self.rows[-1].topper == "down_gentle_continue":
                    if self.topper != "up_steep" and self.topper != "up_gentle_start":

                        self.height -= 1
        self.surface = pygame.Surface((32, (self.height+23)*32))
        for i in range(self.height+23, -1, -1):
            if i != 0:
                type = "inside"
            else:
                type = self.topper
            tile = GroundSprite(ground_tiles_image, type)
            ground_sprites.add([tile])
            self.surface.blit(tile.image, (0, i*32))
        self.rect = self.surface.get_rect()
