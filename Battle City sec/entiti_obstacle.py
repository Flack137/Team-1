from settings import *

class EntityObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, *groups):
        super().__init__(*groups)#виклик конструктору Entity
        self.image = pygame.image.load(image_path).convert_alpha()
        #завантажуємо зображення та конвертуємо його для використання з альфа-каналом. ідея НЕ моя
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        #вирівнювання зображення до розмірів блоку на мапі
        self.rect = self.image.get_rect(topleft=(x, y))
        #rect для отримання позицій

class Wall(EntityObstacle):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, WALL_IMAGE, *groups)

class IronWall(EntityObstacle):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, IRON_WALL_IMAGE, *groups)

class Ice(EntityObstacle):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, ICE_IMAGE, *groups)

class Bushes(EntityObstacle):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, BUSH_IMAGE, *groups)