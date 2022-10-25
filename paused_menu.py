import pygame

import controls
import figure
from settings import HALF_TILE, HEIGHT, MY_FONT_PAUSED, WHITE, WIDTH


def print_text(self):
    """Рисует поступающие кадры прыгающего текста."""
    myfont = pygame.font.SysFont(MY_FONT_PAUSED, int(HALF_TILE * 0.8))
    text = myfont.render("Нажмите, чтобы начать", True, WHITE)
    text_center = text.get_rect(center=(WIDTH // 2, self.paused_figure))
    self.sc.blit(text, text_center)


def paused_game_menu(self):
    """Рисует меню паузы."""
    ground = HEIGHT // 3
    jump_force = 5
    move = jump_force + 1
    self.paused_figure = ground

    """Анимация затухания экрана с прозрачностью."""
    for _ in range(10):
        self.alpha_sc.fill((0, 0, 25, 15))
        self.sc.blit(self.alpha_sc, (0, 0))
        pygame.display.update()
        self.clock.tick(40)

    while self.paused:
        """Цикл паузы."""
        controls.events(self)
        self.get_grid()
        figure.draw_item_game(self)
        figure.draw_text_game(self)
        figure.lower_menu(self)
        figure.draw_figure(self, self.game_sc, self.figure, self.num)
        self.alpha_sc.fill((0, 0, 25, 150))
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
