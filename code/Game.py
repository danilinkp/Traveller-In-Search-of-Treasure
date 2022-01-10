import os
import pygame
import sys

import pytmx

from Mobs import Mob

from tiles import Tile
from settings import screen_width
from player import Traveler
from particles import ParticleEffect

pygame.init()
pygame.display.set_caption('pygame-project')

SIZE = WIDTH, HEIGHT = 1280, 764
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((1280, 764), pygame.FULLSCREEN)
left = False
right = False
volume = 60
change_difficult = 0
select_lang = 0
animCount = 8
all_sprites = pygame.sprite.Group()
MENU_BTN_SOUND = pygame.mixer.Sound('sounds/menu_btn.wav')
pos_of_player = [256, 448]


def load_image(name, dictor='images', colorkey=None):
    fullname = os.path.join(dictor, name)
    # если файл не существует   , то выходим
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

# test
DIFFICULTY = ['easy', 'normal', 'hard', 'cheat']
LANGUAGES = ['en', 'ru']
MENU_BTN_SOUND = pygame.mixer.Sound('sounds/menu_btn.wav')


def rotate():
    pass


class Button:
    """ Класс кнопок для создания непосредственно самих конпок """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, message, button_image, action=None, font_size=50):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)),
                        (x, y - 5))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
                x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2) - 5))
            if clicked[0]:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y))
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
                x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))


class SystemButton:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, image, message, font_size=50):
        screen.blit(pygame.transform.scale(load_image(image), (self.width, self.height)), (x, y))
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, 'white')
        screen.blit(text,
                    (
                        x + ((self.width - text.get_width()) // 2),
                        y + ((self.height - text.get_height()) // 2)))


def show_menu():
    """ Отрисовка самого меню """
    menu_background = load_image('background.jpg')
    show_menu_f = True
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    scores_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    while show_menu_f:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(WIDTH - 500, HEIGHT - 500, 'Start game', 'btn_menu.png', game_cycle)
        settings_btn.draw(WIDTH - 500, HEIGHT - 410, 'Settings', 'btn_menu.png', settings)
        scores_btn.draw(WIDTH - 500, HEIGHT - 320, 'Scores', 'btn_menu.png', scores)
        exit_btn.draw(WIDTH - 500, HEIGHT - 140, 'Exit', 'btn_menu.png', terminate)
        help_btn.draw(WIDTH - 500, HEIGHT - 230, 'Help', 'btn_menu.png', help_menu)
        pygame.display.update()
        clock.tick(60)


def start_menu():
    running = True

    show_menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
    pygame.quit()


def game_cycle():
    name = FunctionCallDrawing('images/background_2.jpg', [(460, 100), (460, 100)],
                               [[(80, 80), 'Story mode', 'btn.png', story_mode],
                                [(730, 80), 'PVP mode', 'btn.png', pvp_mode]])
    name.run()


def story_mode():
    name = FunctionCallDrawing('images/background_5.jpg', [(540, 150), (460, 100), (460, 100)],
                               [[(360, 80), 'NEW GAME', 'btn.png', story_mode_new_game],
                                [(400, 260), 'STORE', 'btn.png', store_mode],
                                [(400, 400), 'HEROES', 'btn.png', pvp_mode]
                                ])
    name.run()


def story_mode_new_game():
    name = FunctionCallDrawing('images/for_nickname.jpg', [(380, 70)],
                               [[(880, 600), 'ok', 'btn.png', story_mode_new_game_select_heroes]])
    name.run()


def story_mode_new_game_select_heroes():
    name = FunctionCallDrawing('images/select_heroes.jpg', [(380, 70)],
                               [[(450, 620), 'select', 'btn.png', levels_show_menu]])
    name.run()


def levels_show_menu():
    name = FunctionCallDrawing('images/start_level.jpg', [(500, 100)],
                               [[(700, 560), 'start', 'btn.png', game]])
    name.run()


def pvp_mode():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               # потом нужно будет исправить
                               [[(145, 500), 'select', 'btn.png', pvp_mode_2],
                                [(515, 500), 'select', 'btn.png', pvp_mode_2],
                                [(885, 500), 'select', 'btn.png', pvp_mode_2]
                                ])
    name.run()


def pvp_mode_2():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               # потом нужно будет исправить
                               [[(145, 500), 'start', 'btn.png', play_pvp_mode],
                                [(515, 500), 'start', 'btn.png', play_pvp_mode],
                                [(885, 500), 'start', 'btn.png', play_pvp_mode]
                                ])
    name.run()


clock = pygame.time.Clock()


def play_pvp_mode():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'select', 'btn.png', buy_mage],
                                [(515, 500), 'select', 'btn.png', buy_warrior],
                                [(885, 500), 'select', 'btn.png', buy_archer]
                                ])
    name.run()


