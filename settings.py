W, H = 5, 8
TILE = 80
HALF_TILE = TILE // 2
GAME_RES = W * TILE, (H - 1) * TILE + 5
BORDER_X = (5, GAME_RES[0] + 5)
BORDER_Y = (TILE // 2 + 10, GAME_RES[1] + TILE // 2 + 10)
RES = WIDTH, HEIGHT = W * TILE + 10, H * TILE + TILE
FPS = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
TRAFFIC_BLACK = (30, 30, 30)

MY_FONT = 'arialblack'
MY_FONT_PAUSED = 'bahnschrift'

CP = {
    1: (255, 255, 255),
    2: (55, 182, 206),
    4: (255, 152, 56),
    8: (255, 99, 146),
    16: (165, 65, 89),
    32: (144, 48, 53),
    64: (128, 112, 161),
    128: (19, 125, 93),
    256: (96, 217, 146),
    512: (247, 162, 134),
    1024: (189, 244, 0),
    2048: (251, 63, 81),
    4096: (8, 108, 162),
    8192: (255, 180, 89),
    16384: (255, 65, 0)
}
