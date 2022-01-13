import os
import pygame
import sys

import pytmx

from Mobs import Mob, Coin, Hp, Diamond, Water

from tiles import Tile

from player import Traveler

from particles import ParticleEffect, HitEffect
from level_select import TravelGuide

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
score = 0
count_diamond = 0
all_sprites = pygame.sprite.Group()
MENU_BTN_SOUND = pygame.mixer.Sound('sounds/menu_btn.wav')
pos_of_player = [256, 448]
overworld = TravelGuide()
clock = pygame.time.Clock()


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


class Button:
    """ Класс кнопок для создания непосредственно самих конпок """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, message, button_image, action=None, font_size=30, type_id=None):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)),
                        (x, y - 5))
            font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
                x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2) - 5))
            if clicked[0]:
                pygame.mixer.Sound.play(MENU_BTN_SOUND)
                pygame.time.delay(300)
                if type_id is not None:
                    overworld.update_current_level(type_id)
                    game()

                else:
                    if action is not None:
                        action()
        else:
            screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y))
            font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size)
            text = font.render(message, True, 'white')
            screen.blit(text, (
                x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))


class SystemButton:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, image, message, font_size=50):
        screen.blit(pygame.transform.scale(load_image(image), (self.width, self.height)), (x, y))
        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size)
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
    name = FunctionCallDrawing('images/background_2.jpg', [(460, 100)],
                               [[(80, 80), 'Story mode', 'btn.png', start_map_guide()]])
    name.run()


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
                if len(self.name_coords_fun) >= 6:
                    self.buttons[i].draw(self.name_coords_fun[i][0][0],
                                         self.name_coords_fun[i][0][1],
                                         self.name_coords_fun[i][1],
                                         self.name_coords_fun[i][2],
                                         self.name_coords_fun[i][3], type_id=self.name_coords_fun[i][4])
                else:

                    self.buttons[i].draw(self.name_coords_fun[i][0][0],
                                         self.name_coords_fun[i][0][1],
                                         self.name_coords_fun[i][1],
                                         self.name_coords_fun[i][2],
                                         self.name_coords_fun[i][3])
            pygame.display.update()


