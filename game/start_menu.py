import pygame
from settings import HALF_TILE, TILE, WHITE, H, W


def start_animation(self) -> None:
    y, x = 0, (W // 2) * TILE + 2
    jump_force = 20
    move = jump_force + 1
    stop = H * TILE
    flag = True

    for _ in range(120):
        start_figure = pygame.Rect(x, y, TILE - 4, TILE - 4)
        self.alpha_sc.fill((5, 0, 25, 150))
        self.sc.blit(self.alpha_sc, (0, 0))

        text_surface = self.myfont_two.render("2048", True, WHITE)
        pygame.draw.rect(self.sc, (255, 196, 18), start_figure, border_radius=4)
        text_rect = text_surface.get_rect(
            center=(start_figure.x + HALF_TILE - 2, start_figure.y + HALF_TILE - 4)
        )
        self.sc.blit(text_surface, text_rect)

        if stop == y:
            move = -jump_force
            flag = False
        if y + move < stop:
            y += move
            if move < jump_force:
                move += 1
        else:
            self.falling_sound.play()
            if flag:
                y = stop
                move = jump_force + 1
            else:
                y = stop
                jump_force = jump_force // 2
                move = jump_force + 1

        pygame.display.update()
        self.clock.tick(120)
