import sys

import paused_menu
import pygame
from settings import (BORDER_X, BORDER_Y, PAUSE_X, PAUSE_Y, THREE_QUARTERS,
                      TILE, UPDATE_PAUSE_X, UPDATE_PAUSE_Y, H)


def events(self) -> None:
    """Обрабатывает нажатия с клавиатуры и мыши."""
    self.dx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.set_record()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pos_x, self.pos_y = event.pos

            if self.paused:
                min_x = UPDATE_PAUSE_X[1]
                max_x = UPDATE_PAUSE_X[1] + THREE_QUARTERS
                min_y, max_y = UPDATE_PAUSE_Y, UPDATE_PAUSE_Y + THREE_QUARTERS

                """Закрытие игры."""
                if min_x < self.pos_x < max_x and min_y < self.pos_y < max_y:
                    self.set_record()
                    sys.exit()
                min_x = UPDATE_PAUSE_X[0]
                max_x = UPDATE_PAUSE_X[0] + THREE_QUARTERS

                """Перезапуск игры."""
                if min_x < self.pos_x < max_x and min_y < self.pos_y < max_y:
                    self.set_record()
                    from main import Py2048
                    game = Py2048()
                    game.play()
                else:
                    self.paused = False

            else:
                """Обработка нажатий по игровому полю."""
                if (BORDER_X[0] < self.pos_x < BORDER_X[1]
                        and BORDER_Y[0] < self.pos_y < BORDER_Y[1]):
                    self.figure.x = 2
                    self.pos_x = (self.pos_x - 5) // TILE
                    self.figure.x += self.width_dict[self.pos_x]
                    figure_on_field = self.field[H - 2, self.figure.x // TILE]
                    self.x_line = self.figure.x
                    if figure_on_field in (0, self.num):
                        self.anim_limit = -1
                """Обработка нажатий по кнопке пауза."""
                if (PAUSE_X[0] < self.pos_x < PAUSE_X[1]
                        and PAUSE_Y[0] < self.pos_y < PAUSE_Y[1]):
                    self.paused = True
                    paused_menu.paused_game_menu(self)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.dx = TILE
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.dx = -TILE
            if event.key in (pygame.K_w, pygame.K_UP):
                if self.field[H - 2, self.figure.x // TILE] in (0, self.num):
                    self.anim_limit = -1
            if event.key == pygame.K_ESCAPE:
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True
                    paused_menu.paused_game_menu(self)

    self.x_line += self.dx
    self.figure.x += self.dx
    if not self.check_borders():
        self.figure.x -= self.dx
