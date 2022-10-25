import sys

import pygame

import paused_menu
from settings import BORDER_X, BORDER_Y, PAUSE_X, PAUSE_Y, TILE, H


def events(self):
    """Обрабатывает нажатия с клавиатуры и мыши."""
    self.dx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.set_record()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.paused:
                self.paused = False
            else:
                self.strip_dx, self.strip_dy = event.pos
                """Обработка нажатий по игровому полю."""
                if (BORDER_X[0] < self.strip_dx < BORDER_X[1]
                        and BORDER_Y[0] < self.strip_dy < BORDER_Y[1]):
                    self.figure.x = 2
                    self.strip_dx = (self.strip_dx - 5) // TILE
                    self.figure.x += self.width_dict[self.strip_dx]
                    figure_on_field = self.field[H - 2, self.figure.x // TILE]
                    self.x_line = self.figure.x
                    if figure_on_field in (0, self.num):
                        self.anim_limit = -1
                """Обработка нажатий по кнопке пауза."""
                if (PAUSE_X[0] < self.strip_dx < PAUSE_X[1]
                        and PAUSE_Y[0] < self.strip_dy < PAUSE_Y[1]):
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
