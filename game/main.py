from random import choice, randint, randrange
from typing import Any

import controls
import figure
import numpy as np
import pygame
import start_menu
from settings import (FPS, GAME_RES, HALF_TILE, HEIGHT, MY_FONT, RES, TILE,
                      WIDTH, H, W)


class Py2048:
    def __init__(self) -> None:
        self.width_dict = {i: i * TILE for i in range(W)}
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.falling_sound = pygame.mixer.Sound('madia/falling_sound.mp3')
        self.merge_sound = pygame.mixer.Sound('madia/merge_sound.mp3')
        pygame.display.set_caption("2048")
        pygame.display.set_icon(pygame.image.load("madia/two.png"))
        self.myfont_one = pygame.font.SysFont(MY_FONT, int(HALF_TILE * 0.8))
        self.myfont_two = pygame.font.SysFont(MY_FONT, int(HALF_TILE * 0.6))
        self.myfont_three = pygame.font.SysFont(MY_FONT, int(HALF_TILE * 0.5))
        self.myfont_four = pygame.font.SysFont(MY_FONT, int(HALF_TILE * 0.4))
        self.mini_myfont = pygame.font.SysFont(MY_FONT, int(HALF_TILE * 0.3))

        self.sc = pygame.display.set_mode(RES, pygame.DOUBLEBUF)
        self.sprite_sc = pygame.Surface(RES).convert_alpha()
        self.game_sc = pygame.Surface(GAME_RES).convert_alpha()
        self.alpha_sc = pygame.Surface(RES).convert_alpha()
        self.game_bg = pygame.image.load('madia/gradient.png').convert()

        """Пустая матрица игрового поля."""
        self.field = np.array([[0 for _ in range(W)] for _ in range(H)])

        """Начальные координаты фигуры."""
        self.x = (W // 2) * TILE + 2
        self.y = H * TILE - TILE + 2
        self.figures = pygame.Rect(self.x, self.y, TILE - 4, TILE - 4)
        self.x_line = self.x
        self.save_figure = self.x
        self.changes_one, self.changes_two = True, True

        self.figure = self.figures.copy()
        self.figure_2 = self.figures.copy()
        self.figure_3 = self.figures.copy()

        self.figure_rect = pygame.Rect(
            W * TILE - TILE + 2,
            H * TILE - TILE + 2,
            TILE - 4,
            TILE - 4)

        """Номер настоящей и будущей фигуры."""
        self.new_num = lambda: choice([2, 4, 8, 16, 32, 64])
        self.next_num = self.new_num()
        self.num = self.next_num
        self.record = self.get_record()
        self.score = 0

        self.anim_count, self.anim_speed, self.anim_limit = 0, FPS, 2000

        self.star_list = [[
            randrange(WIDTH), randrange(HEIGHT), randint(1, 3)
        ] for _ in range(50)]

        self.clock = pygame.time.Clock()
        self.paused = False

    def get_grid(self) -> None:
        """Отображает фигуры расположенные на поле."""
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x = x * TILE + 2
                    self.figure_rect.y = y * TILE + 2
                    figure.draw_figure(
                        self, self.game_sc, self.figure_rect, col)

    def _connection_three_figures(self, y: int, x: int, col: int) -> Any:
        """Проверка и слияние трех соседних фигур."""
        if self.field[y, x - 1] == col and self.field[y, x + 1] == col:
            self.field[y, x - 1] = 0
            self.field[y, x + 1] = 0
            figure.get_right_left_animation_cube(self, x, y, col)
            self.field[y, x] = col * 2
            self.score += col * 2
            return self.check_field_folding()

    def _connection_four_figures(self, y: int, x: int, col: int) -> Any:
        """Проверка и слияние четырех соседних фигур."""
        figure_right = self.field[y, x + 1]
        figure_left = self.field[y, x - 1]
        figure_up = self.field[y - 1, x]

        if col == figure_up and col == figure_left and col == figure_right:
            figure_up, figure_left, figure_right = 0, 0, 0
            figure.get_folding_animation_cube(self, x, y, col)
            self.field[y, x] = 0
            figure.get_down_animation_cube(self, x, y, col)
            figure_up = col * 4
            self.score += col * 4
            return self.check_field_folding()

    def check_field_folding(self) -> Any:
        for y in range(H):
            for x in range(W):
                if col := self.field[y, x]:

                    if y and 0 < x < W - 1:
                        self._connection_four_figures(y, x, col)

                    if 0 < x < W - 1:
                        self._connection_three_figures(y, x, col)

                    """Слияние верхней и нижней фигуры."""
                    if y and self.field[y - 1, x] == col:
                        self.field[y - 1, x] = 0
                        figure.get_up_animation_cube(self, x, y, col)
                        self.field[y, x] = 0
                        figure.get_down_animation_cube(self, x, y, col * 2)
                        self.field[y - 1, x] = col * 2
                        self.score += col * 2
                        return self.check_field_folding()

                    """Опускает фигуру на пустую клетку."""
                    if y and self.field[y - 1, x] == 0:
                        self.field[y, x] = 0
                        figure.get_down_animation_cube(self, x, y, col)
                        self.field[y - 1, x] = col
                        return self.check_field_folding()

        self.changes_one = False

    def check_field_left_right(self) -> Any:
        for y in range(H):
            for x in range(W - 1):
                if col := self.field[y, x]:
                    if self.field[y, x + 1] == col:
                        if self.save_figure < x + 1:
                            self.field[y, x + 1] = 0
                            figure.get_left_animation_cube(self, x, y, col)
                            self.field[y, x] = col * 2
                        else:
                            self.field[y, x] = 0
                            figure.get_right_animation_cube(self, x + 1, y, col)
                            self.field[y, x + 1] = col * 2

                        self.score += col * 2
                        return self.check_field_folding()

        self.changes_two = False

    def check_borders(self) -> bool:
        """Не дает фигуре выйти за границы"""
        dy, dx = self.figure.y // TILE, self.figure.x // TILE
        if dy > H - 1 and dx > W:
            self.figure.y -= TILE
            return False
        if self.figure.x > W * TILE or self.figure.x < 0:
            return False
        elif self.figure.y <= 0 or self.field[dy][dx] > 0:
            return False
        return True

    def next_nem(self) -> None:
        """Задает новый номер настоящей и будущей фигуры."""
        self.num = self.next_num
        if self.score > 15000:
            self.new_num = lambda: choice([4, 8, 16, 32, 64, 128])
        self.next_num = self.new_num()

    def game_over(self) -> bool:
        """Проверяет последнюю строку на отсутствие хода."""
        if 0 not in self.field[H - 2] and self.num not in self.field[H - 2]:
            self.set_record()
            return True
        return False

    def block_display(self) -> None:
        figure.draw_item_game(self)
        figure.draw_text_game(self)
        figure.lower_menu(self)
        figure.draw_figure(self, self.game_sc, self.figure, self.num)

    @staticmethod
    def get_record() -> int:
        try:
            with open('madia/record.txt') as f:
                return int(f.readline())
        except FileNotFoundError:
            with open('madia/record.txt', 'w') as f:
                f.write('0')
            return 0

    def set_record(self) -> None:
        """Записывает новый рекорд."""
        rec = max(int(self.record), self.score)
        with open('madia/record.txt', 'w') as f:
            f.write(str(rec))

    def play(self) -> None:
        """Основной цикл игры."""
        start_menu.start_animation(self)
        for i in range(0, 250, 20):
            self.block_display()
            self.alpha_sc.fill((0, 0, 25, 255 - i))
            self.sc.blit(self.alpha_sc, (0, 0))
            pygame.display.update()
            self.clock.tick(40)

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
                    self.save_figure = dx

                    self.field[dy][dx] = self.num

                    while self.changes_one or self.changes_two:
                        self.check_field_folding()
                        self.check_field_left_right()

                    self.changes_one, self.changes_two = True, True

                    self.next_nem()
                    self.figure.y = H * TILE - TILE + 2

                    if self.game_over():
                        break

            self.block_display()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Py2048()
    game.play()
