import pygame

import controls
import figure
import main


def print_text(self):
    text = self.myfont1.render("Paused", True, pygame.Color("white"))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH // 2, main.HEIGHT // 3)))


def paused_game_menu(self):
    self.transparency = 0
    pygame.draw.rect(self.alpha_sc, (0, 0, 0, 0), (0, 0, main.WIDTH, main.HEIGHT))
    figure.draw_text_game(self)
    figure.get_num(self)
    figure.get_next_num(self)

    while self.paused:
        controls.events(self)
        pygame.display.flip()
        print_text(self)
        if self.transparency < 10:
            self.transparency += 1
            self.alpha_sc.fill((0, 0, 5, 15))
            self.sc.blit(self.alpha_sc, (0, 0))
            self.clock.tick(30)
        else:
            self.clock.tick(15)
