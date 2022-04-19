import pygame
from random import choice, randrange
import main


def new_figure(self):
    self.x, self.y = main.TILE * randrange(main.W) + 2, 2
    self.figures = pygame.Rect(self.x, self.y, main.TILE - 4, main.TILE - 4)

    self.new_num = lambda: choice([2, 4, 8])
    self.num = self.new_num()

    self.figure_rect = pygame.Rect(2, 2, main.TILE - 4, main.TILE - 4)
    self.field = [[0 for i in range(main.W)] for j in range(main.H)]

    self.bg = pygame.image.load('img/fons2.jpg').convert()
    self.game_bg = pygame.image.load('img/fon2.jpg').convert()

    self.title_score = self.myfont.render('Счет:', True, pygame.Color('white'))
    self.title_record = self.myfont.render('Рекорд:', True, pygame.Color('gold'))
