import pygame
import sys
import main


def events(self):
    self.dx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.set_record()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.figure.x = 2
            dx, y = event.pos
            dx = (dx - 5) // main.TILE
            self.figure.x += self.width_dict[dx]
            print(self.dx)
            if self.field[main.H -2][int(self.figure.x / main.TILE)] in (0, self.num):
                self.anim_limit = -1

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                self.dx = main.TILE
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.dx = -main.TILE
            if event.key in (pygame.K_w, pygame.K_UP):
                if self.field[main.H -2][int(self.figure.x / main.TILE)] in (0, self.num):
                    self.anim_limit = -1
            if event.key == pygame.K_ESCAPE:
                self.set_record()
                self.flag = True
                sys.exit()

    self.figure_old = self.figure.copy()
    self.figure.x += self.dx
    if not self.check_borders():
        self.figure = self.figure_old
