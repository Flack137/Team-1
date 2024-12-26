from settings import *
from main_objects import Sprites, Obstacle, Wall, Ice, Bushes, IronWall
from secondary_objects import Player, Enemy, Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))#створення вікна
        pygame.display.set_caption("Battle City")#заголовок вікна
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = True
        self.enemies_list = []
        #під'єднання груп спрайтів
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.ice_blocks = pygame.sprite.Group()
        self.bushes = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.iron_walls = pygame.sprite.Group()
        #створення об'єкту гравця
        self.player = Player(
            9 * TILE_SIZE, 
            19 * TILE_SIZE, 
            self.all_sprites, 
            walls = self.walls, 
            bushs = self.bushes,
            enemies = self.enemies,
            iron_walls = self.iron_walls,
            ice_blocks = self.ice_blocks
        )
        self.load_map()#завантаження мапи

    def load_map(self):
        for row_index, row in enumerate(tilemap):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                if tile == "B":
                    Wall(x, y, self.all_sprites, self.walls)
                #відтворення стіни на мапі
                elif tile == "L":
                    Ice(x, y, self.all_sprites, self.ice_blocks)
                #відтворення льоду (води) на мапі
                elif tile == "P":
                    self.player.rect.topleft = (x, y)
                #відтворення гравця на мапі
                elif tile == "E":
                    enemy = Enemy(x, y, self.enemies_list, self.walls, self.ice_blocks, self.iron_walls, self.all_sprites, self.enemies)
                    self.enemies_list.append(enemy)
                #відтворення ворога на мапі
                elif tile == "K":
                    Bushes(x, y, self.all_sprites, self.bushes)
                #відтворення кущів на мапі
                elif tile == "I":
                    IronWall(x, y, self.all_sprites, self.iron_walls)

    def run(self):
        # Метод для відображення стартового екрану
        font = pygame.font.Font(None, 74)
        start_text = font.render("ГРАТИ", True, (255, 255, 255))
        quit_text = font.render("ВИЙТИ", True, (255, 255, 255))

        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 80, 200, 50)
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10, 200, 50)
        # continue_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 10, 200, 50)

        while self.running:
            self.screen.fill((128, 128, 128))  # Сірий фон
            pygame.draw.rect(self.screen, (0, 0, 0), start_button)
            pygame.draw.rect(self.screen, (0, 0, 0), quit_button)

            self.screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_HEIGHT // 2 - 75))
            self.screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, WINDOW_HEIGHT // 2 + 15))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.running = False  # Завершення стартового вікна
                        self.playing = True  # Запуск гри
                        ENGINE_SOUND.play(-1)
                    elif quit_button.collidepoint(event.pos):
                        self.running = False

    def run2(self):
        #функція з основним циклом
        pygame.mixer.music.play()  # Відтворення фонової музики в циклі
        while self.playing:
            self.clock.tick(FPS)#обмежена кількість кадрів на сек. (60)
            self.handle_events()#функція-обробник подій
            self.update()#оновлення
            self.draw()#відмальовування на екран

    def handle_events(self):
        #обробка всіх подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            #завершення циклу
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.bullets, self.all_sprites)
                elif event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = True
                    ENGINE_SOUND.stop()
                    self.run()

    def update(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.update(self.player)  # Передаємо гравця тільки ворогам
            else:
                sprite.update()
    #функція оновлення: спрайтів та колізій(наприклад події зіткнення)
        for bullet in self.bullets:
            collided_walls = pygame.sprite.spritecollide(bullet, self.walls, True)
            if collided_walls:
                bullet.start_explosion()
            elif pygame.sprite.spritecollide(bullet, self.enemies, True):
                bullet.start_explosion()
            elif pygame.sprite.spritecollide(bullet, self.iron_walls, False):
                bullet.start_explosion()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
    #відмальовування фону


if __name__ == "__main__":
#якщо цей файл основний
    game = Game()
    game.run()#запускається основний цикл
    game.run2()
    pygame.quit()#завершення роботи

