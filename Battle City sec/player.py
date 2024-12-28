from settings import *


class Player(EntityObstacle):
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