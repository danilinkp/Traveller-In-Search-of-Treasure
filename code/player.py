import os
import sys
from math import sin

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


class Traveler(pygame.sprite.Sprite):
    def __init__(self, pos, screen, jump_particles, change_health):
        super().__init__()
        self.animations_dict = {'idle': [],
                                'run': []}

        # данные о герое
        self.loading_hero_sprites()
        self.frame_index = 0
        self.count = 0
        self.image = self.animations_dict['idle'][self.frame_index]

        self.mask = pygame.mask.from_surface(self.image)
        # для определения заданного начального положения координат верхнего левого угла
        self.rect = self.image.get_rect(topleft=pos)

        # частицы
        self.dust_run_particles = []
        self.loading_dust_sprites()
        self.dust_frame_index = 0
        self.dust_animation_count = 0
        self.screen = screen
        self.jump_particles = jump_particles

        # движения игркоа
        self.direction = [0, 0]  # позиция игрока
        self.speed = 6  # скорость передвижения
        self.gravity = 0.8  # скорость подъема
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.direction_to_the_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0
        self.player_hp = 300

    def loading_hero_sprites(self):  # импорт спрайтов для игрока
        animations_test = {'idle': [load_image('../graphics/character/idle/1.png'),
                                    load_image('../graphics/character/idle/2.png'),
                                    load_image('../graphics/character/idle/3.png'),
                                    load_image('../graphics/character/idle/4.png')],
                           'run': [load_image('../graphics/character/run/1.png'),
                                   load_image('../graphics/character/run/2.png'),
                                   load_image('../graphics/character/run/3.png'),
                                   load_image('../graphics/character/run/4.png'),
                                   load_image('../graphics/character/run/5.png')]

                           }

        for i in animations_test['idle']:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 2), int(i.get_height() * 2)))
            self.animations_dict['idle'].append(i)
        for i in animations_test['run']:
            i = pygame.transform.scale(i,
                                       (int(i.get_width() * 2), int(i.get_height() * 2)))
            self.animations_dict['run'].append(i)

    def loading_dust_sprites(self):  # импорт частиц

        self.dust_run_particles = [load_image('../graphics/character/dust_particles/run/run_1.png'),
                                   load_image('../graphics/character/dust_particles/run/run_2.png'),
                                   load_image('../graphics/character/dust_particles/run/run_3.png'),
                                   load_image('../graphics/character/dust_particles/run/run_4.png'),
                                   load_image('../graphics/character/dust_particles/run/run_5.png')]

    def animate(self):
        animation = self.animations_dict[self.status]
        # вид движения на данный момент
        if self.count > 8:  # Счетчик
            self.frame_index = (self.frame_index + 1) % len(animation)
            self.count = 0
        else:
            self.count += 1

        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[self.frame_index]
        if self.direction_to_the_right:
            self.image = image

        else:
            self.image = pygame.transform.flip(image, True, False)

        # set the rect
        self.set_the_rect()

    def run_dust_animation(self):  # прорисовка дастов
        if self.status == 'run' and self.on_ground:
            if self.dust_animation_count > 3:  # Счетчик
                self.dust_frame_index = (self.dust_frame_index + 1) % len(self.dust_run_particles)
                self.dust_animation_count = 0
            else:
                self.dust_animation_count += 1
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.direction_to_the_right:
                self.screen.blit(dust_particle,
                                 (self.rect.bottomleft[0], self.rect.bottomleft[1] - 10))
            else:

                self.screen.blit(pygame.transform.flip(dust_particle, True, False),
                                 (self.rect.bottomright[0] - 15, self.rect.bottomright[1] - 10))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:

            self.direction[0] = 1
            self.direction_to_the_right = True
        elif keys[pygame.K_LEFT]:
            self.direction[0] = -1
            self.direction_to_the_right = False
        else:
            self.direction[0] = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

            self.jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction[1] < 0 or self.direction[1] > 1:
            self.status = 'idle'
        else:
            if self.direction[0] != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction[1] += self.gravity
        self.rect.y += self.direction[1]

    def jump(self):
        self.direction[1] = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()

    def set_the_rect(self):
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)

        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_damage(self, hit):
        if not self.invincible:

            self.player_hp -= hit
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
        print(self.player_hp)

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def return_hp(self):
        return self.player_hp


