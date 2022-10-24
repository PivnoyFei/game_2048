from random import choice

import numpy as np
import pygame

import controls
import figure
from settings import FPS, GAME_RES, HALF_TILE, MY_FONT, RES, TILE, H, W

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
TRAFFIC_BLACK = (30, 30, 30)


class Py2048:
    def __init__(self):
        self.width_dict = {}
        for i in range(W):
            self.width_dict[i] = i * TILE
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.falling_sound = pygame.mixer.Sound('madia/falling_sound.mp3')
        self.merge_sound = pygame.mixer.Sound('madia/merge_sound.mp3')
        self.all_sprites = pygame.sprite.Group()
        pygame.display.set_caption("2048")
        pygame.display.set_icon(pygame.image.load("madia/two.png"))
        self.myfont_one = pygame.font.SysFont(MY_FONT, HALF_TILE - TILE // 8)
        self.myfont_two = pygame.font.SysFont(MY_FONT, HALF_TILE - TILE // 5)
        self.myfont_three = pygame.font.SysFont(MY_FONT, HALF_TILE - TILE // 4)
        self.myfont_four = pygame.font.SysFont(MY_FONT, HALF_TILE - TILE // 3)
        self.mini_myfont = pygame.font.SysFont(MY_FONT, HALF_TILE - TILE // 2)

        self.sc = pygame.display.set_mode(RES, pygame.DOUBLEBUF)
        self.sprite_sc = pygame.Surface(RES).convert_alpha()
        self.game_sc = pygame.Surface(GAME_RES).convert_alpha()
        self.alpha_sc = pygame.Surface(RES).convert_alpha()

        self.clock = pygame.time.Clock()

        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE
                                 ) for x in range(W) for y in range(H)]
        self.field = np.array([[0 for _ in range(W)] for _ in range(H)])

        self.x = (W // 2) * TILE + 2
        self.y = H * TILE - TILE + 2
        self.figures = pygame.Rect(self.x, self.y, TILE - 4, TILE - 4)

        self.new_num = lambda: choice([2, 4, 8, 16, 32, 64])
        self.next_num = self.new_num()
        self.num = self.next_num

        self.figure_rect = pygame.Rect(
            W * TILE - TILE + 2,
            H * TILE - TILE + 2,
            TILE - 4,
            TILE - 4)

        self.game_bg = pygame.image.load('madia/gradient.png').convert()

        self.figure = self.figures.copy()
        self.figure_2 = self.figures.copy()
        self.figure_3 = self.figures.copy()
        self.anim_count, self.anim_speed, self.anim_limit = 0, FPS, 2000

        self.paused = False

        self.record = self.get_record()
        self.score = 0

    def get_grid(self):
        """Отображает фигуры расположенные на поле."""
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x = x * TILE + 2
                    self.figure_rect.y = y * TILE + 2
                    figure.draw_figure(
                        self, self.game_sc, self.figure_rect, col)

    def check_figure(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dx + 1 < W:
            if self.field[dy, dx + 1] == self.field[dy, dx]:
                self.check_field_left()
        if dx - 1 >= 0:
            if self.field[dy, dx - 1] == self.field[dy, dx]:
                self.check_field_right()

    def check_field_folding(self):
        for y in range(1, H):
            for x in range(W):
                col = self.field[y, x]
                if col:
                    if 0 < x < W - 1:
                        if (
                            col == self.field[y - 1, x]
                            and col == self.field[y, x - 1]
                            and col == self.field[y, x + 1]
                        ):
                            self.field[y - 1, x] = 0
                            self.field[y, x - 1] = 0
                            self.field[y, x + 1] = 0
                            figure.get_folding_animation_cube(self, x, y, col)
                            self.field[y, x] = 0
                            figure.get_down_animation_cube(self, x, y, col)
                            self.field[y - 1, x] = col * 4
                            self.score += col * 4
                            return self.check_field_folding()

                    if self.field[y - 1, x] == col:
                        self.field[y - 1, x] = 0
                        figure.get_up_animation_cube(self, x, y - 1, col)
                        self.field[y, x] = 0
                        figure.get_down_animation_cube(self, x, y - 1, col * 2)
                        self.field[y - 1, x] = col * 2
                        self.score += col * 2
                        return self.check_field_folding()
                    if self.field[y - 1, x] == 0:
                        self.field[y, x] = 0
                        figure.get_down_animation_cube(self, x, y - 1, col)
                        self.field[y - 1, x] = col
                        return self.check_field_folding()

    def check_field_right(self):
        for y in range(H):
            for x in range(1, W):
                col = self.field[y, x]
                if col:
                    if self.field[y, x - 1] == col:
                        self.field[y, x - 1] = 0
                        figure.get_right_animation_cube(self, x, y, col)
                        self.field[y, x] = col * 2
                        self.score += self.field[y, x]
                        return self.check_field_folding()

    def check_field_left(self):
        for y in range(H):
            for x in range(W - 2):
                col = self.field[y, x]
                if col:
                    if self.field[y, x + 1] == col:
                        self.field[y, x + 1] = 0
                        figure.get_left_animation_cube(self, x, y, col)
                        self.field[y, x] = col * 2
                        self.score += self.field[y, x]
                        return self.check_field_folding()

    def check_borders(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dy > H - 1 and dx > W:
            self.figure.y -= TILE
            return False
        if self.figure.x > W * TILE or self.figure.x < 0:
            return False
        elif self.figure.y <= 0 or self.field[dy][dx] > 0:
            return False
        return True

    def game_over(self):
        """Проверяет последнюю строку на отсутствие хода."""
        if 0 not in self.field[H - 2] and self.num not in self.field[H - 2]:
            self.set_record()
            return True

    @staticmethod
    def get_record():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self):
        rec = max(int(self.record), self.score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def play(self):
        while True:
            self.get_grid()
            controls.events(self)
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.figure.y -= HALF_TILE
                if not self.check_borders():
                    self.falling_sound.play()
                    self.anim_limit = 2000
                    self.figure.y += HALF_TILE

                    figure.get_animation_cube(self, self.num)
                    dy, dx = self.figure.y // TILE, self.figure.x // TILE

                    self.field[dy][dx] = self.num

                    self.check_field_folding()
                    self.check_figure()
                    self.check_field_left()
                    self.check_field_right()

                    self.num = self.next_num
                    self.next_num = self.new_num()
                    self.figure.y = H * TILE - TILE + 2

                    if self.game_over():
                        break

            figure.draw_item_game(self)
            figure.draw_text_game(self)
            figure.lower_menu(self)
            figure.draw_figure(self, self.game_sc, self.figure, self.num)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Py2048()
    game.play()
