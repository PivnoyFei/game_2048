import controls
import figure
import pygame
from settings import (HALF_TILE, HEIGHT, MY_FONT_PAUSED, THREE_QUARTERS,
                      TRAFFIC_BLACK, UPDATE_PAUSE_X, UPDATE_PAUSE_Y, WHITE,
                      WIDTH)


def print_paused_text(self) -> None:
    """Рисует поступающие кадры прыгающего текста."""
    myfont = pygame.font.SysFont(MY_FONT_PAUSED, int(HALF_TILE * 0.8))
    text = myfont.render("Нажмите, чтобы начать", True, WHITE)
    text_center = text.get_rect(center=(WIDTH // 2, self.paused_figure))
    self.sc.blit(text, text_center)


def print_paused_figure(self, x: int, filename: str, rotate: int | None = None) -> None:
    """Рисует кнопку перезапуска и закрытия игры."""
    size = HALF_TILE
    figur = pygame.Rect(x, UPDATE_PAUSE_Y, THREE_QUARTERS, THREE_QUARTERS)
    image = pygame.image.load(filename).convert_alpha()
    if rotate:
        image = pygame.transform.rotate(image, 45)
        size = int(HALF_TILE * 1.4)
    image = pygame.transform.scale(image, (size, size))
    new_rect = image.get_rect(
        center=(figur.x + THREE_QUARTERS // 2, figur.y + THREE_QUARTERS // 2))
    pygame.draw.rect(self.sc, TRAFFIC_BLACK, figur, border_radius=4)
    self.sc.blit(image, new_rect)


def paused_game_menu(self) -> None:
    """Рисует меню паузы."""
    ground = HEIGHT // 3
    jump_force = 5
    move = jump_force + 1
    self.paused_figure = ground

    """Анимация затухания экрана с прозрачностью."""
    for _ in range(10):
        self.alpha_sc.fill((5, 0, 25, 15))
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
        self.alpha_sc.fill((5, 0, 25, 150))
        self.sc.blit(self.alpha_sc, (0, 0))

        if ground == self.paused_figure:
            move = -jump_force
        if move <= jump_force:
            if self.paused_figure + move < ground:
                self.paused_figure += move
                if move < jump_force:
                    move += 1
            else:
                self.paused_figure = ground
                move = jump_force + 1

        print_paused_text(self)
        print_paused_figure(
            self, UPDATE_PAUSE_X[0], 'madia/Update.png')
        print_paused_figure(
            self, UPDATE_PAUSE_X[1], 'madia/X.png', 45)
        pygame.display.update()
        self.clock.tick(17)
