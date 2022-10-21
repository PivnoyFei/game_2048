import pygame

import main
from constants import CP


def draw_figure(self, sc, figure, num):
    pygame.draw.rect(sc, CP[num], figure, border_radius=4)
    if num > 1:
        if 1024 > num < 256:
            col = (255, 255, 255)
        else:
            col = (0, 0, 0)
        if num < 1000:
            text_surface = self.myfont1.render(f'{num}', True, col)
        else:
            text_surface = self.myfont2.render(f'{num}', True, col)
        self.text_rect = text_surface.get_rect(center=(
            figure.x + main.TILE // 2 - 2, figure.y + main.TILE // 2 - 4))
        sc.blit(text_surface, self.text_rect)


def get_num(self):
    figure = pygame.Rect(
        main.W * main.TILE // 2 - main.TILE // 2 + 5,
        main.H * main.TILE + 3,
        main.TILE - 4,
        main.TILE - 4
    )
    draw_figure(self, self.sc, figure, self.num)


def get_next_num(self):
    figure = pygame.Rect(
        main.W * main.TILE // 2 - main.TILE // 2 + 105,
        main.H * main.TILE + 18,
        main.TILE - main.TILE // 2 + 4,
        main.TILE - main.TILE // 2 + 4
    )
    pygame.draw.rect(self.sc, CP[self.next_num], figure, border_radius=4)
    if 1024 > self.next_num < 256:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    if self.next_num < 1000:
        text_surface = self.myfont3.render(f'{self.next_num}', True, col)
    else:
        text_surface = self.myfont4.render(f'{self.next_num}', True, col)
    self.text_rect = text_surface.get_rect(center=(
        figure.x + main.TILE // 4 + 2, figure.y + main.TILE // 4))
    self.sc.blit(text_surface, self.text_rect)


# def strip_game(self):
#     pygame.draw.rect(
#         self.game_sc,
#         (*CP[self.num], 70),
#         (self.figure.x, 0, main.TILE - 4, main.H * main.TILE)
#     )


def draw_item_game(self):
    self.sc.fill((0, 0, 0))
    self.sc.blit(self.game_sc, (5, 50))
    self.game_sc.blit(self.game_bg, (0, 0))

    [pygame.draw.rect(
        self.game_sc, (0, 0, 0),
        (i_rect * main.TILE - 2, 0, 4, main.H * main.TILE + 2))
        for i_rect in range(main.W) if i_rect != 0]


def draw_text_game(self):
    text = self.myfont1.render(f"{self.score}", True, pygame.Color("white"))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH // 2, main.TILE // 3)))
    text = self.myfont3.render(f"{self.record}", True, pygame.Color('gold'))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH - main.TILE, main.TILE // 4)))


def cube_animation_repeat(self, game_sc, figure, figure_2=None, figure_3=None, col=None):
    draw_item_game(self)
    draw_figure(self, game_sc, figure, col)
    if figure_2:
        draw_figure(self, game_sc, figure_2, col)
    if figure_3:
        draw_figure(self, game_sc, figure_3, col)

    self.get_grid()
    draw_text_game(self)
    get_num(self)
    get_next_num(self)
    pygame.display.update()
    self.clock.tick(main.FPS)


def get_folding_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, (y - 1) * main.TILE + 2
    self.figure_2.x, self.figure_2.y = (x + 1) * main.TILE + 2, y * main.TILE + 2
    self.figure_3.x, self.figure_3.y = (x - 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.y += 8
        self.figure_2.x -= 8
        self.figure_3.x += 8
        cube_animation_repeat(self, self.game_sc, self.figure, self.figure_2, self.figure_3, col)


def get_up_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.y += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_down_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, (y + 1) * main.TILE + 2
    for _ in range(main.TILE // 10):
        self.figure.y -= 10
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)
    get_animation_cube(self, col)


def get_left_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = (x + 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.x -= 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_right_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = (x - 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.x += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_animation_cube(self, col):
    a, b = main.TILE + 1.4, main.TILE - 1
    source = self.figure.x
    self.figure.x -= 1
    for _ in range(7):
        a += 1.4
        b -= 1
        self.figure.x -= 1
        figure = pygame.Rect(self.figure.x, self.figure.y, a, b)
        cube_animation_repeat(self, self.game_sc, figure, col=col)
    a -= 3
    b += 1
    self.figure.x += 1
    for _ in range(2):
        a -= 5
        b += 2
        self.figure.x += 3
        figure = pygame.Rect(self.figure.x, self.figure.y, a, b)
        cube_animation_repeat(self, self.game_sc, figure, col=col)
    self.figure.x = source
