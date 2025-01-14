import pygame
from tilemap import *

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
ENEMY_SPEED = 1.75
BULLET_SPEED = int(PLAYER_SPEED * 5)
#швидкості переміщення об'єктів

PLAYER_IMAGES = {
    "up": ["sprites/player_animation/player_up1.png", "sprites/player_animation/player_up2.png"],
    "down": ["sprites/player_animation/player_down1.png", "sprites/player_animation/player_down2.png"],
    "left": ["sprites/player_animation/player_l1.png", "sprites/player_animation/player_l2.png"],
    "right": ["sprites/player_animation/player_r1.png", "sprites/player_animation/player_r2.png"]
} #зображення для анімацій гравця

WALL_IMAGE = "sprites/obstacle_sprites/wall.png"
ICE_IMAGE = "sprites/obstacle_sprites/ice.png"
BUSH_IMAGE = "sprites/obstacle_sprites/bushes.png"
IRON_WALL_IMAGE = "sprites/obstacle_sprites/iron_wall.jpg"
#зображення стін та льоду(води), кущів

ENEMY_IMAGES = {
    "up": ["sprites/enemy_animation/enemy.png", "sprites/enemy_animation/enemy2.png"],
    "down": ["sprites/enemy_animation/enemy_down1.png", "sprites/enemy_animation/enemy_down2.png"],
    "left": ["sprites/enemy_animation/enemy_l1.png", "sprites/enemy_animation/enemy_l2.png"],
    "right": ["sprites/enemy_animation/enemy_r1.png", "sprites/enemy_animation/enemy_r2.png"]
} #зображення для анімацій ворогів

BULLETS_IMAGE = "sprites/bullet_explosion/bullet.jpg"
BOOM_IMAGES = [
    "sprites/bullet_explosion/boom1.png",
    "sprites/bullet_explosion/boom2.png",
    "sprites/bullet_explosion/boom3.png"
]

LOSE = "sprites/result_images/lossimage.png"

WIN = "sprites/result_images/victoryimage.png"

pygame.mixer.music.load("sounds/vietnam.mp3")
BOOM_SOUND = pygame.mixer.Sound("sounds/boom.wav")
ENGINE_SOUND = pygame.mixer.Sound("sounds/engine.wav")
SHOOT_SOUND = pygame.mixer.Sound("sounds/shoot.wav")
WIN_SOUND = pygame.mixer.Sound("sounds/victory_sound.mp3")
DEFEAT_SOUND = pygame.mixer.Sound("sounds/defeat_sound.mp3")
GAME_START_SOUND = pygame.mixer.Sound("sounds/game_start_bc.mp3")
ENGINE_SOUND.set_volume(0.1)
SHOOT_SOUND.set_volume(0.08)
WIN_SOUND.set_volume(0.3)
DEFEAT_SOUND.set_volume(0.1)
GAME_START_SOUND.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)
BOOM_SOUND.set_volume(0.08)
print("PLAYER_IMAGES['down'][0]:", PLAYER_IMAGES["down"][0])


enemy_bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
ice_blocks = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
bushes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
iron_walls = pygame.sprite.Group()
