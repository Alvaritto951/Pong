import pygame as pg

from entidades import Bola, Raqueta

pg.init() #Se utiliza para iniciar pygame

pantalla_principal = pg.display.set_mode((800, 600))
pg.display.set_caption("Pong Álvaro")
cronometro = pg.time.Clock() #Se utiliza para fijar los milisegundos y convertir en FPS librería/módulo/función-clase

bola = Bola(400, 300)
bola.vx = 5
bola.vy = 5
#Raqueta1 = Pos en y - altura entre 2 = 300 - 60 = 240
raqueta1 = Raqueta(20, 300, w=20, h=120, color=(0, 255, 0))
#Raqueta2 = Pos en x - ancho entre 2 = 
raqueta2 = Raqueta(780, 300, w=20, h=120, color=(0, 255, 0))
raqueta2.vy = 5
raqueta1.vy = 5

#Bucle más importante para pygame 
game_over = False
while not game_over:
    dt = cronometro.tick(60) #dt = diferencial de tiempo -> Indicar los FPS dentro de los () -> 60 FPS /// Devuelve los milisegundos que tarda en mostrar en pantalla
    print(dt)
    #Eventos que hace el usuario y devuelve una lista de eventos
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game_over = True


    raqueta2.mover(pg.K_UP, pg.K_DOWN) #Aquí estaba lo que está indicado en la función "mover" en entidades
    raqueta1.mover(pg.K_w, pg.K_s)
    bola.mover()
    bola.comprobar_choque(raqueta1, raqueta2) #Se usa la función dentro de bola para ver si rebota en las raquetas (r1 & r2 en entidades)

    pantalla_principal.fill((0, 0, 0))
    bola.dibujar(pantalla_principal)
    raqueta1.dibujar(pantalla_principal)
    raqueta2.dibujar(pantalla_principal)

    #Le pasa la información a la tarjeta gráfica
    pg.display.flip()
#Hasta aquí