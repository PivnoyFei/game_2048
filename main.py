import pygame
import controls
import figure


W, H = 5, 8
TILE = 80
GAME_RES = W * TILE, (H - 1) * TILE + 4
RES = WIDTH, HEIGHT = W * TILE + 10, H * TILE + 105
FPS = 120


class Py2048:
    def __init__(self):
        self.width_dict = {}
        for i in range(W):
            self.width_dict[i] = i * TILE
        pygame.init()
        pygame.display.set_caption("2048")
        self.myfont1 = pygame.font.SysFont('Comic Sans MS', TILE // 2 - 10)
        self.myfont2 = pygame.font.SysFont('Comic Sans MS', TILE // 2 - 15)
        self.myfont3 = pygame.font.SysFont('Comic Sans MS', TILE // 2 - 25)
        self.myfont4 = pygame.font.SysFont('Comic Sans MS', TILE // 2 - 30)
        self.mini_myfont = pygame.font.SysFont('Comic Sans MS', TILE // 2 - 35)

        self.sc = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)

        self.game_sc = self.game_sc.convert_alpha()
        self.alpha_sc = pygame.Surface(GAME_RES)
        self.alpha_sc = self.alpha_sc.convert_alpha()

        self.clock = pygame.time.Clock()

        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
        self.field = [[0 for i in range(W)] for j in range(H)]
        figure.new_figure(self)

        self.game_bg = pygame.image.load('img/fon.png').convert()

        self.figure, self.figure_2, self.figure_3 = self.figures.copy(), self.figures.copy(), self.figures.copy()
        self.anim_count, self.anim_speed, self.anim_limit = 0, FPS, 2000
        self.paused = False
        self.score = 0

    def get_grid(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * TILE + 2, y * TILE + 2
                    figure.draw_figure(self, self.game_sc, self.figure_rect, col)

    def check_figure(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dx + 1 < W:
            if self.field[dy][dx + 1] == self.field[dy][dx]:
                self.check_field_left()
        if dx - 1 >= 0:
            if self.field[dy][dx - 1] == self.field[dy][dx]:
                self.check_field_right()

    def check_field_folding(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if y != 0 and y != H - 1 and x != 0 and x != W - 1:
                    center_x = self.field[y][x]
                    if center_x != 0:
                        if center_x == self.field[y - 1][x] and center_x == self.field[y][x - 1] and center_x == self.field[y][x + 1]:
                            self.field[y - 1][x], self.field[y][x - 1], self.field[y][x + 1] = 0, 0, 0
                            figure.get_folding_animation_cube(self, y, x, center_x)
                            self.field[y][x] = 0
                            figure.get_down_animation_cube(self, y, x, center_x)
                            self.field[y - 1][x] = center_x * 4
                            self.score += center_x * 4
                            return self.check_field_folding()

    def check_field_y(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if y != H - 1:
                    if self.field[y + 1][x] != 0 and self.field[y + 1][x] == self.field[y][x]:
                        self.field[y][x] = 0
                        figure.get_up_animation_cube(self, y, x, col)
                        self.field[y + 1][x] = 0
                        self.field[y][x] = col * 2
                        figure.get_down_animation_cube(self, y, x, col * 2)
                        self.score += self.field[y][x]
                        return self.check_field_y()
                    if self.field[y + 1][x] != 0 and col == 0:
                        colr = self.field[y + 1][x]
                        self.field[y][x] = self.field[y + 1][x]
                        self.field[y + 1][x] = 0
                        figure.get_down_animation_cube(self, y, x, colr)
                        self.field[y][x] = colr
                        return self.check_field_y()

    def check_field_right(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if x != 0:
                    if self.field[y][x - 1] == self.field[y][x] and col != 0:
                        self.field[y][x - 1] = 0
                        figure.get_right_animation_cube(self, y, x, col)
                        self.field[y][x] = col * 2
                        self.score += self.field[y][x]
                        return self.check_field_y()

    def check_field_left(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if x != W - 1:
                    if self.field[y][x + 1] == self.field[y][x] and col != 0:
                        self.field[y][x + 1] = 0
                        figure.get_left_animation_cube(self, y, x, col)
                        self.field[y][x] = col * 2
                        self.score += self.field[y][x]
                        return self.check_field_y()

    def check_borders(self):
        dy, dx = int(self.figure.y / TILE), int(self.figure.x / TILE)
        if dy > H - 1 and dx > W:
            self.figure.y -= TILE
            return False
        if self.figure.x > W * TILE or self.figure.x < 0:
            return False
        elif self.figure.y <= 0 or self.field[dy][dx] > 0:
            return False
        return True

    def game_over(self):
        if 0 not in self.field[H - 2] and self.num not in self.field[H - 2]:
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
        while True:
            figure.draw_item_game(self)
            controls.events(self)
            if self.anim_count > self.anim_limit:
                figure.strip_game(self)
            figure.draw_figure(self, self.game_sc, self.figure, self.num)

            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.figure.y -= 40
                if not self.check_borders():
                    self.anim_limit = 2000
                    self.figure.y += 40

                    figure.get_animation_cube(self, self.num)
                    dy, dx = self.figure.y // TILE, self.figure.x // TILE
                    
                    self.field[dy][dx] = self.num
                    for _ in range(2):
                        self.check_field_folding()
                        self.check_field_y()
                        self.check_figure()
                    self.check_field_left()
                    self.check_field_right()

                    if self.game_over():
                        break

                    self.num = self.next_num
                    self.next_num = self.new_num()
                    self.figure.y = H * TILE - TILE + 2

            self.get_grid()
            figure.draw_text_game(self)
            figure.get_num(self)
            figure.get_next_num(self)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Py2048()
    game.play()