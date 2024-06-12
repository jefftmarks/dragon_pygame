import pygame, random

pygame.init()

# Surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT //2
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
GREEN = (0, 255, 0)
DARK_GREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set fonts
font = pygame.font.Font('assets/AttackGraffiti.ttf', 32)

# Set text
score_txt = font.render(f"Score: {str(score)}", True, GREEN, DARK_GREEN)
score_rect = score_txt.get_rect()
score_rect.topleft = (10, 10)

title_txt = font.render("Feed the Dragon", True, GREEN, DARK_GREEN)
title_rect = title_txt.get_rect()
title_rect.centerx = CENTER_X
title_rect.y = 10

lives_txt = font.render(f"Lives: {str(player_lives)}", True, GREEN, DARK_GREEN)
lives_rect = lives_txt.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_txt = font.render("GAME OVER", True, GREEN, DARK_GREEN)
game_over_rect = game_over_txt.get_rect()
game_over_rect.center = (CENTER_X, CENTER_Y)

continue_txt = font.render("Press any key to play again", True, GREEN, DARK_GREEN)
continue_rect = continue_txt.get_rect()
continue_rect.center = (CENTER_X, CENTER_Y + 32)

# Set sounds
coin_sound = pygame.mixer.Sound('assets/coin_sound.wav')
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('assets/ftd_background_music.wav')

# Set images
player_img = pygame.image.load('assets/dragon_right.png')
player_rect = player_img.get_rect()
player_rect.left = 32
player_rect.centery = CENTER_Y

coin_img = pygame.image.load('assets/coin.png')
coin_rect = coin_img.get_rect()


def reset_coin():
    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


reset_coin()

# Game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # Coin movement
    if coin_rect.x < 0:
        # Missed coin
        player_lives -= 1
        miss_sound.play()
        reset_coin()
    else:
        # Move the coin
        coin_rect.x -= coin_velocity

    # Check for collisions
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        reset_coin()
    
    # Update HUD
    score_txt = font.render(f"Score: {str(score)}", True, GREEN, DARK_GREEN)
    lives_txt = font.render(f"Lives: {str(player_lives)}", True, GREEN, DARK_GREEN)

    # Check for game over
    if player_lives == 0:
        display_surface.blit(game_over_txt, game_over_rect)
        display_surface.blit(continue_txt, continue_rect)
        pygame.display.update()

        # Pause the game until player presses key
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # Player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = CENTER_Y
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Fill display
    display_surface.fill(BLACK)

    # Blit the HUD to screen
    display_surface.blit(score_txt, score_rect)
    display_surface.blit(title_txt, title_rect)
    display_surface.blit(lives_txt, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    # Blit assets to screen
    display_surface.blit(player_img, player_rect)
    display_surface.blit(coin_img, coin_rect)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End game
pygame.quit()