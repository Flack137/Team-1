from settings import *
from entiti_obstacle import EntityObstacle
import random
from bullet import Bullet
from abc import ABC, abstractmethod


class Enemy(EntityObstacle):
    def __init__(self, x, y, *groups, speed=ENEMY_SPEED):
        super().__init__(x, y, ENEMY_IMAGES["down"][0], *groups)
        self.speed = speed  # Додаємо швидкість
        self.strategy = AggressiveMovement(vision_radius = 200)  # Встановлюємо стратегію Battle City
        self.current_direction = "down"
        self.images = ENEMY_IMAGES
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.rect.inflate_ip(-self.rect.width * 0.2, -self.rect.height * 0.2)
        self.current_frame = 0  # Ініціалізація кадру
        self.last_update = 0  # Ініціалізація часу останнього оновлення анімації
        self.last_shot_time = 0
        self.shoot_interval = random.randint(800, 1500)  # Випадковий інтервал між пострілами

    def update(self, player):
        self.strategy.move(self, player)
        now = pygame.time.get_ticks()

        if now - self.last_shot_time >= self.shoot_interval:
            self.shoot()
            self.last_shot_time = now
            self.shoot_interval = random.randint(800, 1500)

        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_direction])
            self.image = pygame.image.load(self.images[self.current_direction][self.current_frame]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        direction = pygame.Vector2(0, 0)
        if self.current_direction == "up":
            direction.y = -1
        elif self.current_direction == "down":
            direction.y = 1
        elif self.current_direction == "left":
            direction.x = -1
        elif self.current_direction == "right":
            direction.x = 1
        bullet = Bullet(self.rect.center, direction, enemy_bullets, all_sprites)
        enemy_bullets.add(bullet)  # додаємо кулю до групи куль
        all_sprites.add(bullet)
        self.last_shot_time = now
        SHOOT_SOUND.play()


class MoveStrategy(ABC):
    @abstractmethod
    def move(self, enemy, player):
        pass


class ApproachingStrategy(MoveStrategy):
    def __init__(self, vision_radius = 220):
        self.directions = ["up", "down", "left", "right"]
        self.last_change_time = 0
        self.vision_radius = vision_radius
        self.change_interval = 1000  # Зміна напрямку кожну секунду

    def move(self, enemy, player):
        now = pygame.time.get_ticks()

        # Зміна напрямку через заданий інтервал
        if now - self.last_change_time > self.change_interval:
            self.last_change_time = now
            enemy.current_direction = random.choice(self.directions)

        # Рух у поточному напрямку
        if enemy.current_direction == "up":
            enemy.rect.y -= enemy.speed
        elif enemy.current_direction == "down":
            enemy.rect.y += enemy.speed
        elif enemy.current_direction == "left":
            enemy.rect.x -= enemy.speed
        elif enemy.current_direction == "right":
            enemy.rect.x += enemy.speed

        # Перевірка зіткнень із перешкодами
        if pygame.sprite.spritecollide(enemy, walls, False) or \
                pygame.sprite.spritecollide(enemy, ice_blocks, False) or \
                pygame.sprite.spritecollide(enemy, [player], False) or \
                pygame.sprite.spritecollide(enemy, iron_walls, False):
            # Відкат назад і зміна напрямку
            if enemy.current_direction == "up":
                enemy.rect.y += enemy.speed
            elif enemy.current_direction == "down":
                enemy.rect.y -= enemy.speed
            elif enemy.current_direction == "left":
                enemy.rect.x += enemy.speed
            elif enemy.current_direction == "right":
                enemy.rect.x -= enemy.speed

            enemy.current_direction = random.choice(self.directions)

        distance_to_player = enemy.rect.centerx - player.rect.centerx, enemy.rect.centery - player.rect.centery
        distance = (distance_to_player[0] ** 2 + distance_to_player[1] ** 2) ** 0.5

        if distance <= self.vision_radius:
            enemy.strategy = AggressiveMovement()


class AggressiveMovement(MoveStrategy):
    def __init__(self, vision_radius = 220):
        self.vision_radius = vision_radius  #радіус бачення

    def move(self, enemy, player):
        #обчислюємо відстань до гравця
        distance_to_player = (player.rect.centerx - enemy.rect.centerx, player.rect.centery - enemy.rect.centery)
        distance = (distance_to_player[0] ** 2 + distance_to_player[1] ** 2) ** 0.5

        #перевірка зіткнень із перешкодами
        if pygame.sprite.spritecollide(enemy, walls, False) or \
            pygame.sprite.spritecollide(enemy, ice_blocks, False) or \
            pygame.sprite.spritecollide(enemy, iron_walls, False):
            if enemy.current_direction == "up":
                enemy.rect.y += enemy.speed
            elif enemy.current_direction == "down":
                enemy.rect.y -= enemy.speed
            elif enemy.current_direction == "left":
                enemy.rect.x += enemy.speed
            elif enemy.current_direction == "right":
                enemy.rect.x -= enemy.speed

        if pygame.sprite.spritecollide(enemy, [player], False):
            if enemy.current_direction == "up":
                enemy.rect.y += enemy.speed + 1
            elif enemy.current_direction == "down":
                enemy.rect.y -= enemy.speed + 1
            elif enemy.current_direction == "left":
                enemy.rect.x += enemy.speed + 1
            elif enemy.current_direction == "right":
                enemy.rect.x -= enemy.speed + 1

        if distance <= self.vision_radius:
            #гравець в радіусі бачення
            if abs(distance_to_player[0]) > abs(distance_to_player[1]):
                #рух в горизонтальному напрямку
                if distance_to_player[0] < 0:
                    enemy.rect.x -= enemy.speed
                    enemy.current_direction = "left"
                else:
                    enemy.rect.x += enemy.speed
                    enemy.current_direction = "right"
            else:
                #рух у вертикальному напрямку
                if distance_to_player[1] < 0:
                    enemy.rect.y -= enemy.speed
                    enemy.current_direction = "up"
                else:
                    enemy.rect.y += enemy.speed
                    enemy.current_direction = "down"
        else:
            #гравець поза радіусом бачення, повертаємося до попередньої стратегії
            enemy.strategy = ApproachingStrategy()
            enemy.strategy.move(enemy, player)