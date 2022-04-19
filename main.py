import pygame
from random import randrange
import controls
import figure

W, H = 5, 7
TILE = 80
GAME_RES = W * TILE, H * TILE
RES = WIDTH, HEIGHT = W * TILE + 10, H * TILE + 200
FPS = 60

class Py2048:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self.titlefont = pygame.font.SysFont('Comic Sans MS', 25)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        self.sc = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)
        self.game_sc = self.game_sc.convert_alpha()
        self.alpha_sc = pygame.Surface((TILE, H * TILE))
        self.clock = pygame.time.Clock()

        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
        figure.new_figure(self)

        self.particles = []

        self.figure = self.figures.copy()
        self.anim_count, self.anim_speed, self.anim_limit = 0, FPS, 2000
        self.score = 0

    def get_grid(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * TILE + 2, y * TILE + 2
                    figure.draw_figure(self, self.figure_rect, col)

    def check_figure(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        self.check_field_y()
        figure.draw_game(self)
        if dy + 1 < H:
            if self.field[dy + 1][dx] == self.field[dy][dx]:
                self.field[dy][dx] *= 2
                self.field[dy + 1][dx] = 0
                figure.up_animation(self)
                self.field[dy + 1][dx] = self.field[dy][dx]
                self.field[dy][dx] = 0
                figure.down_animation(self)
                self.score += self.field[dy + 1][dx]
                return self.check_figure()
        if dx + 1 < W:
            if self.field[dy][dx + 1] == self.field[dy][dx]:
                self.field[dy][dx] *= 2
                self.field[dy][dx + 1] = 0
                figure.right_animation(self)
                self.score += self.field[dy][dx]
                return self.check_figure()
        if dx - 1 >= 0:
            if self.field[dy][dx - 1] == self.field[dy][dx]:
                self.field[dy][dx] *= 2
                self.field[dy][dx - 1] = 0
                figure.left_animation(self)
                self.score += self.field[dy][dx]
                return self.check_figure()

    def check_field_y(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if y != 0:
                    if self.field[y - 1][x] != 0 and col == 0:
                        self.field[y][x] = self.field[y - 1][x]
                        self.field[y - 1][x] = 0
                        return self.check_field_y()

    def check_field_x(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if x != 0:
                    if self.field[y][x - 1] == self.field[y][x] and col != 0:
                        self.field[y][x] = self.field[y][x - 1] * 2
                        self.field[y][x - 1] = 0
                        return self.check_field_x()

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

    def update_particles(self):
        for i, particle in reversed(list(enumerate(self.particles))):
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.2
            reversed_particle = self.particles[len(self.particles) - i - 1]

            pygame.draw.circle(
                self.game_sc, (255, 255, 255),
                (int(reversed_particle[0][0]),
                int(reversed_particle[0][1])),
                reversed_particle[2]
            )
            if particle[2] <= 0:
                self.particles.pop(i)

    def add_particles(self):
        pos_x = 0
        pos_y = 10
        padius = 5
        self.particles.append([[self.x, self.y], [pos_x, pos_y], padius])

    def game_over(self):
        for i in self.field[0]:
            if i != 0:
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
        self.down, self.flag = False, False
        while True:
            controls.events(self)

            self.anim_count += self.anim_speed
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.figure.y += 20
                if not self.check_borders():
                    self.anim_limit = 2000
                    self.flag = False
                    self.figure.y -= TILE
                    dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
                    self.field[dy][dx] = self.num
                    self.check_figure()
                    self.check_field_x()

                    if self.game_over():
                        break

                    self.next_num = self.new_num()
                    self.num = self.next_num
                    self.figure.x, self.figure.y = TILE * randrange(W) + 2, 2

            self.get_grid()
            figure.draw_game(self)
            figure.next_num(self, self.next_num)
            # self.add_particles()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Py2048()
    game.play()