import os

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
WIDTH_MAP = 704
HEIGHT_MAP = 416
FPS = 60
ANIMATION = 100
GRAVITY = 0.75
SCROLL_THRESH = 400
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS # Này dùng trong game
TILE_SIZE_MAP = HEIGHT_MAP // ROWS # Này dùng trong map
TILE_TYPES = sum(1 for file in os.listdir('Map/Tile') if file.endswith(".png"))
MAX_LEVELS = 5
MAINBTN_WIDTH = 150
MAINBTN_HEIGHT = 66

PLAYER_WIDTH = 128
PLAYER_HEIGHT = 128

SHOP_WIDTH = 118
SHOP_HEIGHT = 128

GOLEM_WIDTH = 100
GOLEM_HEIGHT = 100

COIN_WIDTH = 16
COIN_HEIGHT = 16

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


