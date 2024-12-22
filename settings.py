import pygame

pygame.init()
win_width = 700
win_height = 500
FPS = 40
TILESIZE = 32
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 50)

gamemap = [
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
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B....................B',
    'B.........P..........B',
    'B....................B',
    'BBBBBBBBBBBBBBBBBBBBBB',
]

wind1 = pygame.display.set_mode((win_width, win_height))
# wind2 = pygame.display.set_mode(win_height, win_width + 60)
# wind3 = pygame.display.set_mode(win_height, win_width)

player_img = 'sprites/tank3000.png'
enemy_img = 'sprite/.png'
bullet_img = 'sprite/.png'
wal = 'sprite/.png'

# wind1_bacground = pygame.transform.scale(pygame.image.load())