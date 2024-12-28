from settings import *
from main_objects import Entity
from abc import ABC, abstractmethod
import math

class Player(Entity):
    def __init__(self, x, y, *groups, walls, iron_walls, ice_blocks, bushs, enemies):
        super().__init__(x, y, PLAYER_IMAGES["down"][0], *groups)
        #ініціалізація положення і початкового спрайту гравця
        self.direction = pygame.Vector2(0, 0)#вектор напрямку руху. ідея не моя
        self.images = PLAYER_IMAGES#анмації
        self.current_frame = 0#поточний кадр анімації
        self.last_update = 0#останнє оновлення
        self.current_direction = "down"#поточний напрям
        self.walls = walls#група стін
        self.ice_blocks = ice_blocks#група льоду(води)
        self.bushs = bushs
        self.enemies = enemies
        self.iron_walls = iron_walls
        self.last_shot_time = 0
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.rect.inflate_ip(-self.rect.width * 0.2, -self.rect.height * 0.2)

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2(0, 0)
        #отримання натискань та оновлення напрямку
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.current_direction = "up"
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.current_direction = "down"
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.current_direction = "left"
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.current_direction = "right"
        #рух в залежності від натиснутої кнопки

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        #нормалізуємо напрямок, якщо він не нульовий

        self.rect.x += self.direction.x * PLAYER_SPEED
        #оновлення по Х
        if pygame.sprite.spritecollide(self, self.walls, False) or pygame.sprite.spritecollide(self, self.ice_blocks, False) or pygame.sprite.spritecollide(self, self.enemies, False) or pygame.sprite.spritecollide(self, self.iron_walls, False):
            self.rect.x -= self.direction.x * PLAYER_SPEED
        #перевірка на зіткнення із перешкодами по X

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        #перевірка меж вікна по X

        self.rect.y += self.direction.y * PLAYER_SPEED
        #ононвлення по Y
        if pygame.sprite.spritecollide(self, self.walls, False) or pygame.sprite.spritecollide(self, self.ice_blocks, False) or pygame.sprite.spritecollide(self, self.enemies, False) or pygame.sprite.spritecollide(self, self.iron_walls, False):
            self.rect.y -= self.direction.y * PLAYER_SPEED
        #перевірка на зіткнення із перешкодами по Y

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        #перевірка меж вікна по Y

        now = pygame.time.get_ticks() #оновлення анімації
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.images[self.current_direction])
            #перехід на новий кадр
            self.image = pygame.image.load(self.images[self.current_direction][self.current_frame]).convert_alpha()
            #завантаження нового кадру
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            #маштабування нового кадру

    def shoot(self, bullets, all_sprites):
        #визначаємо напрямок руху кулі залежно від поточного напрямку гравця
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= 1200:
            direction = pygame.Vector2(0, 0)
            if self.current_direction == "up":
                direction.y = -1
            elif self.current_direction == "down":
                direction.y = 1
            elif self.current_direction == "left":
                direction.x = -1
            elif self.current_direction == "right":
                direction.x = 1
            bullet = Bullet(self.rect.center, direction, bullets, all_sprites)
            bullets.add(bullet)  #додаємо кулю до групи куль
            all_sprites.add(bullet)
            self.last_shot_time = now
            SHOOT_SOUND.play()



class Bullet(Entity):
    def __init__(self, position, direction, *groups):
        x, y = position
        self.image = pygame.image.load(BULLETS_IMAGE).convert_alpha()  # Додано .png
        super().__init__(x, y, BULLETS_IMAGE, *groups)
        self.direction = direction.normalize()
        # self.image = pygame.image.load(BULLETS_IMAGES["up"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE // 3, TILE_SIZE // 3))
        self.rect = self.image.get_rect(center=(x , y))
        self.exploding = False
        self.explosion_images = BOOM_IMAGES
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        #якщо куля не вибухає, вона рухається
        if not self.exploding:
            self.rect.x += self.direction.x * BULLET_SPEED
            self.rect.y += self.direction.y * BULLET_SPEED

            if not (0 <= self.rect.x <= WINDOW_WIDTH and 0 <= self.rect.y <= WINDOW_HEIGHT):
                self.kill()

        if self.exploding:
            # Якщо куля вибухає відтворюємо анімацію
            self.animate_explosion()

    def start_explosion(self):
        self.exploding = True
        BOOM_SOUND.play()
        self.direction = pygame.Vector2(0, 0)  
        self.image = pygame.image.load(self.explosion_images[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate_explosion(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame < len(self.explosion_images):
                self.image = pygame.image.load(self.explosion_images[self.current_frame]).convert_alpha()
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            else:
                self.kill()  # Видалення кулі після завершення анімації


#цей клас Денис робив
class Enemy(Entity):
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
