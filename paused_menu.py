import pygame

import controls
import figure
from settings import HALF_TILE, HEIGHT, MY_FONT_PAUSED, TILE, WHITE, WIDTH


def print_text(self):
    myfont = pygame.font.SysFont(MY_FONT_PAUSED, HALF_TILE - TILE // 6)
    text = myfont.render("Нажмите, чтобы начать", True, WHITE)
    self.paused_text = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    self.sc.blit(text, (WIDTH // 7, self.paused_figure))


def paused_game_menu(self):
    figure.draw_text_game(self)
    figure.lower_menu(self)

    ground = HEIGHT // 3
    jump_force = 5
    move = jump_force + 1
    self.paused_figure = ground

    for _ in range(10):
        self.alpha_sc.fill((0, 0, 15, 15))
        self.sc.blit(self.alpha_sc, (0, 0))
        pygame.display.update()
        self.clock.tick(24)

    while self.paused:
        controls.events(self)
        self.get_grid()
        figure.draw_item_game(self)
        figure.draw_text_game(self)
        figure.lower_menu(self)
        figure.draw_figure(self, self.game_sc, self.figure, self.num)
        self.alpha_sc.fill((0, 0, 15, 150))
        self.sc.blit(self.alpha_sc, (0, 0))

        if True and ground == self.paused_figure:
            move = -jump_force
        if move <= jump_force:
            if self.paused_figure + move < ground:
                self.paused_figure += move
                if move < jump_force:
                    move += 1
            else:
                self.paused_figure = ground
                move = jump_force + 1

        print_text(self)
        pygame.display.update()
        self.clock.tick(17)
