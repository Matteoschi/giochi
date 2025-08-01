import pygame
import sys
import random
pygame.init()

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK,screen, clock, font
from assets import background, nuvola, cactus, sprite, game_over, ricomincia , suono_salto, suono_collisione, suono_punti , quadrato
from levels import livelli

debugging = False

# === SETUP FINESTRA ===
pygame.display.set_caption("Pygame Dino Runner")

# === VARIABILI GIOCO ===
indice_livello_attuale = 0
lista_cactus = []
incremento_vel_terreno = 6
timer_spawn = 0
vel_terreno = 0
walkpoint = 0
anim_timer = 0
posizione_sprite_y = 422
velocità_salto = 0
gravity = 1
punti = 0
sta_salando = False
collisione_rilevata = False
random_inizio = 100
random_fine = 250

# === RESET ===
def reset_game():
    global punti, collisione_rilevata, incremento_vel_terreno, lista_cactus
    global vel_terreno, indice_livello_attuale, random_inizio, random_fine
    global posizione_sprite_y, velocità_salto, sta_salando
    punti = 0
    collisione_rilevata = False
    incremento_vel_terreno = 6
    vel_terreno = 0
    indice_livello_attuale = 0
    random_inizio = 100
    random_fine = 250
    lista_cactus.clear()
    posizione_sprite_y = 422
    velocità_salto = 0
    sta_salando = False

# === CICLO PRINCIPALE ===
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # === EVENTI ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not sta_salando:
                sta_salando = True
                velocità_salto = -20
                suono_salto()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quadrato.collidepoint(event.pos) and collisione_rilevata:
                print("Punti:", punti)
                reset_game()

    # === SALTO ===
    if sta_salando and not collisione_rilevata:
        posizione_sprite_y += velocità_salto
        velocità_salto += gravity
        if posizione_sprite_y >= 415:
            posizione_sprite_y = 422
            sta_salando = False

    # === ANIMAZIONE ===
    if not collisione_rilevata and not sta_salando:
        anim_timer += 3
    if anim_timer >= 20:
        walkpoint = (walkpoint + 1) % 4
        anim_timer = 0

    screen.blit(sprite[walkpoint], [50, posizione_sprite_y])
    player_hitbox = pygame.Rect(65, posizione_sprite_y + 15, 65, 70)
    if debugging:
        pygame.draw.rect(screen, (255, 0, 0), player_hitbox, 2)
        pygame.draw.rect(screen, BLACK, quadrato)

    # === SPAWN CACTUS ===
    timer_spawn += random.randint(1, 2)
    timer_randomizzato = random.randint(random_inizio, random_fine)
    if timer_spawn > timer_randomizzato:
        lista_cactus.append(SCREEN_WIDTH + random.randint(0, random_fine))
        timer_spawn = 0

    # === GESTIONE CACTUS ===
    for i in range(len(lista_cactus) - 1, -1, -1):
        lista_cactus[i] -= incremento_vel_terreno
        cactus_x = lista_cactus[i]

        screen.blit(cactus, [cactus_x, 418])
        cactus_hitbox = pygame.Rect(cactus_x, 418, cactus.get_width(), cactus.get_height())

        if player_hitbox.colliderect(cactus_hitbox) and not collisione_rilevata:
            suono_collisione()
            vel_terreno = 0
            incremento_vel_terreno = 0
            collisione_rilevata = True

        if player_hitbox.colliderect(cactus_hitbox):
            screen.blit(game_over, [SCREEN_HEIGHT // 2, 200])
            screen.blit(ricomincia, [465, 280])

        if cactus_x < -cactus.get_width():
            lista_cactus.pop(i)

        if debugging:
            pygame.draw.rect(screen, (0, 255, 0), cactus_hitbox, 2)

    # === TERRENO ===
    vel_terreno -= incremento_vel_terreno
    if vel_terreno <= -background.get_width():
        vel_terreno = 0

    screen.blit(background, [vel_terreno, 400])
    screen.blit(background, [vel_terreno + background.get_width(), 400])
    screen.blit(nuvola, [vel_terreno, 100])
    screen.blit(nuvola, [vel_terreno + background.get_width(), 100])

    # === PUNTEGGIO E LIVELLI ===
    if not collisione_rilevata:
        punti += 1
        if indice_livello_attuale < len(livelli):
            livello = livelli[indice_livello_attuale]
            if punti >= livello["soglia"]:
                incremento_vel_terreno = livello["velocità"]
                random_inizio = livello["spawn_min"]
                random_fine = livello["spawn_max"]
                suono_punti()
                indice_livello_attuale += 1

    if debugging:
        print(f"Vel: {incremento_vel_terreno}, Spawn: {random_inizio}-{random_fine}, Timer: {timer_spawn}/{timer_randomizzato}")

    # === PUNTEGGIO ===
    punti_text = font.render(f"Punti: {punti}", True, BLACK)
    screen.blit(punti_text, (10, 10))

    # === UPDATE DISPLAY ===
    pygame.display.flip()

# === USCITA ===
pygame.quit()
sys.exit()
