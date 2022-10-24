import pygame

from settings import (BLACK, BORDER_X, BORDER_Y, CP, FPS, GOLD, HALF_TILE,
                      TILE, TRAFFIC_BLACK, WHITE, WIDTH, H, W)


def __figure(num_one, num_two, num_three):
    return pygame.Rect(
        W * HALF_TILE - HALF_TILE + num_one,
        H * TILE - TILE // 4 + num_two,
        num_three,
        num_three
    )


def draw_figure(
        self, sc, figure, num, myfont_one=None, myfont_two=None,
        x=HALF_TILE - 2, y=HALF_TILE - 4
):
    if not myfont_one:
        myfont_one, myfont_two = self.myfont_one, self.myfont_two

    pygame.draw.rect(sc, CP[num], figure, border_radius=4)
    col = WHITE if 1024 > num < 256 else BLACK
    if num < 1000:
        text_surface = myfont_one.render(f'{num}', True, col)
    else:
        text_surface = myfont_two.render(f'{num}', True, col)
    self.text_rect = text_surface.get_rect(center=(
        figure.x + x, figure.y + y))
    sc.blit(text_surface, self.text_rect)


def lower_menu(self):
    """Отображает нижнее меню (номер, следующий номер, кнопку паузы)."""
    figure = __figure(7, 8, TILE - 4)
    draw_figure(self, self.sc, figure, self.num)

    figure = __figure(TILE * 1.3, 18, HALF_TILE + 4)
    draw_figure(
        self, self.sc, figure, self.next_num,
        self.myfont_three, self.myfont_four,
        TILE // 4 + 2, TILE // 4)

    figure = __figure(TILE * 2.25, 18, HALF_TILE + 4)
    pygame.draw.rect(self.sc, TRAFFIC_BLACK, figure, border_radius=4)
    [pygame.draw.rect(
        self.sc, WHITE,
        (
            figure.x + TILE // 7 + i * TILE // 5,
            figure.y + TILE // 8,
            TILE // 11,
            TILE * 0.3
        ),
        border_radius=4) for i in range(2)]


def draw_item_game(self):
    """Отображает игровое поле."""
    self.sc.fill(BLACK)
    self.sc.blit(self.game_sc, (BORDER_X[0], BORDER_Y[0]))
    self.game_sc.blit(self.game_bg, (0, 0))

    [pygame.draw.rect(
        self.game_sc, BLACK,
        (i * TILE - 2, 0, 4, H * TILE + 2))
        for i in range(W) if i != 0]


def draw_text_game(self):
    """Отображает верхнее меню (текущий счет, рекорд)."""
    text = self.myfont_one.render(f"{self.score}", True, WHITE)
    self.sc.blit(text, text.get_rect(center=(WIDTH // 2, TILE // 3)))
    text = self.myfont_three.render(f"{self.record}", True, GOLD)
    self.sc.blit(text, text.get_rect(center=(WIDTH - TILE, TILE // 4)))


def cube_animation_repeat(
        self, game_sc, figure, figure_2=None, figure_3=None, col=None):
    draw_item_game(self)
    draw_figure(self, game_sc, figure, col)
    print(figure_2)
    if figure_2:
        draw_figure(self, game_sc, figure_2, col)
    if figure_3:
        draw_figure(self, game_sc, figure_3, col)

    self.get_grid()
    draw_text_game(self)
    lower_menu(self)

    pygame.display.update()
    self.clock.tick(FPS)


def get_folding_animation_cube(self, x, y, col):
    self.figure.x, self.figure.y = x * TILE + 2, (y - 1) * TILE + 2
    self.figure_2.x, self.figure_2.y = (x + 1) * TILE + 2, y * TILE + 2
    self.figure_3.x, self.figure_3.y = (x - 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.y += 8
        self.figure_2.x -= 8
        self.figure_3.x += 8
        cube_animation_repeat(
            self, self.game_sc, self.figure, self.figure_2, self.figure_3, col
        )


def get_up_animation_cube(self, x, y, col):
    self.figure.x, self.figure.y = x * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.y += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_down_animation_cube(self, x, y, col):
    self.figure.x, self.figure.y = x * TILE + 2, (y + 1) * TILE + 2
    self.falling_sound.play()

    for _ in range(TILE // 10):
        self.figure.y -= 10
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_left_animation_cube(self, x, y, col):
    self.figure.x, self.figure.y = (x + 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.x -= 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_right_animation_cube(self, x, y, col):
    self.figure.x, self.figure.y = (x - 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.x += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_animation_cube(self, col):
    a, b = TILE + 1.4, TILE - 1
    source = self.figure.x
    self.figure.x -= 1
    for _ in range(7):
        a += 1.4
        b -= 1
        self.figure.x -= 1
        figure = pygame.Rect(self.figure.x, self.figure.y, a, b)
        cube_animation_repeat(self, self.game_sc, figure, col=col)
    a -= 3
    b += 1
    self.figure.x += 1
    for _ in range(2):
        a -= 5
        b += 2
        self.figure.x += 3
        figure = pygame.Rect(self.figure.x, self.figure.y, a, b)
        cube_animation_repeat(self, self.game_sc, figure, col=col)
    self.figure.x = source
