import os
import pygame
import sys
import sqlite3
import pytmx

from Mobs import Mob, Coin, Hp, Diamond, Water

from tiles import Tile

from player import Traveler

from particles import ParticleEffect, HitEffect
from level_select import TravelGuide

pygame.init()
pygame.display.set_caption('pygame-project')

SIZE = WIDTH, HEIGHT = 1280, 764
# screen = pygame.display.set_mode((1280, 764), pygame.FULLSCREEN)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
left = False
right = False
volume = 0.5
change_difficult = 0
select_lang = 0
animCount = 8
score = 0
count_diamond = 0
count_enemy_kills = 0
all_sprites = pygame.sprite.Group()
pos_of_player = [256, 448]
overworld = TravelGuide()
clock = pygame.time.Clock()
player_name = ""
con = sqlite3.connect('../database/scores.db')
cur = con.cursor()


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
POWER_UP_SOUND = pygame.mixer.Sound('sounds/power_up.wav')
FOR_MENU_SOUND = pygame.mixer.Sound('sounds/for_menu.wav')
FOR_OTHER_SOUND = pygame.mixer.Sound('sounds/for_other.wav')
COIN_SOUND = pygame.mixer.Sound('sounds/coin.wav')
HIT_SOUND = pygame.mixer.Sound('sounds/hit.wav')
GAME_OVER_SOUND = pygame.mixer.Sound('sounds/g_over.wav')
KILL_SOUND = pygame.mixer.Sound('sounds/stomp.wav')
FINAL_SOUND = pygame.mixer.Sound('sounds/final_sound.wav')

now_play = FOR_OTHER_SOUND


