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
    """Класс, в котором реализованы всякого рода частицы"""

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
            self.frames = [pygame.transform.scale(i,
                                                  (int(i.get_width() // 1.4), int(i.get_height() // 1.4))) for i in
                           self.frames]
        if type_of_movement == 'hit':
            self.frames = [load_image('../graphics/character/dust_particles/hit/B001.png'),
                           load_image('../graphics/character/dust_particles/hit/B002.png'),
                           load_image('../graphics/character/dust_particles/hit/B003.png'),
                           load_image('../graphics/character/dust_particles/hit/B004.png'),
                           load_image('../graphics/character/dust_particles/hit/B005.png'),
                           load_image('../graphics/character/dust_particles/hit/B006.png'),
                           load_image('../graphics/character/dust_particles/hit/B007.png'),
                           load_image('../graphics/character/dust_particles/hit/B008.png'),
                           load_image('../graphics/character/dust_particles/hit/B009.png'),
                           load_image('../graphics/character/dust_particles/hit/B010.png')

                           ]

            self.frames = [pygame.transform.scale(i,
                                                  (int(i.get_width()), int(i.get_height()))) for i in
                           self.frames]
        if type_of_movement == 'land':
            self.frames = [load_image('../graphics/character/dust_particles/land/land_1.png'),
                           load_image('../graphics/character/dust_particles/land/land_2.png'),
                           load_image('../graphics/character/dust_particles/land/land_3.png'),
                           load_image('../graphics/character/dust_particles/land/land_4.png'),
                           load_image('../graphics/character/dust_particles/land/land_5.png')]
            self.frames = [pygame.transform.scale(i,
                                                  (int(i.get_width() // 1.4), int(i.get_height() // 1.4))) for i in
                           self.frames]

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        # Счетчик
        if self.count == 1:
            self.frame_index += 1.3
        else:
            self.count += 1
        if self.frame_index >= len(self.frames):
            self.kill()  # удаляет спрайт из всех групп
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


class HitEffect(ParticleEffect):
    """Класс, который отрисовывает эффект получения урона"""

    def __init__(self, pos):
        super().__init__(pos, 'hit')

    def animate(self):
        # Счетчик
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.kill()  # удаляет спрайт из всех групп
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

    def return_frame(self):
        return self.frame_index
