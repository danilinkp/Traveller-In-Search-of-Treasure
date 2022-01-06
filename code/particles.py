import os
import sys

import pygame


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


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type_of_movement):
        super().__init__()
        self.frame_index = 0
        self.count = 0
        if type_of_movement == 'jump':
            self.frames = [load_image('../graphics/character/dust_particles/jump/jump_1.png'),
                           load_image('../graphics/character/dust_particles/jump/jump_2.png'),
                           load_image('../graphics/character/dust_particles/jump/jump_3.png'),
                           load_image('../graphics/character/dust_particles/jump/jump_4.png'),
                           load_image('../graphics/character/dust_particles/jump/jump_5.png'),
                           load_image('../graphics/character/dust_particles/jump/jump_6.png')]
        if type_of_movement == 'land':
            self.frames = [load_image('../graphics/character/dust_particles/land/land_1.png'),
                           load_image('../graphics/character/dust_particles/land/land_2.png'),
                           load_image('../graphics/character/dust_particles/land/land_3.png'),
                           load_image('../graphics/character/dust_particles/land/land_4.png'),
                           load_image('../graphics/character/dust_particles/land/land_5.png')]

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):

        # Счетчик
        if self.count == 4:
            self.frame_index += 1
        else:
            self.count += 1

        if self.frame_index >= len(self.frames):

            self.kill()  # удаляет спрайт из всех групп

        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift