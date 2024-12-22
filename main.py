from objects import*
import sys
pygame.init()

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Game Menu")

play_text = font.render("Start", True, BLACK)
exit_text = font.render("Exit", True, BLACK)
play_rect = play_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
exit_rect = exit_text.get_rect(center=(win_width // 2, win_height // 2 + 50))

game = True
running = True

while game:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
            #     if play_rect.collidepoint(event.pos):
            #         wind2 = pygame.display.set_mode((win_height, win_width + 60))
            #         wind2.fill(BLACK)  
            #         pygame.display.set_caption("Second Window")
                running = False
            #         player = Player(player_img, win_width // 2, win_height // 2, 50, 50, 5)
            #         running = False
            #     if exit_rect.collidepoint(event.pos):
            #         game = False
            #         running = False

        wind1.fill(GRAY)
        wind1.blit(play_text, play_rect)
        wind1.blit(exit_text, exit_rect)

        pygame.display.flip()

    # while not running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             game = False
    #             running = True

    #     player.update()
    #     wind2.fill(BLACK)
    #     player.draw()

    #     pygame.display.flip()

pygame.quit()
sys.exit()