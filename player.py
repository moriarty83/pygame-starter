import pygame
from pygame.locals import *
import math
import os

pygame.init()

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


class Player(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__()
        self.screen = args[0]
        self.current_rotation = 0
        self.position = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.sprite_index = math.floor(self.current_rotation % 360 / 15)
        self.active_sprite = player_sprites[self.sprite_index]
        self.rect = pygame.Rect(self.screen.get_width() / 2 - 32,
                                self.screen.get_height() / 2 - 32, 64, 64)

    def calculate_thrust(self):
        radians = self.current_rotation * math.pi/180
        return pygame.Vector2(math.sin(radians),
                              -math.cos(radians))

    def rotate(self, degrees):
        if self.current_rotation + degrees == 360 or self.current_rotation + degrees == -360:
            self.current_rotation = 0
        else:
            self.current_rotation += degrees
        self.update_sprite()

    def update_sprite(self):
        self.sprite_index = math.floor(self.current_rotation % 360 / 15)
        self.active_sprite = player_sprites[self.sprite_index]
        self.rect = self.active_sprite.get_rect()
