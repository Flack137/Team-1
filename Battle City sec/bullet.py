from settings import *


class Bullet(EntityObstacle):
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