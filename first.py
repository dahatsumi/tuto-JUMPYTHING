from sys import exit
import pygame
from random import randint


def mostrar_puntaje():
    tiempo = int(pygame.time.get_ticks()/1000) - tiempo_comienzo
    puntaje = fuente.render(f'{tiempo}', False, (64, 64, 64))
    rect_puntaje = puntaje.get_rect(center=(400, 40))
    ventana.blit(puntaje, rect_puntaje)
    return tiempo


def mov_obstaculos(lista_obstcls):
    if lista_obstcls:
        for rect_obstcls in lista_obstcls:
            rect_obstcls.x -= 5

            if rect_obstcls.bottom == 300:
                ventana.blit(caracol, rect_obstcls)

            else:
                ventana.blit(mosca, rect_obstcls)

        lista_obstcls = [
            obstaculos for obstaculos in lista_obstcls if obstaculos.x > -100]

        return lista_obstcls
    else:
        return []


def colisiones(jugador, obstcls):
    if obstcls:
        for rect_obstcls in obstcls:
            if jugador.colliderect(rect_obstcls):
                return False
    return True


def animación_jugador():
    global jugador, jugador_index

    if rect_jugador.bottom < 300:
        jugador = jugador_saltar
    else:
        jugador_index += 0.1
        if jugador_index >= len(lista_jugador_caminar):
            jugador_index = 0
        jugador = lista_jugador_caminar[int(jugador_index)]


pygame.init()
ventana = pygame.display.set_mode((800, 400))
pygame.display.set_caption("jumpything")
reloj = pygame.time.Clock()
fuente = pygame.font.Font('cositas/fuente/fuentepix.ttf', 50)
juego_activo = False
tiempo_comienzo = 0
puntaje_guardado = 0

cielo = pygame.image.load('cositas/gráficos/cielo.png').convert()
suelo = pygame.image.load('cositas/gráficos/suelo.png').convert()

# Obstáculos

# Caracol
caracol_1 = pygame.image.load(
    'cositas/gráficos/caracol/caracol1.png').convert_alpha()
caracol_2 = pygame.image.load(
    'cositas/gráficos/caracol/caracol2.png').convert_alpha()
Lista_caracol = [caracol_1, caracol_2]
caracol_index = 0
caracol = Lista_caracol[caracol_index]

# Mosca
mosca_1 = pygame.image.load(
    'cositas/gráficos/mosca/mosca1.png').convert_alpha()
mosca_2 = pygame.image.load(
    'cositas/gráficos/mosca/mosca2.png').convert_alpha()
lista_mosca = [mosca_1, mosca_2]
mosca_index = 0
mosca = lista_mosca[mosca_index]


lista_rect_obstcls = []


jugador_caminar1 = pygame.image.load(
    'cositas/gráficos/jugador/caminar1.png').convert_alpha()
jugador_caminar2 = pygame.image.load(
    'cositas/gráficos/jugador/caminar2.png').convert_alpha()
lista_jugador_caminar = [jugador_caminar1, jugador_caminar2]
jugador_index = 0
jugador_saltar = pygame.image.load(
    'cositas/gráficos/jugador/saltar.png').convert_alpha()

jugador = lista_jugador_caminar[jugador_index]
rect_jugador = jugador.get_rect(midbottom=(80, 300))

grav_jugador = 0


# Pantalla intro/game over
jugador_tieso = pygame.image.load(
    'cositas/gráficos/jugador/tieso.png').convert_alpha()
jugador_tieso = pygame.transform.scale2x(jugador_tieso)
rect_tieso = jugador_tieso.get_rect(center=(400, 200))

titulo = fuente.render('JUMPYTHING', False, (111, 196, 169))
rect_titulo = titulo.get_rect(center=(400, 80))

mensaje = fuente.render(
    'presiona espacio para comenzar', False, (111, 196, 169))
rect_mensaje = mensaje.get_rect(center=(400, 320))


# Temporizadores
temp_obstaculos = pygame.USEREVENT + 1
pygame.time.set_timer(temp_obstaculos, 1800)

temp_caracol = pygame.USEREVENT + 2
pygame.time.set_timer(temp_caracol, 500)

temp_mosca = pygame.USEREVENT + 3
pygame.time.set_timer(temp_mosca, 200)


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if juego_activo:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_jugador.collidepoint(event.pos) and rect_jugador.bottom >= 300:
                    grav_jugador = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and rect_jugador.bottom >= 300:
                    grav_jugador = -20

            if event.type == temp_obstaculos:
                if randint(0, 2):
                    lista_rect_obstcls.append(caracol.get_rect(
                        midbottom=(randint(900, 1100), 300)))
                else:
                    lista_rect_obstcls.append(mosca.get_rect(
                        midbottom=(randint(900, 1100), 200)))

            if event.type == temp_caracol:
                if caracol_index == 0:
                    caracol_index = 1
                else:
                    caracol_index = 0
                caracol = Lista_caracol[caracol_index]

            if event.type == temp_mosca:
                if mosca_index == 0:
                    mosca_index = 1
                else:
                    mosca_index = 0
                mosca = lista_mosca[mosca_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                juego_activo = True
                tiempo_comienzo = int(pygame.time.get_ticks()/1000)

    if juego_activo:

        ventana.blit(cielo, (0, 0))
        ventana.blit(suelo, (0, 300))
        # pygame.draw.rect(ventana, 'Pink', rect_puntaje,)
        # ventana.blit(puntaje, rect_puntaje)
        puntaje_guardado = mostrar_puntaje()

        # rect_caracol.right -= 4
        # if rect_caracol.right < -100:
        #     rect_caracol.right = 900
        # ventana.blit(caracol, rect_caracol)

        # Jugador
        grav_jugador += 1
        rect_jugador.y += grav_jugador
        if rect_jugador.bottom >= 300:
            rect_jugador.bottom = 300
        animación_jugador()
        ventana.blit(jugador, rect_jugador)

        # Movimiento de obstáculos
        lista_rect_obstcls = mov_obstaculos(lista_rect_obstcls)

        # Colisión
        juego_activo = colisiones(rect_jugador, lista_rect_obstcls)

    else:
        ventana.fill((94, 129, 162))
        ventana.blit(jugador_tieso, rect_tieso)
        lista_rect_obstcls.clear()
        rect_jugador.midbottom = (80, 300)
        grav_jugador = 0

        mensaje_puntaje = fuente.render(
            f'tu puntaje: {puntaje_guardado}', False, (111, 196, 169))
        rect_puntaje = mensaje_puntaje.get_rect(center=(400, 320))
        ventana.blit(titulo, rect_titulo)

        if puntaje_guardado == 0:
            ventana.blit(mensaje, rect_mensaje)
        else:
            ventana.blit(mensaje_puntaje, rect_puntaje)

    pygame.display.update()
    reloj.tick(60)