def store_mode():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'select', 'btn.png', buy_mage],
                                [(515, 500), 'select', 'btn.png', buy_warrior],
                                [(885, 500), 'select', 'btn.png', buy_archer]
                                ])
    name.run()


def buy_mage():
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


def buy_warrior():
    """ Отрисовка самого меню """
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                            ])
    name.run()  # потом нужно будет исправить


def buy_archer():
    """ Отрисовка самого меню """
    name = FunctionCallDrawing('images/buy_skin.jpg', [(250, 70), (250, 70), (250, 70)],
                               [[(145, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(515, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes],
                                [(885, 500), 'buy', 'btn.png', story_mode_new_game_select_heroes]
                                ])
    name.run()  # потом нужно будет исправить


class FunctionCallDrawing:
    def __init__(self, backgroundimage, w_h, name_coords_fun):
        self.back_im = backgroundimage
        self.w_h = w_h
        self.name_coords_fun = name_coords_fun
        self.buttons = []
        self.running = True

    def run(self):
        menu_background = pygame.image.load(self.back_im)

        for i in self.w_h:
            self.buttons.append(Button(i[0], i[1]))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            screen.blit(menu_background, (0, 0))
            for i in range(len(self.buttons)):
                self.buttons[i].draw(self.name_coords_fun[i][0][0],
                                     self.name_coords_fun[i][0][1],
                                     self.name_coords_fun[i][1],
                                     self.name_coords_fun[i][2],
                                     self.name_coords_fun[i][3])
            pygame.display.update()


class Level:
    def __init__(self, path, surface):  # Принимает карту(список) и  скрин

        # level setup
        self.travaler = None  # по умолчанию None, пока не будет вызван класс

        self.tiles = pygame.sprite.Group()
        self.boxes_and_cubes = pygame.sprite.Group()
        self.checkpoint = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()  # группа с героем
        self.enemies = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.constraints = pygame.sprite.Group()
        self.background_im = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.screen = surface  # скрин
        # добавление карты
        self.world_shift = 10  # скорость передвижения камеры
        self.current_x = 160



        self.dust_sprite = pygame.sprite.GroupSingle()  # группа с частицами
        self.player_on_ground = False
        self.path = path
        self.map = pytmx.load_pygame("maps/level.tmx")
        self.num_of_layers = len(self.map.layers)
        self.height_map = self.map.height
        self.width_map = self.map.width
        self.tile_size = self.map.tilewidth * 2
        self.count_camera = 90
        self.change = 20
        self.running_now = True
        self.render()

        self.run()
        self.running_now = False




    def create_jump_particles(self, pos):
        if self.travaler.direction_to_the_right:
            jump_particle_sprite = ParticleEffect((pos[0] - 10, pos[1] - 5), 'jump')
            self.dust_sprite.add(jump_particle_sprite)
        else:
            jump_particle_sprite = ParticleEffect((pos[0] + 10, pos[1] - 5), 'jump')
            self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.travaler.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.travaler.on_ground \
                and not self.dust_sprite.sprites():

            if self.travaler.direction_to_the_right:

                fall_dust_particle = ParticleEffect((self.travaler.rect.midbottom[0] - 10,
                                                     self.travaler.rect.midbottom[1] - 15), 'land')

            else:

                fall_dust_particle = ParticleEffect(
                    (self.travaler.rect.midbottom[0] + 10, self.travaler.rect.midbottom[1] - 15), 'land')
            self.dust_sprite.add(fall_dust_particle)

    def render(self):

        self.travaler = Traveler((7 * 32, 14 * 32), self.screen, self.create_jump_particles, self.change)
        self.player_group.add(self.travaler)

        spisok = [(58 * 32, 16 * 32), (48 * 32, 6 * 32)]
        spisok_constrains = [(55 * 32, 6 * 32), (46 * 32, 6 * 32), (54 * 32, 16 * 32), (61 * 32, 16 * 32)]
        for pos in spisok:
            enemy = Mob(pos, self.tile_size)
            self.enemies.add(enemy)

        for y in range(self.height_map):
            for x in range(self.width_map):
                for i in range(self.num_of_layers):
                    image = self.map.get_tile_image(x, y, i)
                    #          print(image)
                    x_1 = x * self.tile_size
                    y_1 = y * self.tile_size
                    #   print(x_1, y_1)

                    if image:
                        #  < TiledTileLayer[2]: "background_mountains" > 1
                        #  < TiledTileLayer[4]: "decoration" >,2
                    #  < TiledTileLayer[8]: "checkpoint" >,3
                        #  < TiledTileLayer[3]: "background_trees" >,4
                        #  < TiledTileLayer[5]: "water" >,5
                        #  < TiledTileLayer[7]: "grass" >,6
                        #  < TiledTileLayer[6]: "boxes" >,7
                        #  < TiledTileLayer[1]: "landscape" >8
                        #  < TiledTileLayer[9]: "cubes" >]9
                        image = pygame.transform.scale(image,
                                                       (
                                                           image.get_width() * 2,
                                                           image.get_height() * 2))

                        if (x_1, y_1) in spisok_constrains:
                            tile = Tile((x_1, y_1), self.tile_size, image)
                            self.constraints.add(tile)
                        else:

                            if i == 8 or i == 7 or i == 6:
                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.tiles.add(tile)
                            if i == 7 or i == 6:

                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.boxes_and_cubes.add(tile)
                            elif i == 0:
                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.background_im.add(tile)

                            elif i == 4:
                                tile = Tile((x_1, y_1), self.tile_size, image)

                                self.water.add(tile)

                            elif i == 2:
                                tile = Tile((x_1, y_1), self.tile_size, image)

                                self.checkpoint.add(tile)

                            else:

                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.decorations.add(tile)

    def scroll_x(self):
        player_x = self.travaler.rect.centerx
        direction_x = self.travaler.direction





        if self.running_now:
            self.world_shift = -385 * 2
            self.travaler.speed = 0

        elif player_x < screen_width / 4 and direction_x[0] < 0:

                self.world_shift = 6
                self.travaler.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x[0] > 0:

                self.world_shift = -6
                self.travaler.speed = 0
        else:
            self.running_now = False
            self.world_shift = 0
            self.travaler.speed = 6

    def horizontal_movement_collision(self):
        self.travaler.rect.x += self.travaler.direction[0] * self.travaler.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.travaler.rect):

                if self.travaler.direction[0] < 0:

                    self.travaler.rect.left = sprite.rect.right
                    self.travaler.on_left = True
                    self.current_x = self.travaler.rect.left

                elif self.travaler.direction[0] > 0:
                    self.travaler.rect.right = sprite.rect.left
                    self.travaler.on_right = True
                    self.current_x = self.travaler.rect.right

        if self.travaler.on_left and (self.travaler.rect.left < self.current_x
                                      or self.travaler.direction[0] >= 0):
            self.travaler.on_left = False

        if self.travaler.on_right and (self.travaler.rect.right > self.current_x
                                       or self.travaler.direction[0] <= 0):
            self.travaler.on_right = False

    def vertical_movement_collision(self):
        self.travaler.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(self.travaler.rect):

                if self.travaler.direction[1] > 0:
                    self.travaler.rect.bottom = sprite.rect.top
                    self.travaler.direction[1] = 0
                    self.travaler.on_ground = True
                elif self.travaler.direction[1] < 0:
                    self.travaler.rect.top = sprite.rect.bottom
                    self.travaler.direction[1] = 0
                self.travaler.on_ceiling = True

        if self.travaler.on_ground and self.travaler.direction[1] < 0 or self.travaler.direction[1] > 1:
            self.travaler.on_ground = False
        if self.travaler.on_ceiling and self.travaler.direction[1] > 0.1:
            self.travaler.on_ceiling = False

    def enemy_collision_reverse(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints, False):
                enemy.reverse()

    def water_collision(self):

        if pygame.sprite.spritecollide(self.travaler, self.water, False):
                print('DEATH')

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player_group.sprite, self.enemies, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player_group.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player_group.sprite.direction[1] >= 0:
                    self.player_group.sprite.direction[1] = -15
                    #  explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')

                    enemy.kill()
                else:
                    self.travaler.get_damage()

    def run(self):
        self.background_im.update(self.world_shift)

        self.background_im.draw(self.screen)
        self.decorations.update(self.world_shift)

        self.decorations.draw(self.screen)

        self.tiles.update(self.world_shift)

        self.tiles.draw(self.screen)

        self.enemies.update(self.world_shift)

        self.constraints.update(self.world_shift)

        self.constraints.draw(self.screen)
        self.enemy_collision_reverse()
        self.enemies.draw(self.screen)

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.screen)

        self.checkpoint.update(self.world_shift)
        self.checkpoint.draw(self.screen)

        self.player_group.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.water.update(self.world_shift)
        self.water.draw(self.screen)
        self.scroll_x()
        self.player_group.draw(self.screen)

        self.check_enemy_collisions()
        self.water_collision()


