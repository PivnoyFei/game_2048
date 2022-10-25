from random import randrange

import pygame

from settings import (BLACK, BORDER_X, BORDER_Y, CP, FPS, GOLD, HALF_TILE,
                      HEIGHT, TILE, TRAFFIC_BLACK, WHITE, WIDTH, H, W)


def __figure(num_one, num_two, num_three):
    """Рисует геометрию кубик на поле."""
    return pygame.Rect(
        W * HALF_TILE - HALF_TILE + num_one,
        H * TILE - TILE // 4 + num_two,
        num_three,
        num_three
    )


def draw_figure(
        self, sc, figure, num, myfont=False,
        x=HALF_TILE - 2, y=HALF_TILE - 4
):
    """Отображает конкретную фигуру с номером, на поле."""
    if myfont:
        myfont_one, myfont_two = self.myfont_three, self.myfont_four
    else:
        myfont_one, myfont_two = self.myfont_one, self.myfont_two

    col = WHITE if 1024 > num < 256 else BLACK
    if 1000 > num:
        myfont = myfont_one
    elif 1000 < num < 10000:
        myfont = myfont_two
    elif 10000 < num < 1000000:
        myfont = self.myfont_three
    elif 1000000 < num < 10000000:
        myfont = self.myfont_four
    else:
        myfont = self.mini_myfont
    if num not in CP:
        CP[num] = (237, 207, 114)

    text_surface = myfont.render(f'{num}', True, col)

    pygame.draw.rect(sc, CP[num], figure, border_radius=4)

    self.text_rect = text_surface.get_rect(center=(
        figure.x + x, figure.y + y))
    sc.blit(text_surface, self.text_rect)


def lower_menu(self):
    """Отображает нижнее меню (номер, следующий номер, кнопку паузы)."""
    figure = __figure(7, 8, TILE - 4)
    draw_figure(self, self.sc, figure, self.num)

    figure = __figure(TILE * 1.3, 18, HALF_TILE + 4)
    draw_figure(
        self, self.sc, figure, self.next_num, True,
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

    """Обрабатываем каждую звезду в списке."""
    for star in self.star_list:
        pygame.draw.circle(self.sc, WHITE, star[0: 2], 2)
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[0] = randrange(WIDTH)
            star[1] = randrange(-50, -10)

    self.sc.blit(self.game_sc, (BORDER_X[0], BORDER_Y[0]))
    self.game_sc.blit(self.game_bg, (0, 0))

    """Рисует разделительные полосы."""
    [pygame.draw.rect(
        self.game_sc, BLACK,
        (i * TILE - 2, 0, 4, H * TILE))
        for i in range(W + 1)]

    if self.num not in CP:
        CP[self.num] = (237, 207, 114)
    pygame.draw.rect(
        self.game_sc, (*CP[self.num], 70),
        (self.x_line, 0, TILE - 4, H * TILE)
    )


def draw_text_game(self):
    """Отображает верхнее меню (текущий счет, рекорд)."""
    text = self.myfont_one.render(f"{self.score}", True, WHITE)
    self.sc.blit(text, text.get_rect(center=(WIDTH // 2, TILE // 3)))
    text = self.myfont_three.render(f"{self.record}", True, GOLD)
    self.sc.blit(text, text.get_rect(center=(WIDTH - TILE, TILE // 4)))


def cube_animation_repeat(
        self, game_sc, figure, figure_2=None, figure_3=None, col=None):
    """Рисует поступающие кадры движения конкретного кубика(-ов)."""
    draw_item_game(self)
    draw_figure(self, game_sc, figure, col)
    if figure_2:
        draw_figure(self, game_sc, figure_2, col)
    if figure_3:
        draw_figure(self, game_sc, figure_3, col)

    self.get_grid()
    draw_text_game(self)
    lower_menu(self)

    pygame.display.update()
    self.clock.tick(FPS)


def get_right_left_animation_cube(self, x, y, col):
    """Анимация слияния трех соседних кубиков."""
    self.figure.x, self.figure.y = (x - 1) * TILE + 2, y * TILE + 2
    self.figure_2.x, self.figure_2.y = (x + 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.x += 8
        self.figure_2.x -= 8
        cube_animation_repeat(
            self, self.game_sc, self.figure, self.figure_2, col=col
        )


def get_folding_animation_cube(self, x, y, col):
    """Анимация слияния четырех соседних кубиков."""
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
    """Анимация поглощения верхнего кубика нижним."""
    self.figure.x, self.figure.y = x * TILE + 2, (y - 1) * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.y += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_down_animation_cube(self, x, y, col):
    """Анимация падения кубика пустую клетку."""
    self.figure.x, self.figure.y = x * TILE + 2, y * TILE + 2
    self.falling_sound.play()

    for _ in range(TILE // 10):
        self.figure.y -= 10
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_left_animation_cube(self, x, y, col):
    """Анимация поглощения правого кубика левым (сдвиг в левую сторону)."""
    self.figure.x, self.figure.y = (x + 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.x -= 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_right_animation_cube(self, x, y, col):
    """Анимация поглощения левого кубика правым (сдвиг в правую сторону)."""
    self.figure.x, self.figure.y = (x - 1) * TILE + 2, y * TILE + 2
    self.merge_sound.play()

    for _ in range(TILE // 8):
        self.figure.x += 8
        cube_animation_repeat(self, self.game_sc, self.figure, col=col)


def get_animation_cube(self, col):
    """Анимация падения кубика после нажатия кнопки."""
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
