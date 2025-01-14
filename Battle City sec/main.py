from settings import *
from enemy import Enemy
from player import Player
from entiti_obstacle import Wall, Ice, Bushes, IronWall
import time


class Game:
    def __init__(self):
        pygame.init()
        self.elims = 0
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Створення вікна
        pygame.display.set_caption("Battle City")  # Заголовок вікна
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = True
        self.enemies_list = []
        self.reset_game()  # Очищення груп спрайтів та ініціалізація гри
        # Створення об'єкту гравця
        self.player = Player(9 * TILE_SIZE, 19 * TILE_SIZE, all_sprites)
        self.load_map()  # завантаження мапи

    def reset_game(self):
        # Очищення всіх груп спрайтів
        all_sprites.empty()
        walls.empty()
        ice_blocks.empty()
        enemies.empty()
        bushes.empty()
        iron_walls.empty()
        player_bullets.empty()
        enemy_bullets.empty()

    def load_map(self):
        for row_index, row in enumerate(Tilemap):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                if tile == "B":
                    Wall(x, y, all_sprites, walls)
                # відтворення стіни на мапі
                elif tile == "L":
                    Ice(x, y, all_sprites, ice_blocks)
                # відтворення льоду (води) на мапі
                elif tile == "P":
                    self.player.rect.topleft = (x, y)
                # відтворення гравця на мапі
                elif tile == "E":
                    enemy = Enemy(x, y, all_sprites, enemies)
                    self.enemies_list.append(enemy)
                # відтворення ворога на мапі
                elif tile == "K":
                    Bushes(x, y, all_sprites, bushes)
                # відтворення кущів на мапі
                elif tile == "I":
                    IronWall(x, y, all_sprites, iron_walls)

    def wait_for_explosions(self):
        while any(sprite.exploding for sprite in all_sprites if hasattr(sprite, 'exploding')):
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
                        self.playing = True  # Запуск гри
                        GAME_START_SOUND.play()
                        ENGINE_SOUND.play(-1)
                    elif quit_button.collidepoint(event.pos):
                        self.running = False

    def run2(self):
        # Лічильник знищених ворогів
        GAME_START_SOUND.play()
        score = 0
        total_enemies = len(self.enemies_list)  # Загальна кількість ворогів
        pygame.mixer.music.play()

        while self.playing:
            self.clock.tick(FPS)  # Обмежена кількість кадрів на сек. (60)
            self.handle_events()  # Обробник подій
            self.update()  # Оновлення

            # Перевірка на знищення ворогів
            score = total_enemies - len(enemies)  # Знищені вороги

            if score == total_enemies:
                pygame.mixer.music.stop()
                # Wait for all explosion animations to finish
                self.wait_for_explosions()
                self.playing = False
                ENGINE_SOUND.stop()
                WIN_SOUND.play()
                self.show_result(WIN, 500, 500)  # Показ екрану перемоги

            if self.playing:
                self.draw()  # Відмальовування на екран

    def show_result(self, image, x, y):
        # Load the victory image
        result = pygame.image.load(image).convert_alpha()
        result = pygame.transform.scale(result, (x, y))  # Adjust size if needed

        # Blit the victory image onto the center of the screen
        image_rect = result.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(result, image_rect)
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

    def handle_events(self):
        # обробка всіх подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            # завершення циклу
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = True
                    ENGINE_SOUND.stop()
                    self.run()

    def update(self):
        for sprite in all_sprites:
            if isinstance(sprite, Enemy):
                sprite.update(self.player)  # Передаємо гравця тільки ворогам
            else:
                sprite.update()

        for bullet in player_bullets:
            if pygame.sprite.spritecollide(bullet, enemies, True):
                bullet.start_explosion()
                self.elims += 1  # Збільшуємо лічильник знищених ворогів
        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, self.player):
                pygame.mixer.music.stop()
                DEFEAT_SOUND.play()  # Відтворення звуку поразки
                ENGINE_SOUND.stop()  # Зупинка звуку двигуна
                self.show_result(LOSE, 700, 500)  # Показ екрану поразки
                return
        all_bullets = player_bullets.copy()
        all_bullets.add(enemy_bullets)
        for bullet in all_bullets:
            collided_walls = pygame.sprite.spritecollide(bullet, walls, True)
            if collided_walls:
                bullet.start_explosion()
            elif pygame.sprite.spritecollide(bullet, iron_walls, False):
                bullet.start_explosion()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(self.screen)
        pygame.display.flip()
    # відмальовування фону


if __name__ == "__main__":
    # якщо цей файл основний
    game = Game()
    game.run()  # запускається основний цикл
    game.run2()
    pygame.quit()  # завершення роботи