def settings():
    settings_background = load_image('background_5.jpg')
    volume_btn = SystemButton(400, 135)
    difficulty_btn = SystemButton(400, 135)
    language_btn = SystemButton(400, 135)
    change_lang_btn = Button(40, 40)
    quiet_btn = Button(40, 15)
    loud_btn = Button(40, 40)
    easier_btn = Button(40, 15)
    harder_btn = Button(40, 40)
    about_btn = Button(400, 135)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
        screen.blit(settings_background, (0, 0))
        volume_btn.draw(460, 50, 'settings_btns.png', f'Volume {volume}%')
        difficulty_btn.draw(460, 200, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}", 40)
        language_btn.draw(460, 350, 'settings_btns.png', f'Language: {LANGUAGES[select_lang]}')
        about_btn.draw(460, 500, 'About', 'settings_btns.png', about_widget)

        quiet_btn.draw(500, 110, '', 'minus_btn.png', quiet_volume)
        loud_btn.draw(780, 95, '', 'plus_btn.png', loud_volume)
        easier_btn.draw(500, 260, '', 'minus_btn.png', reduce_difficult)
        harder_btn.draw(780, 245, '', 'plus_btn.png', increase_difficult)
        change_lang_btn.draw(780, 395, '', 'plus_btn.png', change_language)

        pygame.display.update()


