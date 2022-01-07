import os
import sys

import pygame
from tiles import AnimatedTile


def load_image(name, dictor='', colorkey=None):
    fullname = os.path.join(dictor, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mob(AnimatedTile):
    def __init__(self, pos, size):
        self.animations = []
        self.loading_hero_sprites()
        super().__init__(pos, size, self.animations)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 5

    def loading_hero_sprites(self):  # импорт спрайтов для игрока
        animations_test = [load_image('../graphics/enemies/Walk/Walk_1.png'),
                           load_image('../graphics/enemies/Walk/Walk_2.png'),
                           load_image('../graphics/enemies/Walk/Walk_3.png'),
                           load_image('../graphics/enemies/Walk/Walk_4.png')]
        for i in animations_test:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 2), int(i.get_height() * 2)))
            self.animations.append(i)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()
