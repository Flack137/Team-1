from settings import *
import random
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.img = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.start_image = self.image
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, width/2, height/2)

    def cange_image (self, new_image):
        self.image = pygame.transform.scale(pygame.image.load(new_image), (self.w, self.h))
        self.start_image = self.image

    def draw (self):
        wind1.blit(self.image, self.rect)

    def reset(self):
        wind1.blit(self.image, (self.rect.x, self.rect.y))
        

class Player(Entity):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        pass

class Enemy(Entity):
    pass

