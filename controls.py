import pygame
import sys
import main
import paused_menu


def events(self):
    self.dx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.set_record()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.paused:
                self.figure.x = 2
                self.strip_dx, y = event.pos
                self.strip_dx = (self.strip_dx - 5) // main.TILE
                self.figure.x += self.width_dict[self.strip_dx]
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
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True
                    paused_menu.paused_game_menu(self)
        
    self.figure.x += self.dx
    if not self.check_borders():
        self.figure.x -= self.dx
