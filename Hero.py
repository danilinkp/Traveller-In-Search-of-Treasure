import pygame


class Hero(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, speed):
        super().__init__()
        self.screen = screen  # перменная, отвечающая за дисплей
        self.left = False
        self.right = False  # переменные, отвечающие за направление игрока
        self.start = True  # True, если герой в состоянии покоя
        self.animCount = 0  # Счетчик анимаций
        self.x = x  # начальное расположение героя
        self.y = y
        self.speed = speed
        self.isJump = False  # герой в состоянии прыжка или нет
        self.up = True  # если герой только что прыгнул и летит вверх - 1, падает - 0

        self.jumpCount = 8  # перменная для времени прыжка
        self.f_atk_flag = False  # Переменная, отвечающая за проверку нажатия атаки (1-3)
        self.s_atk_flag = False
        self.t_atk_flag = False
        self.ultimate_f = False  # Переменная, отвечающая за проверку нажатия ульты
        self.count_sec = 0  # Счётчик времени, дял медитации Monk
        self.meditate_f = False  # Если герой в состоянии медитации - 1, иначе - 0
        self.defend_f = False  # Активация защиты

        self.walkRight = []  # Переменная, хранящая спрайты движения вправо/влево
        self.walkLeft = [pygame.transform.flip(i, True, False) for i in self.walkRight]

        self.idle = []  # Переменная, хранящая спрайт покоя

        self.j_up = []  # Переменная, хранящая спрайты движения вверх

        self.j_down = []  # Переменная, хранящая спрайты движения вниз

        # Переменная, хранящая спрайты атак вправо/влево
        self.f_atk_r = []
        self.f_atk_l = [pygame.transform.flip(i, True, False) for i in self.f_atk_r]

        self.s_atk_r = []
        self.s_atk_l = [pygame.transform.flip(i, True, False) for i in self.s_atk_r]

        self.t_atk_r = []
        self.t_atk_l = [pygame.transform.flip(i, True, False) for i in self.t_atk_r]

        # Переменная, хранящая спрайты ульты вправо/влево
        self.ultimate_r = []
        self.ultimate_l = [pygame.transform.flip(i, True, False) for i in self.ultimate_r]
        # Переменная, хранящая спрайты медитации
        self.meditate_s = []
        # Переменная, хранящая спрайты защиты вправо/влево
        self.defend_r = []
        self.defend_l = [pygame.transform.flip(i, True, False) for i in self.defend_r]

    def run(self):  # Отрисовка игрока
        if self.isJump:  # Проверка, что игрок не в полете
            if self.animCount >= 18:
                self.animCount = 0
            if self.up:
                self.screen.blit(self.j_up[self.animCount // 6], (self.x, self.y))
            else:
                self.screen.blit(self.j_down[self.animCount // 6], (self.x, self.y))
        elif self.f_atk_flag:   # Если игрок не в полете
            if self.animCount == 36:
                self.animCount = 0
                self.f_atk_flag = False
            self.left_or_right(self.f_atk_l, self.f_atk_r)  # Отрисовка по направлению
            self.count_fun()

        elif self.s_atk_flag:  # Аналогично self.f_atk_flag
            if self.animCount >= 72:
                self.animCount = 0
                self.s_atk_flag = False
            self.left_or_right(self.s_atk_l, self.s_atk_r)
            self.count_fun()

        elif self.t_atk_flag: # Аналогично self.f_atk_flag
            if self.animCount >= 144:
                self.animCount = 0
                self.t_atk_flag = False
            self.left_or_right(self.t_atk_l, self.t_atk_r)
            self.count_fun()

        elif self.ultimate_f:  # Аналогично self.f_atk_flag
            if self.animCount >= 150:
                self.animCount = 0
                self.ultimate_f = False
            self.left_or_right(self.ultimate_l, self.ultimate_r)
            self.count_fun()

        elif self.defend_f:  # Аналогично self.f_atk_flag
            if self.animCount >= 78:
                self.animCount = 0
                self.defend_f = False
            self.left_or_right(self.defend_l, self.defend_r)
            self.count_fun()
        else:   # Если герой не в полете и не использует способности, то ...
            if self.right or self.left:
                if self.animCount == 48:
                    self.animCount = 0  # Проверка на движение
            else:
                if self.meditate_f:    # Если герой в режиме медитации
                    if self.animCount >= 72:
                        self.animCount = 32
                    self.start = False
                else:   # Если герой в режиме покоя
                    if self.animCount == 36:
                        self.animCount = 0

            self.left_or_right(self.walkRight, self.walkLeft)   # Проверка направленяи

            if not (all([self.left, self.right])):
                if self.meditate_f:
                    self.screen.blit(self.meditate_s[self.animCount // 6], (self.x, self.y))
                else:
                    self.screen.blit(self.idle[self.animCount // 6], (self.x, self.y))

    def left_or_right(self, right, left):  # замена повторяющихся блоков функцией
        if self.right:
            self.screen.blit(right[self.animCount // 6], (self.x, self.y))
        elif self.left:
            self.screen.blit(left[self.animCount // 6], (self.x, self.y))

    def horizontal_movement(self, flag, flag2):  # движение игрока по горизонтали
        self.left = flag
        self.right = flag2

        if self.left:
            self.x -= self.speed
            if all([self.meditate_f, self.start, self.right]):
                self.animCount = 0
            if self.right:
                self.right = False
                self.left = True
            elif not (all([self.right, self.left])):
                self.left = True
        else:
            self.x += self.speed
            if all([self.meditate_f, self.start, self.left]):
                self.animCount = 0
            if self.left:
                self.left = False
                self.right = True
            elif not (all([self.right, self.left])):
                self.right = True

        self.start = False
        self.meditate_f = False

    def count_fun(self):  # счетчик анимаций
        self.animCount += 1

    def idle_pos(self):
        pass

    def jump(self):
        pass

    def get_pos(self):
        return self.x, self.y

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

    def meditate(self):
        self.meditate_f = True

    def get_flags(self):
        return f'left - {self.left}\n' \
               f'right - {self.right} \n' \
               f'start - {self.start} \n' \
               f'medit - {self.meditate_f} \n ' \
               f'count - {self.animCount} \n' \
               f'--------------------------- \n'

    def defend_el(self):
        if not self.defend_f:
            self.defend_f = True
            self.animCount = 0
