import pygame
import controls
import main


def print_text(self):
    text = self.myfont1.render("Paused", True, pygame.Color("white"))
    self.sc.blit(text, text.get_rect(center=(main.WIDTH // 2, main.TILE // 3)))


def paused_game_menu(self):
    self.transparency = 0
    pygame.draw.rect(self.alpha_sc, (0, 0, 0, 0), (0, 0, main.W * main.TILE, (main.H - 1) * main.TILE + 4))

    while self.paused:
        controls.events(self)
        pygame.display.update()
        print_text(self)
        if self.transparency < 10:
            self.transparency += 1
            self.sc.blit(self.alpha_sc, (5, 50))
            pygame.draw.rect(self.alpha_sc, (0, 0, 0, 10), (0, 0, main.W * main.TILE, (main.H - 1) * main.TILE + 4))
            self.clock.tick(30)
        else:
            self.clock.tick(15)
