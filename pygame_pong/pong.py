import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

ball = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 15, 30, 30)
player_1= pygame.Rect(5, SCREEN_HEIGHT // 2 - 60, 20, 120)
player_2 = pygame.Rect(SCREEN_WIDTH - 25, SCREEN_HEIGHT // 2 - 60, 20, 120)

def draw():
    pygame.draw.ellipse(screen,WHITE,ball)
    pygame.draw.rect(screen, WHITE, player_1)
    pygame.draw.rect(screen,WHITE, player_2)   
    pygame.draw.line(screen,GRAY,(SCREEN_WIDTH // 2, 0),(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2-50),2)
    pygame.draw.line(screen,GRAY,(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2+50),(SCREEN_WIDTH // 2, SCREEN_HEIGHT),2)


def draw_score():
    small_font = pygame.font.SysFont(None, 28)
    score_surface = small_font.render(f"Punti: {punti}", True, WHITE)
    screen.blit(score_surface, (10, 10))

def animation():
    if player_1.y <= 0:
        player_1.y = 0
    if player_1.y >= SCREEN_HEIGHT-120:
        player_1.y = SCREEN_HEIGHT - 120
    if player_2.y <= 0:
        player_2.y = 0
    if player_2.y >= SCREEN_HEIGHT-120:
        player_2.y = SCREEN_HEIGHT - 120


ball_speed= 5
a = random.choice([-1, 1])
b= random.choice([-1, 1])
ball_speed_x= ball_speed * a
ball_speed_y= ball_speed * b
player_speed_1 = 0
player_speed_2 = 0
punti = 0
indice_livello=0
allenamento = True

gioco= True
running = True
# Play start sound once at the beginning
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    if ball.y >= SCREEN_HEIGHT - 30 or ball.y <= 0:
        ball_speed_y *= -1

    fattore = 1 + (punti / 2000) 
    ball_speed_x = ball_speed * fattore * (1 if ball_speed_x > 0 else -1)
    ball_speed_y = ball_speed * fattore * (1 if ball_speed_y > 0 else -1)

    if gioco:
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        player_1.y += player_speed_1
        player_2.y += player_speed_2
        punti +=1
    else:
        ball_speed_x = 0
        ball_speed_y = 0


    if ball.x >= SCREEN_WIDTH-30:
        gioco= False
        score_surface = font.render(f"Player 1 win", True, GRAY)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_surface, score_rect)
    if ball.x <= 0:
        gioco = False
        score_surface = font.render(f"Player 2 win", True, GRAY)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_surface, score_rect)

    if ball.colliderect(player_1):
        ball.left = player_1.right  # riposiziona subito a destra del paddle
        ball_speed_x *= -1

    if ball.colliderect(player_2):
        ball.right = player_2.left  # riposiziona subito a sinistra del paddle
        ball_speed_x *= -1
    
    if allenamento:
        player_2 .y = ball.y
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed_1 += 9
            if event.key == pygame.K_UP:
                player_speed_1 -= 9
            if not allenamento:
                if event.key == pygame.K_s:
                    player_speed_2 += 9
                if event.key == pygame.K_w:
                    player_speed_2 -= 9
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed_1 -= 9
            if event.key == pygame.K_UP:
                player_speed_1 += 9
            if not allenamento:
                if event.key == pygame.K_s:
                    player_speed_2 -= 9
                if event.key == pygame.K_w:
                    player_speed_2 += 9

    draw_score()
    animation()
    draw()
    pygame.display.flip()

pygame.quit()
sys.exit()