import pygame, sys, random

pygame.init()
pygame.mixer.init()

# Ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego Pygame")

# Sonidos
sonido_fondo = pygame.mixer.Sound("assets/sonidos/fondo.mp3")
sonido_fondo.set_volume(0.2)
sonido_fondo.play()
choque = pygame.mixer.Sound("assets/sonidos/choque.mp3")
choque.set_volume(0.3)

# Jugador
jugador_size = 50
jugador_x = width // 2 - jugador_size // 2
jugador_y = height - 2 * jugador_size
jugador_speed = 5
jugador_image = pygame.image.load("assets/imagenes/jugador.png")
jugador_image = pygame.transform.scale(jugador_image, (jugador_size, jugador_size))

# Enemigos
enemigo_size = 50
enemigo_speed = 2
enemigo_image = pygame.image.load("assets/imagenes/enemigo.png")
enemigo_image = pygame.transform.scale(enemigo_image, (enemigo_size, enemigo_size))
enemigos = []

# Fondo
background_image = pygame.image.load("assets/imagenes/fondo.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Reloj
clock = pygame.time.Clock()

# Estado del juego
juego_activo = False
score = 0
high_score = 0

# Funciones
def mostrar_jugador(x, y):
    screen.blit(jugador_image, (x, y))

def mostrar_enemigo(x, y):
    screen.blit(enemigo_image, (x, y))

def mostrar_menu():
    font_path = "assets/fuentes/VCR_OSD_MONO_1.001.ttf"
    font_titulo = pygame.font.Font(font_path, 55)
    font = pygame.font.Font(None, 36)
    screen.blit(background_image, (0, 0))
    texto_menu = font_titulo.render("MENU", True, (255, 255, 255))
    screen.blit(texto_menu, (width // 2 - 90, height // 2 - 100))
    inicio = font.render("Presiona ESPACIO para iniciar", True, (255, 255, 255))
    salir = font.render("Presiona Q para salir", True, (255, 255, 255))
    screen.blit(inicio, (width // 2 - 200, height // 2 - 18))
    screen.blit(salir, (width // 2 - 200, height // 2 + 18))

def mostrar_score():
    font = pygame.font.Font(None, 36)
    texto_score = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    screen.blit(texto_score, (10, 10))

def mostrar_highscore():
    font = pygame.font.Font(None, 36)
    texto_highscore = font.render(f"Record: {high_score}", True, (255, 255, 255))
    screen.blit(texto_highscore, (10, 50))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (width // 2 - 150, height // 2 - 30))
    pygame.display.flip()
    pygame.time.wait(2000)
    reset_game()

def reset_game():
    global jugador_x, jugador_y, enemigos, juego_activo
    jugador_x = width // 2 - jugador_size // 2
    jugador_y = height - 2 * jugador_size
    enemigos = []
    juego_activo = False

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not juego_activo:
                    reset_game()
                    juego_activo = True
            elif event.key == pygame.K_q:
                if not juego_activo:
                    pygame.quit()
                    sys.exit()

    keys = pygame.key.get_pressed()

    if juego_activo:
        jugador_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * jugador_speed

        # Limitar al jugador dentro de la pantalla
        jugador_x = max(0, min(width - jugador_size, jugador_x))

        # Mover enemigos y comprobar colisiones
        for enemigo in enemigos:
            enemigo[1] += enemigo_speed

            if enemigo[1] > height:
                enemigos.remove(enemigo)
                enemigos.append([random.randint(0, width - enemigo_size), 0])
                score += 1 # Suma puntaje

            if score > high_score:
                high_score = score # Actualiza el puntaje más alto

            if (
                jugador_x < enemigo[0] + enemigo_size
                and jugador_x + jugador_size > enemigo[0]
                and jugador_y < enemigo[1] + enemigo_size
                and jugador_y + jugador_size > enemigo[1]
            ):
                choque.play()
                game_over()
                score = 0

        # Generar nuevos enemigos
        if random.random() < 0.02:
            enemigos.append([random.randint(0, width - enemigo_size), 0])

        # Mostrar fondo
        screen.blit(background_image, (0, 0))

        # Mostrar jugador
        mostrar_jugador(jugador_x, jugador_y)

        # Mostrar enemigos
        for enemigo in enemigos:
            mostrar_enemigo(enemigo[0], enemigo[1])

        # Mostrar puntajes
        mostrar_score()
        mostrar_highscore()

    else:
        # Mostrar menú
        mostrar_menu()

    # Actualizar pantalla
    pygame.display.flip()

    # Establecer velocidad de fotogramas
    clock.tick(60)