class Level:
    def __init__(self, path, surface, p_cord, coins_coord, enemy_coord,
                 const_coord, scroll_count):  # Принимает карту(список) и  скрин

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
        self.water_2 = pygame.sprite.Group()
        self.hit_animated = False

        self.player_cords = p_cord
        self.coins_cords = coins_coord
        self.enemy_cords = enemy_coord
        self.constrains_cords = const_coord
        self.scroll_count = scroll_count

        self.gold_coins = pygame.sprite.Group()
        self.health_player_images = pygame.sprite.Group()
        self.diamond_coins = pygame.sprite.Group()

        self.screen = surface  # скрин

        self.hp_class = Hp()

        # добавление карты
        self.world_shift = 10  # скорость передвижения камеры
        self.current_x = 160

        self.dust_sprite = pygame.sprite.GroupSingle()  # группа с частицами
        self.player_on_ground = False
        self.path = path
        self.map = pytmx.load_pygame(self.path)
        self.layers = self.map.layers
        self.num_of_layers = len(self.layers)
        self.count_hit_anim = 0

        self.height_map = self.map.height
        self.width_map = self.map.width
        self.tile_size = self.map.tilewidth * 2
        self.count_camera = 90
        self.coins_flag = False
        self.change = 20
        self.running_now = True
        self.death = False

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

    def create_hit_particles(self):

        if self.travaler.direction_to_the_right:

            fall_dust_particle = HitEffect((self.travaler.rect.midbottom[0],
                                            self.travaler.rect.midbottom[1] - 15), 'hit')

        else:

            fall_dust_particle = HitEffect(
                (self.travaler.rect.midbottom[0], self.travaler.rect.midbottom[1] - 15), 'hit')
        self.dust_sprite.add(fall_dust_particle)

    def get_player_on_ground(self):
        if self.travaler.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.travaler.on_ground \
                and not self.dust_sprite.sprites():

            if self.travaler.direction_to_the_right:

                fall_dust_particle = ParticleEffect((self.travaler.rect.midbottom[0],
                                                     self.travaler.rect.midbottom[1] - 15), 'land')

            else:

                fall_dust_particle = ParticleEffect(
                    (self.travaler.rect.midbottom[0], self.travaler.rect.midbottom[1] - 15), 'land')
            self.dust_sprite.add(fall_dust_particle)

    def render(self):

        self.travaler = Traveler(self.player_cords, self.screen, self.create_jump_particles, self.change)
        self.player_group.add(self.travaler)
        self.diamond_im = Diamond((10, 60), self.tile_size)
        self.diamond_coins.add(self.diamond_im)

        for i in range(30):
            water = Water((i * 32 + 275 * i, 800), self.tile_size)
            self.water.add(water)
        for pos in self.enemy_cords:
            enemy = Mob(pos, self.tile_size, 40, 2)
            self.enemies.add(enemy)
        for pos in self.coins_cords[1]:
            print(self.coins_cords[1])
            print(pos)
            print('error')
            enemy = Coin(pos, self.tile_size, 1)
            self.gold_coins.add(enemy)

        for pos in self.coins_cords[0]:
            enemy = Coin(pos, self.tile_size, 5)

            self.gold_coins.add(enemy)

        for pos in self.coins_cords[2]:
            enemy = Coin(pos, self.tile_size, 2)
            self.gold_coins.add(enemy)

        for pos in self.coins_cords[3]:
            enemy = Coin(pos, self.tile_size, 3)
            self.gold_coins.add(enemy)

        for y in range(self.height_map):
            for x in range(self.width_map):
                for i in range(self.num_of_layers):
                    image = self.map.get_tile_image(x, y, i)

                    x_1 = x * self.tile_size
                    y_1 = y * self.tile_size

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

                        if (x_1, y_1) in self.constrains_cords:
                            tile = Tile((x_1, y_1), self.tile_size, image)
                            self.constraints.add(tile)
                        else:
                            # print(type(self.layers[i]))
                            if 'landscape' in str(self.layers[i]) or 'cubes' in str(self.layers[i]) or 'boxes' in str(
                                    self.layers[i]):
                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.tiles.add(tile)

                            if 'ground' in str(self.layers[i]):
                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.background_im.add(tile)


                            elif 'checkpoint' in str(self.layers[i]):
                                tile = Tile((x_1, y_1), self.tile_size, image)

                                self.checkpoint.add(tile)

                            elif 'water' in str(self.layers[i]):
                                pass


                            else:

                                tile = Tile((x_1, y_1), self.tile_size, image)
                                self.decorations.add(tile)

    def scroll_x(self):
        player_x = self.travaler.rect.centerx
        direction_x = self.travaler.direction

        if self.running_now:
            self.world_shift = self.scroll_count
            self.travaler.speed = 0

        elif player_x < WIDTH / 4 and direction_x[0] < 0:

            self.world_shift = 6
            self.travaler.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x[0] > 0:

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
            self.travaler.player_hp = 0

    def check_enemy_collisions(self):
        global score

        enemy_collisions = pygame.sprite.spritecollide(self.player_group.sprite, self.enemies, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player_group.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player_group.sprite.direction[1] >= 0:
                    self.player_group.sprite.direction[1] = -15
                    #  explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    score += 20

                    enemy.kill()
                else:

                    self.travaler.get_damage(enemy.return_hit())
                    if not self.hit_animated:
                        self.hit_animated = True
                        self.create_hit_particles()
                    else:
                        if self.count_hit_anim == 10:
                            self.hit_animated = False
                            self.count_hit_anim = 0
                        else:
                            self.count_hit_anim += 1

    def check_coins_collisions(self):
        global score
        global count_diamond

        coin_collisions = pygame.sprite.spritecollide(self.player_group.sprite, self.gold_coins, False)

        if coin_collisions:
            for coin in coin_collisions:

                name, count = coin.collisions()
                if name == 's':
                    score += count
                elif name == 's_d':
                    count_diamond += 1
                    score += count
                elif name == 'h':

                    self.travaler.player_hp += count + 50
                    if self.travaler.player_hp > 300:
                        self.travaler.player_hp = 300

                coin.kill()

    def check_death(self):
        return True if self.death else False

    def rect_y_coins(self):
        if not self.coins_flag:
            for sprite in self.gold_coins.sprites():
                sprite.rect.y += 19
            self.coins_flag = True

    def check_player_hp(self):
        if self.travaler.player_hp <= 0:
            self.death = True

    def diamond(self):

        pos = 10, 50

        enemy = Diamond(pos, self.tile_size)

        enemy.update()

    def health(self):

        count = self.travaler.return_hp()
        images = self.hp_class.return_image(count)

        pos = 40, 10
        for i in range(len(images)):
            screen.blit(images[i], (pos[0] * i + 10, pos[1]))

    def draw_score(self):
        global score

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 20)
        text = font.render(f"SCORE: {score}", True, (0, 0, 0))
        text_x = 1080
        text_y = 20
        self.screen.blit(text, (text_x, text_y))

    def draw_count_diamond(self):
        global count_diamond

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 25)
        text = font.render(f"{count_diamond}", True, (0, 0, 0))
        text_x = 50
        text_y = 70
        self.screen.blit(text, (text_x, text_y))

    def run(self):
        self.background_im.update(self.world_shift)

        self.background_im.draw(self.screen)
        self.decorations.update(self.world_shift)

        self.decorations.draw(self.screen)

        self.tiles.update(self.world_shift)

        self.tiles.draw(self.screen)

        self.enemies.update(self.world_shift)

        self.constraints.update(self.world_shift)
        self.gold_coins.update(self.world_shift)

        self.constraints.draw(self.screen)

        self.enemy_collision_reverse()

        self.enemies.draw(self.screen)
        self.rect_y_coins()
        self.gold_coins.draw(self.screen)

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
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.screen)

        self.draw_score()
        self.health()

        self.diamond_coins.update()
        self.diamond_coins.draw(self.screen)
        self.draw_count_diamond()

        self.check_enemy_collisions()
        self.check_coins_collisions()
        self.water_collision()
        self.check_player_hp()


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

    level_map = overworld.return_map()
    player_coordinates = overworld.return_hero_coords()
    coins_coordinates = overworld.return_coins_coords()
    enemy_coordinates = overworld.return_enemy_coords()
    constrains_coordinates = overworld.return_constrains_coords()
    scroll_count = overworld.return_scroll_x()
    level = Level(level_map, screen, player_coordinates, coins_coordinates, enemy_coordinates, constrains_coordinates,
                  scroll_count)

    while running:

        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        level.run()

        if level.check_death():
            running = False

            level = Level(level_map, screen, player_coordinates, coins_coordinates, enemy_coordinates,
                          constrains_coordinates,
                          scroll_count)

        pygame.display.flip()
        clock.tick(60)

    start_map_guide()


def start_map_guide():
    name = FunctionCallDrawing('images/background_5.jpg',
                               [(150 * 1.9, 100 * 1.9), (150 * 1.9, 100 * 1.9), (150 * 1.9, 100 * 1.9),
                                (150 * 1.9, 100 * 1.9), (150 * 1.9, 100 * 1.9), (150 * 1.9, 100 * 1.9)],
                               [[(89, 67), '1 LEVEL', 'level_btn.png', game, 1],
                                [(505, 67), '2 LEVEL', 'level_btn.png', game, 2],
                                [(905, 67), '3 LEVEL', 'level_btn.png', game, 3],
                                [(89, 400), '4 LEVEL', 'level_btn.png', game, 4],
                                [(505, 400), '5 LEVEL', 'level_btn.png', game, 5],
                                [(905, 400), '6 LEVEL', 'level_btn.png', game, 6]])
    name.run()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    show_menu()
