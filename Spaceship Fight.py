# Author: Puru Soni (purusoni@buffalo.edu)

import os
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_MODERATE_GREEN_LIME = (79, 175, 68)
VIVID_RED = (239, 68, 35)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

FPS = 60

VEL = 5
BULLET_VEL = 10

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!")

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "space.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    red_health_text = HEALTH_FONT.render(f"HEALTH: {red_health}", True, VIVID_RED)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    yellow_health_text = HEALTH_FONT.render(f"HEALTH: {yellow_health}", True, VIVID_RED)
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and not (yellow.x - VEL < 5):
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and not (yellow.x + VEL + yellow.width - 15 > WIDTH // 2 - BORDER.width // 2):
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and not (yellow.y - VEL - 5 < 0):
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and not (yellow.y + VEL + yellow.height + 20 > HEIGHT):
        yellow.y += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and not (red.x - VEL < WIDTH // 2 + BORDER.width // 2):
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and not (red.x + red.width + VEL > WIDTH):
        red.x += VEL
    if keys_pressed[pygame.K_UP] and not (red.y - VEL < 0):
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and not (red.y + VEL + red.height + 20 > HEIGHT):
        red.y += VEL


def handle_bullets(yellow, red, yellow_bullets, red_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()

        if bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(winner):
    winner_text = WINNER_FONT.render(f"{winner} WINS!", True, DARK_MODERATE_GREEN_LIME)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    yellow_health = 100
    red_health = 100
    winner = ''

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(yellow_bullets) < 3:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RALT and len(red_bullets) < 3:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 10
            if event.type == YELLOW_HIT:
                yellow_health -= 10

        if yellow_health <= 0:
            winner = "RED"
        if red_health <= 0:
            winner = "YELLOW"
        if not winner == '':
            draw_winner(winner)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow, red, yellow_bullets, red_bullets)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