class Button:
    """ Класс кнопок для создания непосредственно самих конпок """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, message, button_image, action=None, font_size=30, type_id=None, not_image=False):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            if not not_image:
                screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)),
                            (x, y - 5))

            if type_id is not None:
                font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size + 10)
                text = font.render(message, True, 'white')
                screen.blit(text, (
                    x + ((self.width - text.get_width()) // 2) + 2, y + ((self.height - text.get_height()) // 2) + 25))
            else:
                font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size + 10)
                text = font.render(message, True, 'white')
                screen.blit(text, (
                    x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2) - 5))
            if clicked[0]:

                pygame.mixer.Sound.play(MENU_BTN_SOUND)

                pygame.mixer.Sound.stop(now_play)

                pygame.time.delay(300)

                self.check_clicked = True
                if type_id is not None:
                    if overworld.check_open_level(type_id):
                        overworld.update_current_level(type_id)
                        game()

                else:
                    if action is not None:
                        action()
                        pygame.mixer.Sound.play(now_play, loops=-1)


        else:
            if not not_image:
                screen.blit(pygame.transform.scale(load_image(button_image), (self.width, self.height)), (x, y))

            if type_id is not None:
                font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size + 10)
                text = font.render(message, True, 'white')
                screen.blit(text, (
                    x + ((self.width - text.get_width()) // 2) + 2, y + ((self.height - text.get_height()) // 2) + 30))
            else:
                font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', font_size)
                text = font.render(message, True, 'white')
                screen.blit(text, (
                    x + ((self.width - text.get_width()) // 2), y + ((self.height - text.get_height()) // 2)))

    def is_clicked(self, x, y):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if (x < mouse_pos_x < x + self.width) and (y < mouse_pos_y < y + self.height):
            if clicked[0]:
                return True
            else:
                return False

def show_menu():
    global now_play
    """ Отрисовка самого меню """


    pygame.mixer.Sound.stop(now_play)

    menu_background = load_image('for_menu_3.png')
    now_play = FOR_MENU_SOUND
    pygame.mixer.Sound.play(now_play, loops=-1)


    show_menu_f = True
    start_btn = Button(300, 70)
    settings_btn = Button(300, 70)
    scores_btn = Button(300, 70)
    help_btn = Button(300, 70)
    exit_btn = Button(300, 70)
    font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 60)
    text = font.render("Traveler:", True, (0, 255, 255))


    while show_menu_f:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        start_btn.draw(WIDTH // 2 - text.get_width() // 2, HEIGHT - 500, 'start', 'btn_menu.png', start_player_input,
                       font_size=40)
        settings_btn.draw(WIDTH // 2 - text.get_width() // 2, HEIGHT - 410, 'settings', 'btn_menu.png', settings,
                          font_size=40)
        scores_btn.draw(WIDTH // 2 - text.get_width() // 2, HEIGHT - 320, 'scores', 'btn_menu.png', scores,
                        font_size=40)
        exit_btn.draw(WIDTH // 2 - text.get_width() // 2, HEIGHT - 140, 'exit', 'btn_menu.png', terminate, font_size=40)
        help_btn.draw(WIDTH // 2 - text.get_width() // 2, HEIGHT - 230, 'help', 'btn_menu.png', help_menu, font_size=40)
        pygame.display.update()


class Level:
    def __init__(self, path, surface, p_cord, coins_coord, enemy_coord,
                 const_coord, scroll_count, details):  # Принимает карту(список) и  скрин

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

        self.restart_draw_count = 0

        self.score = 0
        self.diamond_count = 0
        self.mobs_details = details

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
        self.enemy_kills = 0

        self.height_map = self.map.height
        self.width_map = self.map.width
        self.tile_size = self.map.tilewidth * 2
        self.count_camera = 90
        self.coins_flag = False
        self.change = 10
        self.running_now = True
        self.death = False
        self.passed = False

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
            enemy = Mob(pos, self.tile_size, self.mobs_details[1], self.mobs_details[0])
            self.enemies.add(enemy)
        for pos in self.coins_cords[1]:
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

    def checkpoint_collision(self):

        if pygame.sprite.spritecollide(self.travaler, self.checkpoint, False):
            overworld.update_current_level_pluse()
            self.passed = True

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
                    self.score += 20
                    self.enemy_kills += 1
                    pygame.mixer.Sound.play(KILL_SOUND)
                    enemy.kill()
                else:

                    self.travaler.get_damage(enemy.return_hit())

                    if not self.hit_animated:
                        self.hit_animated = True
                        self.create_hit_particles()
                        pygame.mixer.Sound.play(HIT_SOUND)
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
                    self.score += count
                    pygame.mixer.Sound.play(COIN_SOUND)

                elif name == 's_d':
                    self.diamond_count += 1
                    self.score += count
                    pygame.mixer.Sound.play(COIN_SOUND)

                elif name == 'h':
                    pygame.mixer.Sound.play(POWER_UP_SOUND)

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
            pygame.mixer.Sound.play(GAME_OVER_SOUND)


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
        text = font.render(f"SCORE: {score + self.score}", True, (0, 0, 0))
        text_x = 1080
        text_y = 20
        self.screen.blit(text, (text_x, text_y))

    def draw_count_diamond(self):
        global count_diamond

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 25)
        text = font.render(f"{self.diamond_count + count_diamond}", True, (0, 0, 0))
        text_x = 50
        text_y = 70
        self.screen.blit(text, (text_x, text_y))

    def draw_restart_text(self):

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 45)
        text = font.render("press SPACE to restart", True, (255, 255, 255))
        if self.restart_draw_count >= 30:
            self.restart_draw_count = 0
            if self.change > 0:
                self.change *= - 1
            else:
                self.change *= - 1
        else:
            self.restart_draw_count += 1
        text_x = 300
        text_y = 650 + self.change
        self.screen.blit(text, (text_x, text_y))

    def draw_final_text(self):

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 45)
        font_for_win = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 50)
        text = font.render("press ESCAPE to go to the menu", True, (255, 255, 255))
        text_score = font.render(f"Your score: {score}", True, (255, 255, 255))
        text_win = font_for_win.render("You passed the game", True, (255, 255, 255))
        text_diamond = font.render(f"Number of diamonds: {count_diamond}", True, (255, 255, 255))
        text_count_kills = font.render(f"Number of kills: {count_enemy_kills}", True, (255, 255, 255))

        if self.restart_draw_count > 20:
            self.restart_draw_count = 0
            if self.change > 0:
                self.change *= - 1
            else:
                self.change *= - 1
        else:
            self.restart_draw_count += 1
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = 650 + self.change
        self.screen.blit(text, (text_x, text_y))
        self.screen.blit(text_win, (WIDTH // 2 - text_win.get_width() // 2, 15))
        self.screen.blit(text_score, (20, 150))
        self.screen.blit(text_diamond, (20, 250))
        self.screen.blit(text_count_kills, (20, 350))

    def draw_escape_text(self):

        font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 40)
        text = font.render("press ENTER to continue or ESCAPE to exit", True, (255, 255, 255))
        if self.restart_draw_count >= 30:
            self.restart_draw_count = 0
            if self.change > 0:
                self.change *= - 1
            else:
                self.change *= - 1
        else:
            self.restart_draw_count += 1
        text_x = 60
        text_y = 650 + self.change
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

        self.player_group.update(self.running_now)
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
        self.checkpoint_collision()
        self.water_collision()
        self.check_player_hp()

    def draw_for_restart(self):

        self.background_im.draw(self.screen)

        self.decorations.draw(self.screen)

        self.tiles.draw(self.screen)

        self.constraints.draw(self.screen)

        self.enemies.draw(self.screen)

        self.gold_coins.draw(self.screen)

        self.checkpoint.draw(self.screen)

        self.water.draw(self.screen)
        self.draw_score()
        self.health()

        self.diamond_coins.draw(self.screen)
        self.draw_count_diamond()

        self.player_group.draw(self.screen)

        self.dust_sprite.draw(self.screen)

        self.diamond_coins.draw(self.screen)


def text_write(x, y, message, font_size=50):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, 'white')
    screen.blit(text,
                (x + ((400 - text.get_width()) // 2), y + ((135 - text.get_height()) // 2)))


def settings():
    global now_play
    pygame.mixer.Sound.stop(now_play)

    now_play = FOR_OTHER_SOUND
    pygame.mixer.Sound.play(FOR_OTHER_SOUND, loops=-1)

    disables = Button(100, 100)
    enabled = Button(100, 100)
    pluse = Button(100, 100)
    minuse = Button(100, 100)
    show = True
    font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 60)
    text = font.render(f"volume:{round(volume, 1)} ", True, (0, 0, 0))
    while show:
        screen.fill('grey')
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
                    show_menu()
        disables.draw(WIDTH // 2 - 300, HEIGHT // 2, '', 'disabled.png', disabled_volume
                      )
        enabled.draw(WIDTH // 2 - 100, HEIGHT // 2, '', 'enabled.png', enabled_volume
                     )
        pluse.draw(WIDTH // 2 + 100, HEIGHT // 2, '', 'pluse.png', loud_volume
                   )
        minuse.draw(WIDTH // 2 + 300, HEIGHT // 2, '', 'minuse.png', quiet_volume
                    )
        text = font.render(f"volume:{round(volume, 1)} ", True, (0, 0, 0))
        now_play = FOR_OTHER_SOUND
        pygame.display.update()


def scores():
    global now_play
    pygame.mixer.Sound.stop(now_play)

    now_play = FOR_OTHER_SOUND

    pygame.mixer.Sound.play(now_play, loops=-1)


    font = pygame.font.Font('../graphics/font/ARCADEPI.TTF', 40)
    base_font = pygame.font.Font(None, 32)
    x_n = 150
    x_s = 450
    x_d = 750
    y = 60
    y_i = [120]

    score_information = cur.execute(
        f"""SELECT score, diamonds, player.name from scores, player WHERE player.id == player_id ORDER BY score""").fetchall()[
                        ::-1]
    print(score_information)
    for i in range(len(score_information)):
        y_i.append(y_i[-1] + 60)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show = False
                    pygame.mixer.Sound.stop(now_play)
                    show_menu()
        text_name = font.render('Name', True, 'white')
        text_score = font.render('Score', True, 'white')
        text_diamonds = font.render('Diamonds', True, 'white')
        screen.fill('black')
        screen.blit(text_name, (x_n, y))
        screen.blit(text_score, (x_s, y))
        screen.blit(text_diamonds, (x_d, y))
        if len(score_information) > 10:
            for i in range(10):
                surface_score = base_font.render(str(score_information[i][0]), True, 'white')
                surface_diamond = base_font.render(str(score_information[i][1]), True, 'white')
                surface_name = base_font.render(str(score_information[i][2]), True, 'white')
                screen.blit(surface_score, (x_s + 60, y_i[i]))
                screen.blit(surface_diamond, (x_d + 60, y_i[i]))
                screen.blit(surface_name, (x_n, y_i[i]))
        else:
            for i in range(len(score_information)):
                surface_score = base_font.render(str(score_information[i][0]), True, 'white')
                surface_diamond = base_font.render(str(score_information[i][1]), True, 'white')
                surface_name = base_font.render(str(score_information[i][2]), True, 'white')
                screen.blit(surface_score, (x_s + 20, y_i[i]))
                screen.blit(surface_diamond, (x_d + 20, y_i[i]))
                screen.blit(surface_name, (x_n, y_i[i]))
        pygame.display.update()


def help_menu():

    pygame.mixer.Sound.play(FOR_OTHER_SOUND, loops=-1)
    now_play = FOR_OTHER_SOUND

    show = True
    count = 0
    anim_count = 1
    animations_A_key = [load_image('A.png', dictor='../graphics/keyboard/'),
                        load_image('A_Pressed.png', dictor='../graphics/keyboard/')]
    animations_A_key = [pygame.transform.scale(i,
                                               (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                        animations_A_key]
    animations_D_key = [load_image('D.png', dictor='../graphics/keyboard/'),
                        load_image('D_Pressed.png', dictor='../graphics/keyboard/')]
    animations_D_key = [pygame.transform.scale(i,
                                               (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                        animations_D_key]

    animations_left_key = [load_image('Left.png', dictor='../graphics/keyboard/'),
                           load_image('Left_Pressed.png', dictor='../graphics/keyboard/')]
    animations_left_key = [pygame.transform.scale(i,
                                                  (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                           animations_left_key]

    animations_right_key = [load_image('Right.png', dictor='../graphics/keyboard/'),
                            load_image('Right_Pressed.png', dictor='../graphics/keyboard/')]
    animations_right_key = [pygame.transform.scale(i,
                                                   (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                            animations_right_key]

    animations_W_key = [load_image('W.png', dictor='../graphics/keyboard/'),
                        load_image('W_Pressed.png', dictor='../graphics/keyboard/')]
    animations_W_key = [pygame.transform.scale(i,
                                               (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                        animations_W_key]

    animations_UP_key = [load_image('UP.png', dictor='../graphics/keyboard/'),
                         load_image('UP_Pressed.png', dictor='../graphics/keyboard/')]
    animations_UP_key = [pygame.transform.scale(i,
                                                (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                         animations_UP_key]

    animations_space_key = [load_image('Space.png', dictor='../graphics/keyboard/'),
                            load_image('Space_Pressed.png', dictor='../graphics/keyboard/')]
    animations_space_key = [pygame.transform.scale(i,
                                                   (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                            animations_space_key]

    animations_escape_key = [load_image('Escape.png', dictor='../graphics/keyboard/'),
                             load_image('Escape_Pressed.png', dictor='../graphics/keyboard/')]
    animations_escape_key = [pygame.transform.scale(i,
                                                    (int(i.get_width() // 2), int(i.get_height() // 2))) for i in
                             animations_escape_key]

    animations_mob = [load_image('Walk_1.png', dictor='../graphics/enemies/Walk/'),
                      load_image('Walk_2.png', dictor='../graphics/enemies/Walk/'),
                      load_image('Walk_3.png', dictor='../graphics/enemies/Walk/'),
                      load_image('Walk_4.png', dictor='../graphics/enemies/Walk/')]
    animations_mob = [pygame.transform.scale(i,
                                             (int(i.get_width() * 4), int(i.get_height() * 4))) for i in
                      animations_mob]
    animations_coin = [load_image('MonedaD_1.png', dictor='../graphics/Coins/'),
                       load_image('MonedaD_2.png', dictor='../graphics/Coins/'),
                       load_image('MonedaD_3.png', dictor='../graphics/Coins/'),
                       load_image('MonedaD_4.png', dictor='../graphics/Coins/'),
                       load_image('MonedaD_5.png', dictor='../graphics/Coins/')
                       ]
    animations_coin = [pygame.transform.scale(i,
                                              (int(i.get_width() * 4), int(i.get_height() * 4))) for i in
                       animations_coin]

    font = pygame.font.Font('../graphics/font/ARCADEPI.ttf', 45)
    text = font.render("keys to move horizontally", True, (0, 0, 0))
    text1 = font.render("jump", True, (0, 0, 0))
    text2 = font.render("return", True, (0, 0, 0))
    text3 = font.render("enemy. they deal damage carefully", True, (0, 0, 0))
    text4 = font.render("coins that increase your scoreboard", True, (0, 0, 0))
    text_r = font.render("press ESCAPE to restart", True, (21, 21, 21))
    text_x = 500
    text_y = 50
    count_for_mob = 0

    count_for_coin = 0
    while show:
        screen.fill('grey')
        screen.blit(text, (text_x, text_y))
        screen.blit(text1, (800, 160))
        screen.blit(text2, (170, 270))
        screen.blit(text3, (170, 370))
        screen.blit(text4, (170, 470))

        if count > 1000:
            anim_count *= -1
            count = 0


        else:
            count += 1
            if anim_count > 0:
                screen.blit(animations_A_key[0], (20, 30))
                screen.blit(animations_D_key[0], (130, 30))
                screen.blit(animations_left_key[0], (280, 30))
                screen.blit(animations_right_key[0], (390, 30))
                screen.blit(animations_W_key[0], (20, 140))
                screen.blit(animations_UP_key[0], (130, 140))
                screen.blit(animations_space_key[0], (240, 140))
                screen.blit(animations_escape_key[0], (20, 250))
                screen.blit(text_r, (WIDTH // 2 - text_r.get_width() // 2, 620))


            else:
                screen.blit(animations_A_key[1], (20, 30))
                screen.blit(animations_D_key[1], (130, 30))
                screen.blit(animations_left_key[1], (280, 30))
                screen.blit(animations_right_key[1], (390, 30))
                screen.blit(animations_W_key[1], (20, 140))
                screen.blit(animations_UP_key[1], (130, 140))
                screen.blit(animations_space_key[1], (240, 140))
                screen.blit(animations_escape_key[1], (20, 250))
                screen.blit(text_r, (WIDTH // 2 - text_r.get_width() // 2, 620 - 10))
        if count_for_mob >= 3:
            count_for_mob = 0
        else:
            count_for_mob += 0.01

        if count_for_coin >= 4:
            count_for_coin = 0
        else:
            count_for_coin += 0.01
        screen.blit(animations_mob[int(count_for_mob)], (10, 320))
        screen.blit(animations_coin[int(count_for_coin)], (25, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.stop(now_play)

                    show = False
                    show_menu()

        pygame.display.update()


def loud_volume():
    global volume
    volume += 0.1
    if volume > 1:
        volume = 1

    MENU_BTN_SOUND.set_volume(volume)

    POWER_UP_SOUND.set_volume(volume)
    FOR_MENU_SOUND.set_volume(volume)
    FOR_OTHER_SOUND.set_volume(volume)
    COIN_SOUND.set_volume(volume)
    HIT_SOUND.set_volume(volume)
    GAME_OVER_SOUND.set_volume(volume)
    KILL_SOUND.set_volume(volume)
    FINAL_SOUND.set_volume(volume)


def quiet_volume():
    global volume
    volume -= 0.1
    if volume < 0:
        volume = 0
    MENU_BTN_SOUND.set_volume(volume)

    POWER_UP_SOUND.set_volume(volume)
    FOR_MENU_SOUND.set_volume(volume)
    FOR_OTHER_SOUND.set_volume(volume)
    COIN_SOUND.set_volume(volume)
    HIT_SOUND.set_volume(volume)
    GAME_OVER_SOUND.set_volume(volume)
    KILL_SOUND.set_volume(volume)
    FINAL_SOUND.set_volume(volume)


def disabled_volume():
    global volume
    volume = 0
    MENU_BTN_SOUND.set_volume(volume)

    POWER_UP_SOUND.set_volume(volume)
    FOR_MENU_SOUND.set_volume(volume)
    FOR_OTHER_SOUND.set_volume(volume)
    COIN_SOUND.set_volume(volume)
    HIT_SOUND.set_volume(volume)
    GAME_OVER_SOUND.set_volume(volume)
    KILL_SOUND.set_volume(volume)
    FINAL_SOUND.set_volume(volume)


def enabled_volume():
    global volume
    volume = 0.5
    MENU_BTN_SOUND.set_volume(volume)

    POWER_UP_SOUND.set_volume(volume)
    FOR_MENU_SOUND.set_volume(volume)
    FOR_OTHER_SOUND.set_volume(volume)
    COIN_SOUND.set_volume(volume)
    HIT_SOUND.set_volume(volume)
    GAME_OVER_SOUND.set_volume(volume)
    KILL_SOUND.set_volume(volume)
    FINAL_SOUND.set_volume(volume)


def game():
    global score
    global count_diamond
    global count_enemy_kills
    global player_name
    running = True


    level_map = overworld.return_map()
    player_coordinates = overworld.return_hero_coords()
    coins_coordinates = overworld.return_coins_coords()
    enemy_coordinates = overworld.return_enemy_coords()
    constrains_coordinates = overworld.return_constrains_coords()
    scroll_count = overworld.return_scroll_x()
    mobs_details = overworld.return_mobs_damage_type_id()
    level = Level(level_map, screen, player_coordinates, coins_coordinates, enemy_coordinates, constrains_coordinates,
                  scroll_count, mobs_details)

    while running:

        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            escape_flag = True
            while escape_flag:
                level.draw_for_restart()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            escape_flag = False
                            running = False
                        if event.key == pygame.K_RETURN:
                            escape_flag = False

                level.draw_escape_text()

                pygame.display.flip()
                clock.tick(60)

        level.run()

        if level.passed:
            print(player_name)
            score += level.score
            count_diamond += level.diamond_count
            count_enemy_kills += level.enemy_kills
            cur.execute(
                f"""UPDATE scores set score = {score} 
                                   where player_id = (select id from player where name = '{player_name}')""")
            cur.execute(
                f"""UPDATE scores set diamonds = {count_diamond} 
                                    where player_id = (select id from player where name = '{player_name}')""")
            cur.execute(
                f"""UPDATE scores set open_levels = {overworld.return_open_levels()} 
                                                where player_id = (select id from player where name = '{player_name}')""")

            cur.execute(
                f"""UPDATE scores set enemies = {count_enemy_kills} 
                                                           where player_id = (select id from player where name = '{player_name}')""")

            con.commit()
            if overworld.current_level == 7:
                global now_play
                final_form = True
                pygame.mixer.Sound.stop(now_play)

                now_play = FINAL_SOUND
                pygame.mixer.Sound.play(now_play, loops=-1)


                while final_form:
                    screen.fill('black')

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                                final_form = False

                    level.draw_final_text()

                    pygame.display.flip()
                    clock.tick(60)

            else:
                game()

        if level.check_death():

            restart_flag = True
            while restart_flag:
                level.draw_for_restart()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            restart_flag = False
                        if event.key == pygame.K_SPACE:
                            restart_flag = False
                            level = Level(level_map, screen, player_coordinates, coins_coordinates, enemy_coordinates,
                                          constrains_coordinates,
                                          scroll_count, mobs_details)

                level.draw_restart_text()

                pygame.display.flip()
                clock.tick(60)

        pygame.display.flip()
        clock.tick(60)
    print(1)

    start_map_guide()


def start_player_input():
    global player_name
    global score
    global count_diamond
    global now_play
    global count_enemy_kills

    pygame.mixer.Sound.stop(now_play)
    now_play = FOR_OTHER_SOUND
    pygame.mixer.Sound.play(now_play, loops=-1)


    continue_btn = Button(350, 100)
    base_font = pygame.font.Font(None, 48)
    font = pygame.font.Font('../graphics/font/ARCADEPI.TTF', 40)
    name = ""
    input_rect = pygame.Rect(390, 320, 500, 65)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color_rect = color_passive
    active = False
    pygame.key.set_repeat(250, 0)
    if __name__ == "__main__":

        running = True
        while running:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        acive = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        show_menu()

                    if event.key == pygame.K_BACKSPACE:
                        active = True
                        name = name[:-1]

                    else:
                        if active:
                            if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == '_':
                                name += event.unicode
            screen.blit(load_image('for_menu.png'), (0, 0))

            if active:
                color_rect = color_active
            else:
                color_rect = color_passive

            pygame.draw.rect(screen, color_rect, input_rect, 2)

            text_surface = base_font.render(name, True, ' white')
            text = font.render('Input your name:', True, 'white')
            if text_surface.get_width() > input_rect.w - 19:
                active = False

            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 16))
            screen.blit(text, (input_rect.x, input_rect.y - 46))
            if name:

                if continue_btn.is_clicked(450, 450):
                    player_name = name
                    players_in_bd = [str(i[0]) for i in cur.execute(f"SELECT name from player").fetchall()]
                    length = len(players_in_bd) + 1
                    if str(name) in players_in_bd:
                        player_information = cur.execute(
                            f"""SELECT score, diamonds, open_levels, enemies from scores 
                                                    WHERE player_id = (SELECT id FROM player WHERE name = '{name}')""").fetchall()
                        score = player_information[0][0]
                        count_diamond = player_information[0][1]
                        open_level = player_information[0][2]
                        overworld.close_all()
                        print(overworld.levels_open)
                        overworld.update_open_levels(open_level)
                        count_enemy_kills = player_information[0][3]

                    else:
                        overworld.close_all()
                        cur.execute(f"""INSERT INTO player(name) VALUES('{name}')""")
                        cur.execute(f"""INSERT INTO scores(id, player_id) VALUES({length}, {length}) """)
                    con.commit()
                continue_btn.draw(450, 450, 'Continue', 'btn_menu.png', start_map_guide)

            pygame.display.flip()


def start_map_guide():
    global now_play

    pygame.mixer.Sound.stop(now_play)
    now_play = FOR_OTHER_SOUND
    pygame.mixer.Sound.play(now_play, loops=-1)

    if overworld.check_open_level(1):
        first_level_image = 'test_btn.png'
        first_level_text = '1 Level'
    else:
        first_level_image = 'test_btn.png'
        first_level_text = '1 Level'

    if overworld.check_open_level(2):
        second_level_image = 'test_btn.png'
        second_level_text = '2 Level'
    else:
        second_level_image = 'test_btn_close.png'
        second_level_text = ''

    if overworld.check_open_level(3):
        third_level_image = 'test_btn_2_1.png'
        third_level_text = '3 Level'
    else:
        third_level_image = 'test_btn_2_1_close.png'
        third_level_text = ''

    if overworld.check_open_level(4):
        fourth_level_image = 'test_btn_2_1.png'
        fourth_level_text = '4 Level'
    else:
        fourth_level_image = 'test_btn_2_1_close.png'
        fourth_level_text = ''

    if overworld.check_open_level(5):
        fifth_level_image = 'test_btn_4_1.png'
        fifth_level_text = '5 Level'
    else:
        fifth_level_image = 'test_btn_4_1_close.png'
        fifth_level_text = ''

    if overworld.check_open_level(6):
        sixth_level_image = 'test_btn_4_1.png'
        sixth_level_text = '6 Level'
    else:
        sixth_level_image = 'test_btn_4_1_close.png'
        sixth_level_text = ''

    menu_background = load_image('for_menu.png')
    running = True
    first_level = Button(150 * 1.9, 130 * 1.9)
    second_level = Button(150 * 1.9, 130 * 1.9)
    third_level = Button(150 * 1.9, 130 * 1.9)
    fourth_level = Button(150 * 1.9, 130 * 1.9)
    fifth_level = Button(150 * 1.9, 130 * 1.9)
    sixth_level = Button(150 * 1.9, 130 * 1.9)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                    pygame.mixer.Sound.stop(now_play)
                    show_menu()

        screen.blit(menu_background, (0, 0))

        first_level.draw(89, 27, first_level_text, first_level_image, game, type_id=1, font_size=40)
        second_level.draw(505, 27, second_level_text, second_level_image, game, type_id=2, font_size=40)
        third_level.draw(905, 27, third_level_text, third_level_image, game, type_id=3, font_size=40)
        fourth_level.draw(89, 360, fourth_level_text, fourth_level_image, game, type_id=4, font_size=40)
        fifth_level.draw(505, 360, fifth_level_text, fifth_level_image, game, type_id=5, font_size=40)
        sixth_level.draw(905, 360, sixth_level_text, sixth_level_image, game, type_id=6, font_size=40)

        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    show_menu()
