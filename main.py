import pygame
from random import randrange
from constants import CP
import controls
import figure

H, W = 10, 5
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = WIDTH, HEIGHT = 640, 960
FPS = 60

class Py2048:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.sc = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)
        self.clock = pygame.time.Clock()

        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
        figure.new_figure(self)
        self.figure = self.figures.copy()
        self.anim_count, self.anim_speed, self.anim_limit = 0, FPS, 2000
        self.score = 0

    def get_animation(self, dy, dx):
        self.field[dy + 1][dx] = self.field[dy][dx] * 2
        self.score += self.field[dy][dx] * 2
        
        self.field[dy][dx] = 0

        pygame.display.flip()

    def get_grid(self):
        [pygame.draw.rect(self.game_sc, (40, 40, 40), i_rect, 1) for i_rect in self.grid]
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * TILE + 2, y * TILE + 2
                    pygame.draw.rect(self.game_sc, CP[col], self.figure_rect, border_radius=4)
                    text_surface = self.myfont.render(f'{col}', True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(self.figure_rect.x + TILE // 2 - 2, self.figure_rect.y + TILE // 2 - 4))
                    self.game_sc.blit(text_surface, text_rect)

    def draw_game(self):
        pygame.draw.rect(self.game_sc, CP[self.num], self.figure, border_radius=4)
        text_surface = self.myfont.render(f'{self.num}', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.figure.x + TILE // 2 - 2, self.figure.y + TILE // 2 - 4))
        self.game_sc.blit(text_surface, text_rect)

    def check_figure(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dy + 1 < H:
            if self.field[dy + 1][dx] == self.field[dy][dx]:
                self.get_animation(dy, dx)
                pygame.time.wait(TILE)
                self.figure.y += TILE
                return self.check_figure()

    def check_borders(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dy > H and dx > W:
            self.figure.y -= TILE
            return False
        if self.figure.x > W * TILE or self.figure.x < 0:
            return False
        elif self.figure.y > H * TILE or self.field[dy][dx] > 0:
            return False
        return True

    def get_speed(self):
        pass

    def game_over(self):
        dx = int(self.figure.x / TILE)
        if self.field[0][dx] > 0:
            self.set_record()
            self.score = 0
            return True

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self):
        rec = max(int(self.record), self.score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def play(self):
        self.down = False
        while True:
            self.record = self.get_record()
            self.sc.blit(self.bg, (0, 0))
            self.sc.blit(self.game_sc, (5, 5))
            self.game_sc.blit(self.game_bg, (0, 0))

            controls.events(self)

            self.anim_count += self.anim_speed
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.figure.y += TILE
                if not self.check_borders():
                    self.figure.y -= TILE
                    dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
                    self.field[dy][dx] = self.num

                    self.check_figure()
                    pygame.time.wait(0)

                    if self.game_over():
                        break

                    self.num = self.new_num()
                    self.figure.x, self.figure.y = TILE * randrange(W) + 2, 2

            self.get_grid()
            self.draw_game()

            self.sc.blit(self.title_score, (505, 780))
            self.sc.blit(self.myfont.render(f"{self.score}", True, pygame.Color("white")), (505, 840))
            self.sc.blit(self.title_record, (505, 650))
            self.sc.blit(self.myfont.render(f"{self.record}", True, pygame.Color('gold')), (505, 710))

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Py2048()
    game.play()