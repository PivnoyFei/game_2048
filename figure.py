import pygame
from random import choice, randrange
import main
from constants import CP


def new_figure(self):
    self.x = (main.W // 2) * main.TILE + 2
    self.y = main.H * main.TILE - main.TILE + 2
    self.figures = pygame.Rect(self.x, self.y, main.TILE - 4, main.TILE - 4)

    self.new_num = lambda: choice([2, 4, 8, 16, 32, 64])
    self.next_num = self.new_num()
    self.num = self.next_num

    self.figure_rect = pygame.Rect(
        main.W * main.TILE - main.TILE + 2,
        main.H * main.TILE - main.TILE + 2,
        main.TILE - 4,
        main.TILE - 4)
    self.field = [[0 for i in range(main.W)] for j in range(main.H)]

    self.game_bg = pygame.image.load('img/fon.png').convert()


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
    num = 1

    figure4 = pygame.Rect(
        main.W * main.TILE // 2 - main.TILE // 2 + 5,
        main.H * main.TILE + 3,
        main.TILE - 4,
        main.TILE - 4
    )
    draw_figure(self, self.sc, figure4, self.num)


def get_next_num(self):
    num = 1

    figure2 = pygame.Rect(
        main.W * main.TILE // 2 - main.TILE // 2 + 105,
        main.H * main.TILE + 18,
        main.TILE - main.TILE // 2 + 4,
        main.TILE - main.TILE // 2 + 4
    )
    pygame.draw.rect(self.sc, CP[self.next_num], figure2, border_radius=4)
    if 1024 > self.next_num < 256:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    if self.next_num < 1000:
        text_surface = self.myfont3.render(f'{self.next_num}', True, col)
    else:
        text_surface = self.myfont4.render(f'{self.next_num}', True, col)
    self.text_rect = text_surface.get_rect(center=(
        figure2.x + main.TILE // 4 + 2, figure2.y + main.TILE // 4))
    self.sc.blit(text_surface, self.text_rect)


def draw_item_game(self):
    self.record = self.get_record()
    self.sc.fill((0, 0, 0))
    self.sc.blit(self.game_sc, (5, 50))
    #self.game_sc.blit(self.A.text_surface, self.A.rest)
    self.game_sc.blit(self.game_bg, (0, 0))

    [pygame.draw.rect(
        self.game_sc, (0, 0, 0),
        (i_rect * main.TILE - 2, 0, 4, main.H * main.TILE + 2))
        for i_rect in range(main.W) if i_rect != 0
    ]
    pygame.draw.rect(
        self.game_sc,
        (*CP[self.num], 70),
        (self.figure.x, 0, main.TILE - 4, main.H * main.TILE)
    )


def draw_game(self):
    text = self.myfont1.render(f"{self.score}", True, pygame.Color("white"))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH // 2, 25)))
    text = self.myfont3.render(f"{self.record}", True, pygame.Color('gold'))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH - main.TILE, 20)))


def cube_animation_repeat(self, game_sc, figure, col):
    draw_item_game(self)
    draw_figure(self, game_sc, figure, col)
    draw_game(self)
    get_num(self)
    get_next_num(self)
    self.get_grid()
    pygame.display.update()
    self.clock.tick(main.FPS)


def get_folding_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, (y - 1) * main.TILE + 2
    self.figure_2.x, self.figure_2.y = (x - 1) * main.TILE + 2, y * main.TILE + 2
    self.figure_3.x, self.figure_2.y = (x + 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.y += 8
        self.figure_2.x += 8
        self.figure_3.x -= 8
        cube_animation_repeat(self, self.game_sc, self.figure, col)
        cube_animation_repeat(self, self.game_sc, self.figure_2, col)
        cube_animation_repeat(self, self.game_sc, self.figure_3, col)


def get_up_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.y += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col)


def get_down_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = x * main.TILE + 2, (y + 1) * main.TILE + 2
    for _ in range(main.TILE // 10):
        self.figure.y -= 10
        cube_animation_repeat(self, self.game_sc, self.figure, col)


def get_left_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = (x + 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.x -= 8
        cube_animation_repeat(self, self.game_sc, self.figure, col)


def get_right_animation_cube(self, y, x, col):
    self.figure.x, self.figure.y = (x - 1) * main.TILE + 2, y * main.TILE + 2
    for _ in range(main.TILE // 8):
        self.figure.x += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col)


def get_animation_cube(self):
    a, b = main.TILE, main.TILE
    for _ in range(8):
        a += 1
        b -= 1
        self.figure.x -= 1
        figure = pygame.Rect(self.figure.x, self.figure.y, a, b)
        cube_animation_repeat(self, self.game_sc, figure, self.num)
    self.figure.x += 8
