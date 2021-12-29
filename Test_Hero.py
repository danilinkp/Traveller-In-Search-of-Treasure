import os
import sys

import pygame

from Hero import Hero


class MonkHero(Hero):
    def __init__(self, screen, x, y, speed):
        super().__init__(screen, x, y, speed)
        self.screen = screen
        self.speed = speed
        self.x = x
        self.y = y
        self.jumpcount = 8
        self.scale = 4

        self.walkRight = [load_image('run_1.png', dictor='run'),
                          load_image('run_2.png', dictor='run'),
                          load_image('run_3.png', dictor='run'),
                          load_image('run_4.png', dictor='run'),
                          load_image('run_5.png', dictor='run'),
                          load_image('run_6.png', dictor='run'),
                          load_image('run_7.png', dictor='run'),
                          load_image('run_8.png', dictor='run')]
        self.walkRight = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.walkRight]

        self.walkLeft = [pygame.transform.flip(i, True, False) for i in self.walkRight]

        self.idle = [load_image('idle_1.png', dictor='idle'),
                     load_image('idle_2.png', dictor='idle'),
                     load_image('idle_3.png', dictor='idle'),
                     load_image('idle_4.png', dictor='idle'),
                     load_image('idle_5.png', dictor='idle'),
                     load_image('idle_6.png', dictor='idle')]
        self.idle = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.idle]


        self.j_up = [load_image('j_up_1.png', dictor='j_up'),
                     load_image('j_up_2.png', dictor='j_up'),
                     load_image('j_up_3.png', dictor='j_up')]
        self.j_up = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.j_up]

        self.j_down = [load_image('j_down_1.png', dictor='j_down'),
                       load_image('j_down_2.png', dictor='j_down'),
                       load_image('j_down_3.png', dictor='j_down')]

        self.j_down = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.j_down]

        self.f_atk_r = [load_image('1_atk_1.png', dictor='1_atk'),
                        load_image('1_atk_2.png', dictor='1_atk'),
                        load_image('1_atk_3.png', dictor='1_atk'),
                        load_image('1_atk_4.png', dictor='1_atk'),
                        load_image('1_atk_5.png', dictor='1_atk'),
                        load_image('1_atk_6.png', dictor='1_atk')]

        self.f_atk_r = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.f_atk_r]
        self.f_atk_l = [pygame.transform.flip(i, True, False) for i in self.f_atk_r]

        self.s_atk_r = [load_image('2_atk_1.png', dictor='2_atk'),
                        load_image('2_atk_2.png', dictor='2_atk'),
                        load_image('2_atk_3.png', dictor='2_atk'),
                        load_image('2_atk_4.png', dictor='2_atk'),
                        load_image('2_atk_5.png', dictor='2_atk'),
                        load_image('2_atk_6.png', dictor='2_atk'),
                        load_image('2_atk_7.png', dictor='2_atk'),
                        load_image('2_atk_8.png', dictor='2_atk'),
                        load_image('2_atk_9.png', dictor='2_atk'),
                        load_image('2_atk_10.png', dictor='2_atk'),
                        load_image('2_atk_11.png', dictor='2_atk'),
                        load_image('2_atk_12.png', dictor='2_atk')]
        self.s_atk_r = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.s_atk_r]
        self.s_atk_l = [pygame.transform.flip(i, True, False) for i in self.s_atk_r]

        self.t_atk_r = [load_image('3_atk_1.png', dictor='3_atk'),
                        load_image('3_atk_2.png', dictor='3_atk'),
                        load_image('3_atk_3.png', dictor='3_atk'),
                        load_image('3_atk_4.png', dictor='3_atk'),
                        load_image('3_atk_5.png', dictor='3_atk'),
                        load_image('3_atk_6.png', dictor='3_atk'),
                        load_image('3_atk_7.png', dictor='3_atk'),
                        load_image('3_atk_8.png', dictor='3_atk'),
                        load_image('3_atk_9.png', dictor='3_atk'),
                        load_image('3_atk_10.png', dictor='3_atk'),
                        load_image('3_atk_11.png', dictor='3_atk'),
                        load_image('3_atk_12.png', dictor='3_atk'),
                        load_image('3_atk_13.png', dictor='3_atk'),
                        load_image('3_atk_14.png', dictor='3_atk'),
                        load_image('3_atk_15.png', dictor='3_atk'),
                        load_image('3_atk_16.png', dictor='3_atk'),
                        load_image('3_atk_17.png', dictor='3_atk'),
                        load_image('3_atk_18.png', dictor='3_atk'),
                        load_image('3_atk_19.png', dictor='3_atk'),
                        load_image('3_atk_20.png', dictor='3_atk'),
                        load_image('3_atk_21.png', dictor='3_atk'),
                        load_image('3_atk_22.png', dictor='3_atk'),
                        load_image('3_atk_23.png', dictor='3_atk'),
                        load_image('3_atk_24.png', dictor='3_atk'),
                        ]
        self.t_atk_r = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.t_atk_r]
        self.t_atk_l = [pygame.transform.flip(i, True, False) for i in self.t_atk_r]

        self.ultimate_r = [load_image('sp_atk_1.png', dictor='sp_atk'),
                           load_image('sp_atk_2.png', dictor='sp_atk'),
                           load_image('sp_atk_3.png', dictor='sp_atk'),
                           load_image('sp_atk_4.png', dictor='sp_atk'),
                           load_image('sp_atk_5.png', dictor='sp_atk'),
                           load_image('sp_atk_6.png', dictor='sp_atk'),
                           load_image('sp_atk_7.png', dictor='sp_atk'),
                           load_image('sp_atk_8.png', dictor='sp_atk'),
                           load_image('sp_atk_9.png', dictor='sp_atk'),
                           load_image('sp_atk_10.png', dictor='sp_atk'),
                           load_image('sp_atk_11.png', dictor='sp_atk'),
                           load_image('sp_atk_12.png', dictor='sp_atk'),
                           load_image('sp_atk_13.png', dictor='sp_atk'),
                           load_image('sp_atk_14.png', dictor='sp_atk'),
                           load_image('sp_atk_15.png', dictor='sp_atk'),
                           load_image('sp_atk_16.png', dictor='sp_atk'),
                           load_image('sp_atk_17.png', dictor='sp_atk'),
                           load_image('sp_atk_18.png', dictor='sp_atk'),
                           load_image('sp_atk_19.png', dictor='sp_atk'),
                           load_image('sp_atk_20.png', dictor='sp_atk'),
                           load_image('sp_atk_21.png', dictor='sp_atk'),
                           load_image('sp_atk_22.png', dictor='sp_atk'),
                           load_image('sp_atk_23.png', dictor='sp_atk'),
                           load_image('sp_atk_24.png', dictor='sp_atk'),
                           load_image('sp_atk_25.png', dictor='sp_atk')
                           ]
        self.ultimate_r = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.ultimate_r]
        self.ultimate_l = [pygame.transform.flip(i, True, False) for i in self.ultimate_r]

        self.meditate_s = [
            load_image('meditate_1.png', dictor='meditate'),
            load_image('meditate_2.png', dictor='meditate'),
            load_image('meditate_3.png', dictor='meditate'),
            load_image('meditate_4.png', dictor='meditate'),
            load_image('meditate_5.png', dictor='meditate'),
            load_image('meditate_6.png', dictor='meditate'),
            load_image('meditate_7.png', dictor='meditate'),
            load_image('meditate_8.png', dictor='meditate'),
            load_image('meditate_9.png', dictor='meditate'),
            load_image('meditate_10.png', dictor='meditate'),
            load_image('meditate_11.png', dictor='meditate'),
            load_image('meditate_12.png', dictor='meditate'),
            load_image('meditate_13.png', dictor='meditate'),
            load_image('meditate_14.png', dictor='meditate'),
            load_image('meditate_15.png', dictor='meditate'),
            load_image('meditate_16.png', dictor='meditate')

        ]
        self.meditate_s = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.meditate_s]

        self.defend_r = [
            load_image('defend_1.png', dictor='defend'),
            load_image('defend_2.png', dictor='defend'),
            load_image('defend_3.png', dictor='defend'),
            load_image('defend_4.png', dictor='defend'),
            load_image('defend_5.png', dictor='defend'),
            load_image('defend_6.png', dictor='defend'),
            load_image('defend_7.png', dictor='defend'),
            load_image('defend_8.png', dictor='defend'),
            load_image('defend_9.png', dictor='defend'),
            load_image('defend_10.png', dictor='defend'),
            load_image('defend_11.png', dictor='defend'),
            load_image('defend_12.png', dictor='defend'),
            load_image('defend_13.png', dictor='defend')

        ]
        self.defend_r = [
            pygame.transform.scale(i, (int(i.get_width() * self.scale), int(i.get_height() * self.scale))) for
            i in self.defend_r]

        self.defend_l = [pygame.transform.flip(i, True, False) for i in self.defend_r]

    def run(self):
        if self.isJump:
            if self.animCount >= 18:
                self.animCount = 0
            if self.up:
                self.screen.blit(self.j_up[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.j_down[self.animCount // 6], (self.x, self.y))
        elif self.f_atk_flag:
            if self.animCount == 36:
                self.animCount = 0
                self.f_atk_flag = False

            if self.left:
                self.screen.blit(self.f_atk_l[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.f_atk_r[self.animCount // 6], (self.x, self.y))
            self.count_fun()

        elif self.s_atk_flag:
            if self.animCount >= 72:
                self.animCount = 0
                self.s_atk_flag = False

            if self.left:
                self.screen.blit(self.s_atk_l[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.s_atk_r[self.animCount // 6], (self.x, self.y))
            self.count_fun()

        elif self.t_atk_flag:
            if self.animCount >= 144:
                self.animCount = 0
                self.t_atk_flag = False

            if self.left:
                self.screen.blit(self.t_atk_l[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.t_atk_r[self.animCount // 6], (self.x, self.y))
            self.count_fun()

        elif self.ultimate_f:
            if self.animCount >= 150:
                self.animCount = 0
                self.ultimate_f = False

            if self.left:
                self.screen.blit(self.ultimate_l[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.ultimate_r[self.animCount // 6], (self.x, self.y))
            self.count_fun()


        elif self.defend_f:
            if self.animCount >= 78:
                self.animCount = 0
                self.defend_f = False

            if self.left:
                self.screen.blit(self.defend_l[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.defend_r[self.animCount // 6], (self.x, self.y))
            self.count_fun()



        else:
            if self.right or self.left:
                if self.animCount == 48:
                    self.animCount = 0
            else:
                if self.meditate_f:
                    if self.animCount >= 72:
                        self.animCount = 32
                    self.start = False

                else:

                    if self.animCount == 36:
                        self.animCount = 0

            if self.right:

                self.screen.blit(self.walkRight[self.animCount // 6], (self.x, self.y))

            elif self.left:
                self.screen.blit(self.walkLeft[self.animCount // 6], (self.x, self.y))

            else:

                if self.meditate_f:
                    self.screen.blit(self.meditate_s[self.animCount // 6], (self.x, self.y))
                else:

                    self.screen.blit(self.idle[self.animCount // 6], (self.x, self.y))

    def count_fun(self):
        self.animCount += 1

    def idle_pos(self):
        if not self.start:
            self.start = True
            self.animCount = 0
            self.left = False
            self.right = False
            self.count_sec = 0
        else:
            self.animCount += 1
            self.count_sec += 1
            if self.count_sec > 200:
                self.count_sec = 0
                self.animCount = 0
                self.meditate_f = True
                self.start = False

    def get_pos(self):
        return self.x, self.y

    def jump(self):
        self.meditate_f = False
        if self.jumpcount >= -8:
            if self.jumpcount < 0:
                self.y += (self.jumpcount ** 2) // 1.5
                if self.up:
                    self.up = False
                    self.animCount = 0

            else:
                if not self.up:
                    self.up = True
                    self.animCount = 0

                self.y -= (self.jumpcount ** 2) // 1.5
            self.jumpcount -= 1
            self.count_fun()
        else:
            self.jumpcount = 8
            self.isJump = False

    def first_attack(self):
        if not self.f_atk_flag:
            self.f_atk_flag = True
            self.animCount = 0

    def second_attack(self):
        if not self.s_atk_flag:
            self.s_atk_flag = True
            self.animCount = 0

    def third_attack(self):
        if not self.t_atk_flag:
            self.t_atk_flag = True
            self.animCount = 0

    def ultimate_attack(self):
        if not self.ultimate_f:
            self.ultimate_f = True
            self.animCount = 0


def load_image(name, dictor='images', colorkey=None):
    fullname = os.path.join(dictor, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл` с изображением '{fullname}' не найден")
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
