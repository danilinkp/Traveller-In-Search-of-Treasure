import os
import sys

import pygame
from tiles import AnimatedTile


def load_image(name, dictor='', colorkey=None):
    """ Функция для загрузки изображения """
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
    """ Класс, в котором реализован весь функционал мобов """

    def __init__(self, pos, size, hit_count, id):
        type_id = id
        if type_id == 1:
            self.animations = [load_image('../graphics/enemies/Walk/Walk_1.png'),
                               load_image('../graphics/enemies/Walk/Walk_2.png'),
                               load_image('../graphics/enemies/Walk/Walk_3.png'),
                               load_image('../graphics/enemies/Walk/Walk_4.png')]

        if type_id == 2:
            self.animations = [load_image('../graphics/enemies/Walk_3/Walk_1.png'),
                               load_image('../graphics/enemies/Walk_3/Walk_2.png'),
                               load_image('../graphics/enemies/Walk_3/Walk_3.png'),
                               load_image('../graphics/enemies/Walk_3/Walk_4.png')]
        if type_id == 3:
            self.animations = [load_image('../graphics/enemies/Walk_4/Walk_1.png'),
                               load_image('../graphics/enemies/Walk_4/Walk_2.png'),
                               load_image('../graphics/enemies/Walk_4/Walk_3.png'),
                               load_image('../graphics/enemies/Walk_4/Walk_4.png')]
        self.loading_hero_sprites()
        super().__init__(pos, size, self.animations)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 3
        self.check_flag = 1
        self.hit_count = hit_count

    def loading_hero_sprites(self):
        """ Импорт спрайтов для игрока """
        self.animations = [pygame.transform.scale(i, (int(i.get_width() * 2), int(i.get_height() * 2))) for i in
                           self.animations]

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def return_size_image(self):
        return self.image.get_width()

    def reverse(self):
        """Меняет направление моба"""
        self.speed *= -1

    def return_speed(self):
        """Возвращает скорость передвижения моба"""
        return self.speed

    def return_hit(self):
        """Возвращает урон который наносит моб"""
        return self.hit_count

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()


class Coin(AnimatedTile):
    """ Класс, в котором реализован функционал монет """

    def __init__(self, pos, size, type_id):
        self.animations = []
        self.type_id = type_id

        self.loading_hero_sprites()

        super().__init__(pos, size, self.animations)
        self.rect.y += size - self.image.get_size()[1]

    def loading_hero_sprites(self):
        """Импорт спрайтов для монет"""
        if self.type_id == 1:
            animations_test = [load_image('../graphics/Coins/MonedaD_1.png'),
                               load_image('../graphics/Coins/MonedaD_2.png'),
                               load_image('../graphics/Coins/MonedaD_3.png'),
                               load_image('../graphics/Coins/MonedaD_4.png'),
                               load_image('../graphics/Coins/MonedaD_5.png')

                               ]
        elif self.type_id == 2:
            animations_test = [load_image('../graphics/Coins/frame0000.png'),
                               load_image('../graphics/Coins/frame0001.png'),
                               load_image('../graphics/Coins/frame0002.png'),
                               load_image('../graphics/Coins/frame0003.png'),
                               load_image('../graphics/Coins/frame0004.png'),
                               load_image('../graphics/Coins/frame0005.png'),
                               load_image('../graphics/Coins/frame0006.png')
                               ]

        elif self.type_id == 3:
            animations_test = [load_image('../graphics/Health/health_1.png'),
                               load_image('../graphics/Health/health_2.png'),
                               load_image('../graphics/Health/health_3.png'),
                               load_image('../graphics/Health/health_4.png'),
                               load_image('../graphics/Health/health_5.png'),
                               load_image('../graphics/Health/health_6.png')
                               ]

        else:
            animations_test = [load_image('../graphics/Coins/MonedaP_1.png'),
                               load_image('../graphics/Coins/MonedaP_2.png'),
                               load_image('../graphics/Coins/MonedaP_3.png'),
                               load_image('../graphics/Coins/MonedaP_4.png'),
                               load_image('../graphics/Coins/MonedaP_5.png')

                               ]

        for i in animations_test:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 1.6), int(i.get_height() * 1.6)))
            self.animations.append(i)

    def return_size_image(self):
        return self.image.get_width()

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()

    def collisions(self):
        """Возвращает ценность монет при столкновении с игроком"""
        if self.type_id == 1:
            return 's', 10
        elif self.type_id == 2:
            return 's_d', 30
        elif self.type_id == 3:
            return 'h', 30
        return 's', 5


