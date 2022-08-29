import pygame as pg

from entidades import Bola, Raqueta

pg.init()

pantalla_principal = pg.display.set_mode((800, 600))
pg.display.set_caption("Pong Álvaro")

bola = Bola(400, 300)
#Raqueta1 = Pos en y - altura entre 2 = 300 - 60 = 240
raqueta1 = Raqueta(20, 300, w=20, h=120, color=(0, 255, 0))
#Raqueta2 = Pos en x - ancho entre 2 = 
raqueta2 = Raqueta(780, 300, w=20, h=120, color=(0, 255, 0))
raqueta2.vy = 5

game_over = False
while not game_over:
    #Eventos que hace el usuario y devuelve una lista de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
        elif evento.type == pg.KEYDOWN:
            if evento.key == pg.K_DOWN:
                raqueta2.center_y += raqueta2.vy
            elif evento.key == pg.K_UP:
                raqueta2.center_y -= raqueta2.vy
    
    estado_teclas = pg.key.get_pressed()
    if estado_teclas[pg.K_UP]:
        raqueta2.center_y -= raqueta2.vy
    if estado_teclas[pg.K_DOWN]:
        raqueta2.center_y += raqueta2.vy
 
    pantalla_principal.fill((0, 0, 0))
    bola.dibujar(pantalla_principal)
    raqueta1.dibujar(pantalla_principal)
    raqueta2.dibujar(pantalla_principal)
    #Le pasa la información a la tarjeta gráfica
    pg.display.flip()