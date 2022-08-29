import pygame as pg
import random
from entidades import Bola, Raqueta

pg.init()

pantalla_principal = pg.display.set_mode((800, 600))
pg.display.set_caption("Pong Álvaro")

bola = Bola(400, 300)
#Raqueta1 = Pos en y - altura entre 2 = 300 - 60 = 240
raqueta1 = Raqueta(20, 300, w=20, h=120, color=(0, 255, 0))
#Raqueta2 = Pos en x - ancho entre 2 = 
raqueta2 = Raqueta(780, 300, w=20, h=120, color=(0, 255, 0))

game_over = False
while not game_over:
    #Eventos que hace el usuario y devuelve una lista de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True
    pantalla_principal.fill((0, 0, 0))
    bola.dibujar(pantalla_principal)
    raqueta1.dibujar(pantalla_principal)
    raqueta2.dibujar(pantalla_principal)
    #Le pasa la información a la tarjeta gráfica
    pg.display.flip()