class Hp:
    """Класс, в котором реализованы жизни игрока"""

    def __init__(self):
        self.animations = []
        self.animations_dict = {'full': '', 'half': '', 'few': '', 'Not': ''}

        self.loading_hero_sprites()

    def loading_hero_sprites(self):
        """Импорт спрайтов для жизней """

        animations_test = [load_image('../graphics/Health/health_player_1.png'),
                           load_image('../graphics/Health/health_player_2.png'),
                           load_image('../graphics/Health/health_player_3.png'),
                           load_image('../graphics/Health/health_player_4.png'),

                           ]

        for i in animations_test:
            i = pygame.transform.scale(i,
                                       (int(i.get_width()) // 2, int(i.get_height()) // 2))
            self.animations.append(i)

        self.animations_dict['full'] = self.animations[0]
        self.animations_dict['half'] = self.animations[1]
        self.animations_dict['few'] = self.animations[2]
        self.animations_dict['not'] = self.animations[3]

    def return_image(self, count_hp):
        """Возвращает есть ли сердечка, или нет"""
        if count_hp > 260:
            return [self.animations_dict['full'], self.animations_dict['full'], self.animations_dict['full']]
        if 230 < count_hp <= 260:
            return [self.animations_dict['full'], self.animations_dict['full'], self.animations_dict['half']]
        if 200 < count_hp <= 230:
            return [self.animations_dict['full'], self.animations_dict['full'], self.animations_dict['few']]
        if 160 < count_hp <= 200:
            return [self.animations_dict['full'], self.animations_dict['full'], self.animations_dict['not']]
        if 130 < count_hp <= 160:
            return [self.animations_dict['full'], self.animations_dict['half'], self.animations_dict['not']]
        if 100 < count_hp <= 130:
            return [self.animations_dict['full'], self.animations_dict['few'], self.animations_dict['not']]
        if 60 < count_hp <= 100:
            return [self.animations_dict['full'], self.animations_dict['not'], self.animations_dict['not']]
        if 30 < count_hp <= 60:
            return [self.animations_dict['half'], self.animations_dict['not'], self.animations_dict['not']]
        if 0 < count_hp <= 30:
            return [self.animations_dict['few'], self.animations_dict['not'], self.animations_dict['not']]

        return [self.animations_dict['not'], self.animations_dict['not'], self.animations_dict['not']]


class Diamond(AnimatedTile):
    """Класс, в котором реализованы алмазы"""

    def __init__(self, pos, size):
        self.animations = []

        self.loading_hero_sprites()

        super().__init__(pos, size, self.animations)
        self.rect.y += size - self.image.get_size()[1]

    def loading_hero_sprites(self):
        """Импорт спрайтов для алмазов"""

        animations_test = [load_image('../graphics/Coins/frame0000.png'),
                           load_image('../graphics/Coins/frame0001.png'),
                           load_image('../graphics/Coins/frame0002.png'),
                           load_image('../graphics/Coins/frame0003.png'),
                           load_image('../graphics/Coins/frame0004.png'),
                           load_image('../graphics/Coins/frame0005.png'),
                           load_image('../graphics/Coins/frame0006.png')
                           ]

        for i in animations_test:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 1.6), int(i.get_height() * 1.6)))
            self.animations.append(i)

    def update(self):
        self.animate()


class Water(AnimatedTile):
    """Класс, в котором реализован функционал воды"""

    def __init__(self, pos, size):
        self.animations = []

        self.loading_hero_sprites()

        super().__init__(pos, size, self.animations)
        self.rect.y += size - self.image.get_size()[1]

    def loading_hero_sprites(self):
        """Импорт спрайтов для водички"""

        animations_test = [load_image('../graphics/water/1.png'),
                           load_image('../graphics/water/2.png'),
                           load_image('../graphics/water/3.png'),
                           load_image('../graphics/water/4.png')]

        for i in animations_test:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 1.6), int(i.get_height() * 1.6)))
            self.animations.append(i)

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
