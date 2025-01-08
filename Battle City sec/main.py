from settings import *
from enemy import Enemy
from player import Player
from entiti_obstacle import EntityObstacle, Wall, Ice, Bushes, IronWall
import time

class Game:
    def __init__(self):
        pygame.init()
        self.elims = 0
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
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
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
        for row_index, row in enumerate(Tilemap):
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

    def wait_for_explosions(self):
        while any(sprite.exploding for sprite in self.all_sprites if hasattr(sprite, 'exploding')):
            self.clock.tick(FPS)  # Keep ticking to maintain FPS
            self.handle_events()
            self.update()
            self.draw()

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
                        self.playing = True # Запуск гри
                        GAME_START_SOUND.play()
                        ENGINE_SOUND.play(-1)
                    elif quit_button.collidepoint(event.pos):
                        self.running = False

    def run2(self):
        # Лічильник знищених ворогів
        GAME_START_SOUND.play()
        eliminations = 0
        total_enemies = len(self.enemies_list)  # Загальна кількість ворогів

        while self.playing:
            self.clock.tick(FPS)  # Обмежена кількість кадрів на сек. (60)
            self.handle_events()  # Обробник подій
            self.update()  # Оновлення

            # Перевірка на знищення ворогів
            eliminations = total_enemies - len(self.enemies)  # Знищені вороги

            if eliminations >= total_enemies:
                # Wait for all explosion animations to finish
                self.wait_for_explosions()
                self.playing = False
                ENGINE_SOUND.stop()
                WIN_SOUND.play()
                self.show_victory_screen()  # Показ екрану перемоги


            self.draw()  # Відмальовування на екран

    def show_victory_screen(self):
        # Load the victory image
        victory_image = pygame.image.load(WIN).convert_alpha()
        victory_image = pygame.transform.scale(victory_image, (500, 500))  # Adjust size if needed

        # Blit the victory image onto the center of the screen
        image_rect = victory_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(victory_image, image_rect)
        pygame.display.flip()  # Update the display

        # Pause for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    pygame.quit()
                    return

            pygame.time.delay(100)  # Prevent high CPU usage during the delay

        # Reset the game states properly
        self.playing = False
        self.running = True  # Keep the game running
        self.__init__()  # Reinitialize game objects

        self.run()  # Return to the start screen

    def show_defeat_screen(self):
        # Load the victory image
        defeat_image = pygame.image.load(LOSE).convert_alpha()
        defeat_image = pygame.transform.scale(defeat_image, (750, 500))  # Adjust size if needed

        # Blit the victory image onto the center of the screen
        image_rect = defeat_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(defeat_image, image_rect)
        pygame.display.flip()  # Update the display

        start_time = time.time()
        while time.time() - start_time < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    pygame.quit()
                    return

            pygame.time.delay(100)  # Prevent high CPU usage during the delay

        self.playing = False
        self.running = True  # Keep the game running
        self.__init__()  # Reinitialize game objects
        self.run()  # Return to the start screen


    def handle_events(self):
        #обробка всіх подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            #завершення циклу
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.player_bullets, self.all_sprites)
                elif event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = True
                    ENGINE_SOUND.stop()
                    self.run()

    def update(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.update(self.player, self.enemy_bullets, self.all_sprites)  # Передаємо гравця тільки ворогам
            else:
                sprite.update()
        # функція оновлення: спрайтів та колізій(наприклад події зіткнення)
        for bullet in self.player_bullets:
            collided_walls = pygame.sprite.spritecollide(bullet, self.walls, True)
            if collided_walls:
                bullet.start_explosion()
            elif pygame.sprite.spritecollide(bullet, self.enemies, True):
                bullet.start_explosion()
                self.elims += 1  # Збільшуємо лічильник знищених ворогів
            elif pygame.sprite.spritecollide(bullet, self.iron_walls, False):
                bullet.start_explosion()
        for bullet in self.enemy_bullets:
            collided_walls = pygame.sprite.spritecollide(bullet, self.walls, True)
            if pygame.sprite.collide_rect(bullet, self.player):
                DEFEAT_SOUND.play()  # Відтворення звуку поразки
                ENGINE_SOUND.stop()  # Зупинка звуку двигуна
                self.show_defeat_screen()  # Показ екрану поразки
                return 
            elif collided_walls:
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

#bullets