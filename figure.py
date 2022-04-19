import pygame
from random import choice, randrange
import main
from constants import CP


def new_figure(self):
    self.x, self.y = main.TILE * randrange(main.W) + 2, 2
    self.figures = pygame.Rect(self.x, self.y, main.TILE - 4, main.TILE - 4)

    self.new_num = lambda: choice([2, 4, 8, 16, 32, 64])
    self.num = self.new_num()
    self.next_num = self.new_num()

    self.figure_rect = pygame.Rect(2, 2, main.TILE - 4, main.TILE - 4)
    self.field = [[0 for i in range(main.W)] for j in range(main.H)]

    self.bg = pygame.image.load('img/fon2.jpg').convert()
    self.game_bg = pygame.image.load('img/fon2.png').convert()


def draw_figure(self, figure, num):
    pygame.draw.rect(self.game_sc, CP[num], figure, border_radius=4)
    if num < 256:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    text_surface = self.myfont.render(f'{num}', True, col)
    self.text_rect = text_surface.get_rect(center=(
        figure.x + main.TILE // 2 - 2, figure.y + main.TILE // 2 - 4))
    self.game_sc.blit(text_surface, self.text_rect)


def next_num(self, num):
    figure = pygame.Rect(
        main.W * main.TILE // 2 - main.TILE // 2 + 5,
        main.H * main.TILE + 70,
        main.TILE - 4,
        main.TILE - 4
    )
    pygame.draw.rect(self.sc, CP[num], figure, border_radius=4)
    if num < 256:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    text_surface = self.myfont.render(f'{num}', True, col)
    self.text_rect = text_surface.get_rect(center=(
        figure.x + main.TILE // 2 - 2, figure.y + main.TILE // 2 - 4))
    self.sc.blit(text_surface, self.text_rect)


def draw_game(self):
    self.record = self.get_record()
    self.sc.fill((0, 0, 0))
    self.sc.blit(self.game_sc, (5, 50))
    self.game_sc.blit(self.game_bg, (0, 0))

    [pygame.draw.rect(
        self.game_sc, (0, 0, 0),
        (i_rect * main.TILE - 2, 0, 4, main.H * main.TILE)) 
        for i_rect in range(main.W) if i_rect != 0
    ]
    pygame.draw.rect(
        self.game_sc,
        (*CP[self.num], 70),
        (self.figure.x, 0, main.TILE - 4, main.H * main.TILE)
    )
    draw_figure(self, self.figure, self.num)

    self.sc.blit(self.titlefont.render(
        f"{self.score}", True, pygame.Color("white")),
        (main.WIDTH // 2 - 10, 8))
    self.sc.blit(self.myfont.render(
        f"{self.record}", True, pygame.Color('gold')),
        (main.WIDTH - main.TILE - 20, 10))


def up_animation(self):
    self.figure.y += main.TILE
    for _ in range(main.TILE // 2):
        self.figure.y -= 2
        draw_game(self)
        self.get_grid()
        pygame.display.flip()
        self.clock.tick(main.FPS * 2)


def down_animation(self):
    for _ in range(main.TILE // 2):
        self.figure.y += 2
        draw_game(self)
        self.get_grid()
        pygame.display.flip()


def left_animation(self):
    self.figure.x -= main.TILE
    for _ in range(main.TILE // 2):
        self.figure.x += 2
        draw_game(self)
        self.get_grid()
        pygame.display.flip()
        self.clock.tick(main.FPS * 2)


def right_animation(self):
    self.figure.x += main.TILE
    for _ in range(main.TILE // 2):
        self.figure.x -= 2
        draw_game(self)
        self.get_grid()
        pygame.display.flip()
        self.clock.tick(main.FPS * 2)
