import pygame
import os

# Initialize font and sound mixer
pygame.font.init()
pygame.mixer.init()

# Create a window with the predetermined height and width
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game")

# In-game colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Border
BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Game Variables
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4
SHIP_WIDTH, SHIP_HEIGHT = 55, 40

# Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(RED_SPACESHIP_IMAGE, -90)

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

def draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    # Draw the background
    WIN.blit(SPACE, (0, 0))

    # Draw the border
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {str(yellow_health)}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Draw the assets
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, ((WIDTH//2) - (draw_text.get_width() // 2), (HEIGHT // 2) - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:                              # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:                              # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 12:    # DOWN
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + (yellow.width / 2) < BORDER.x:  # RIGHT
        yellow.x += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_KP_4] and red.x - VEL > BORDER.x:                       # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_KP_8] and red.y - VEL > 0:                              # UP
        red.y -= VEL
    if keys_pressed[pygame.K_KP_2] and red.y + VEL + red.height < HEIGHT - 12:       # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_KP_6] and red.x + VEL + (red.width / 2) < WIDTH:        # RIGHT
        red.x += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    # If I don't call this, I get an error when exiting the game.
    pygame.init()

    # Represent the spaceships (and everything else) as rectangles.
    red = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    # Initialize the health and winning condition of the game
    red_health = 10
    yellow_health = 10
    winner_text = ""

    # Game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        # Run the game at 60 FPS (unless the computer is slower).
        clock.tick(FPS)

        # Get a list of events in Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + (yellow.height // 2) - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + (red.height // 2) - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"
        
        if winner_text != "":
            draw_winner(winner_text)    # SOMEONE WON
            break

        # Get what keys are getting pressed down.
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)

    main()

if __name__ == '__main__':
    main()