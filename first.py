import pygame
from sys import exit

pygame.init()
ventana = pygame.display.set_mode((800, 400))
pygame.display.set_caption("jumpything")
reloj = pygame.time.Clock()
fuente = pygame.font.Font('cositas/fuente/fuentepix.ttf',50)

cielo = pygame.image.load('cositas/gráficos/cielo.png').convert()
suelo = pygame.image.load('cositas/gráficos/suelo.png').convert()
texto = fuente.render('burbujas', False, 'Gray')

caracol = pygame.image.load('cositas/gráficos/caracol/caracol1.png').convert_alpha()
rect_caracol = caracol.get_rect(midbottom = (900,300))

jugador = pygame.image.load('cositas/gráficos/jugador/caminar1.png').convert_alpha()
rect_jugador = jugador.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ventana.blit(cielo,(0,0))
    ventana.blit(suelo,(0,300))
    ventana.blit(texto,(300,50))
    rect_caracol.right -= 4
    if rect_caracol.right < -100:rect_caracol.right = 900
    ventana.blit(caracol,rect_caracol)

    if rect_jugador.colliderect(rect_caracol):
        print("xokesito piujjj")

    
    ventana.blit(jugador,rect_jugador)

    pygame.display.update()
    reloj.tick(60)
