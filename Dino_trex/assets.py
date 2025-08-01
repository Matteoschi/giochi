import pygame

# === Caricamento immagini ===
background = pygame.image.load(r"assets/terreno.png")
nuvola = pygame.image.load(r"assets/nuvola.png")
cactus = pygame.image.load(r"assets/cactus/cactus 1.png")
sprite = [
    pygame.image.load(r"assets/sprite/sprite 1.png"),
    pygame.image.load(r"assets/sprite/sprite 2.png"),
    pygame.image.load(r"assets/sprite/sprite 3.png"),
    pygame.image.load(r"assets/sprite/sprite 4.png")
]
game_over = pygame.image.load(r"assets/game over.png")
ricomincia = pygame.image.load(r"assets/ricomincia.png")
quadrato = pygame.Rect(465, 280, 75, 67)
# === Funzioni per suoni ===
def suono_salto():
    pygame.mixer.Sound(r"assets/sound/sfx_jump.mp3").play()

def suono_collisione():
    pygame.mixer.Sound(r"assets/sound/hit.mp3").play()

def suono_punti():
    pygame.mixer.Sound(r"assets/sound/score-reached.mp3").play()