def scores():
    menu_background = load_image('background_2.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #     logging.warning('game exit by keys')
                    show = False

        screen.blit(menu_background, (0, 0))
        pygame.display.update()


def help_menu():
    about = load_image('background_5.jpg')
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False

        screen.blit(about, (0, 0))
        pygame.display.update()


def loud_volume():
    global volume
    volume_btn = SystemButton(400, 135)
    volume += 10
    volume_btn.draw(460, 200, 'settings_btns.png', f'Volume {volume}%')
    if volume == 110:
        volume = 0


def quiet_volume():
    global volume
    volume_btn = SystemButton(400, 135)
    volume -= 10
    volume_btn.draw(460, 200, 'settings_btns.png', f'Volume {volume}%')
    if volume == -10:
        volume = 100


def increase_difficult():
    global change_difficult
    difficulty_btn = SystemButton(400, 135)
    change_difficult += 1
    if change_difficult == 4:
        change_difficult = 0
        difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")
    difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")


def reduce_difficult():
    global change_difficult
    difficulty_btn = SystemButton(400, 135)
    change_difficult -= 1
    difficulty_btn.draw(460, 355, 'settings_btns.png', f"Difficulty: {DIFFICULTY[change_difficult]}")
    if change_difficult == -1:
        change_difficult = 3


def change_language():
    global select_lang
    language_btn = SystemButton(400, 135)
    select_lang += 1
    if select_lang == 2:
        select_lang = 0
        language_btn.draw(460, 510, 'settings_btns.png', f'Language: {LANGUAGES[select_lang % 2]}')
    language_btn.draw(460, 510, 'settings_btns.png', f'Language: {LANGUAGES[select_lang % 2]}')


def about_widget():
    about = pygame.transform.scale(load_image('about.png'), (700, 600))
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False

        screen.blit(about, (300, 40))
        pygame.display.update()


def game():
    running = True

    level = Level("maps/level.tmx", screen)

    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        level.run()
        pygame.display.flip()

        pygame.display.update()
        clock.tick(60)


def get_event(sprite, event):
    if sprite.rect.collidepoint(event.pos):
        pass


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    game()
