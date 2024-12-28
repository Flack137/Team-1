from settings import *


class Enemy(EntityObstacle):
    def __init__(self, x, y, enemies, walls, ice_blocks, iron_walls, *groups):
        super().__init__(x, y, ENEMY_IMAGES["down"][0], *groups)
        # self.strategy = ManhattanDistance()#вибір стратегії обчислення відстані
        self.images = ENEMY_IMAGES
        self.current_frame = 0
        self.last_update = 0
        self.current_direction = "down"
        self.strategy = ApproachingStrategy()  # Встановлюємо початкову стратегію
        self.enemies = enemies
        self.walls = walls  # Додаємо групу стін
        self.ice_blocks = ice_blocks  # Додаємо групу льодових блоків
        self.iron_walls = iron_walls 
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.rect.inflate_ip(-self.rect.width * 0.2, -self.rect.height * 0.2)

    def update(self, player):
        # Виклик стратегії руху
        self.strategy.move(self, player)
        now = pygame.time.get_ticks()

        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_direction])
            self.image = pygame.image.load(self.images[self.current_direction][self.current_frame]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))


class MoveStrategy(ABC):
    @abstractmethod
    def move(self, enemy, player):
        pass

class ApproachingStrategy(MoveStrategy):
    def move(self, enemy, player):
        original_position = enemy.rect.topleft
        # Рух ворога до гравця
        if abs(enemy.rect.x - player.rect.x) > abs(enemy.rect.y - player.rect.y):
            # Рух по X
            if enemy.rect.x < player.rect.x:
                enemy.rect.x += ENEMY_SPEED
                enemy.current_direction = "right"
                # Перевірка на зіткнення
                if pygame.sprite.spritecollide(enemy, enemy.walls, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.ice_blocks, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.iron_walls, False):
                    enemy.rect.x -= ENEMY_SPEED  # Відкат назад
            else:
                enemy.rect.x -= ENEMY_SPEED
                enemy.current_direction = "left"
                # Перевірка на зіткнення
                if pygame.sprite.spritecollide(enemy, enemy.walls, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.ice_blocks, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.iron_walls, False):
                    enemy.rect.x += ENEMY_SPEED  # Відкат назад
        else:
            # Рух по Y
            if enemy.rect.y < player.rect.y:
                enemy.rect.y += ENEMY_SPEED
                enemy.current_direction = "down"
                # Перевірка на зіткнення
                if pygame.sprite.spritecollide(enemy, enemy.walls, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.ice_blocks, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.iron_walls, False):
                    enemy.rect.y -= ENEMY_SPEED  # Відкат назад
            else:
                enemy.rect.y -= ENEMY_SPEED
                enemy.current_direction = "up"
                # Перевірка на зіткнення
                if pygame.sprite.spritecollide(enemy, enemy.walls, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.ice_blocks, False) or \
                   pygame.sprite.spritecollide(enemy, enemy.iron_walls, False):
                    enemy.rect.y += ENEMY_SPEED  # Відкат назад

        if pygame.sprite.collide_rect(enemy, player):
            enemy.rect.topleft = original_position  # Відкат до початкової позиції

        # Перевірка на зіткнення з іншими ворогами
        for other_enemy in enemy.enemies:
            if other_enemy != enemy and pygame.sprite.collide_rect(enemy, other_enemy):
                enemy.rect.topleft = original_position

class DistanceStrategy(MoveStrategy):
    def move(self, enemy, player):
        # Тримати дистанцію 2 тайли
        distance_x = player.rect.x - enemy.rect.x
        distance_y = player.rect.y - enemy.rect.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance < 2 * TILE_SIZE:  # Якщо ворог ближче ніж 2 тайли
            if abs(distance_x) > abs(distance_y):
                # Рух по X
                if distance_x > 0:
                    enemy.rect.x -= ENEMY_SPEED
                    enemy.current_direction = "left"
                else:
                    enemy.rect.x += ENEMY_SPEED
                    enemy.current_direction = "right"
            else:
                # Рух по Y
                if distance_y > 0:
                    enemy.rect.y -= ENEMY_SPEED
                    enemy.current_direction = "up"
                else:
                    enemy.rect.y += ENEMY_SPEED
                    enemy.current_direction = "down"

class DirectionStrategy(MoveStrategy):
    def move(self, enemy, player):
        # Якщо гравець напрямлений у протилежний бік, ворог рухається в притул
        player_direction = player.current_direction
        if player_direction == "up" and enemy.rect.y > player.rect.y:
            enemy.rect.y += ENEMY_SPEED
            enemy.current_direction = "down"
        elif player_direction == "down" and enemy.rect.y < player.rect.y:
            enemy.rect.y -= ENEMY_SPEED
            enemy.current_direction = "up"
        elif player_direction == "left" and enemy.rect.x > player.rect.x:
            enemy.rect.x += ENEMY_SPEED
            enemy.current_direction = "right"
        elif player_direction == "right" and enemy.rect.x < player.rect.x:
            enemy.rect.x -= ENEMY_SPEED
            enemy.current_direction = "left"
