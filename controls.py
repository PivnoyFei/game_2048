import pygame
import sys
import main


def events(self):
    self.dx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.set_record()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.dx = main.TILE
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.dx = -main.TILE
            if event.key in (pygame.K_s, pygame.K_DOWN):
                self.anim_limit = 1
            if event.key == pygame.K_ESCAPE:
                self.set_record()
                self.flag = True
                sys.exit()

    self.figure_old = self.figure.copy()
    self.figure.x += self.dx
    if not self.check_borders():
        self.figure = self.figure_old

    if self.down:
        self.figure.y += main.TILE
        if not self.check_borders():
            self.figure.y -= main.TILE
