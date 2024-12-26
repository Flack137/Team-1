import pygame

pygame.init()
pygame.mixer.init()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
#розміри вікна
FPS = 60
#кадрів в сек.
TILE_SIZE = 37
PLAYER_SIZE = int(TILE_SIZE * 0.9)
#розміри об'єктів на мапі

BACKGROUND_COLOR = (0, 0, 0)
# PLAYER_COLOR = (0, 255, 0)
# ENEMY_COLOR = (255, 0, 0)
# BULLET_COLOR = (255, 255, 0)
# WALL_COLOR = (128, 128, 128)
# ICE_COLOR = (173, 216, 230)
#кольори

PLAYER_SPEED = 2
ENEMY_SPEED = 2
BULLET_SPEED = int(PLAYER_SPEED * 5)
#швидкості переміщення об'єктів

tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBB',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....II..............B',
    'B....................B',
    'B....EE..............B',
    'B....BB..............B',
    'B....................B',
    'B....KK..............B',
    'B....LL..............B',
    'B....................B',
    'B....................B',
    'B.........P..........B',
    'B....................B',
    'BBBBBBBBBBBBBBBBBBBBBB',
] #сітка мапи

PLAYER_IMAGES = {
    "up": ["sprites/player_up1.png", "sprites/player_up2.png"],
    "down": ["sprites/player_down1.png", "sprites/player_down2.png"],
    "left": ["sprites/player_l1.png", "sprites/player_l2.png"],
    "right": ["sprites/player_r1.png", "sprites/player_r2.png"]
} #зображення для анімацій гравця

WALL_IMAGE = "sprites/wall.png"
ICE_IMAGE = "sprites/ice.png"
BUSH_IMAGE = "sprites/bushes.png"
IRON_WALL_IMAGE = "sprites/iron_wall.jpg"
#зображення стін та льоду(води), кущів

ENEMY_IMAGES = {
    "up": ["sprites/enemy.png", "sprites/enemy2.png"],
    "down": ["sprites/enemy_down1.png", "sprites/enemy_down2.png"],
    "left": ["sprites/enemy_l1.png", "sprites/enemy_l2.png"],
    "right": ["sprites/enemy_r1.png", "sprites/enemy_r2.png"]
} #зображення для анімацій ворогів

BULLETS_IMAGE = "sprites/bullet.jpg"
BOOM_IMAGES = [
    "sprites/boom1.png",
    "sprites/boom2.png",
    "sprites/boom3.png"
]

pygame.mixer.music.load("sounds/vietnam.mp3")
BOOM_SOUND = pygame.mixer.Sound("sounds/boom.wav")
ENGINE_SOUND = pygame.mixer.Sound("sounds/engine.wav")
SHOOT_SOUND = pygame.mixer.Sound("sounds/shoot.wav")

ENGINE_SOUND.set_volume(0.5)  # 50% гучності
pygame.mixer.music.set_volume(0.2)