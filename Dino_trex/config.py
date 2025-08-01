import pygame

# === Costanti schermo ===
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 75

# === Colori ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# === Font ===
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)