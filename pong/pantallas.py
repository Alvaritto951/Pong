import pygame as pg
from pong.entidades import Bola, Raqueta
from pong import ALTO, ANCHO, AMARILLO, FPS, NARANJA, NEGRO, BLANCO, PRIMER_AVISO, ROJO, SEGUNDO_AVISO, TIEMPO_MAXIMO_PARTIDA


class Partida:
    def __init__(self):
        self.pantalla_principal = pg.display.set_mode((ANCHO, ALTO)) #La pantalla en grande/negro
        pg.display.set_caption("Pong Álvaro") #Nombre de la pantalla
        self.cronometro = pg.time.Clock() #Se utiliza para fijar los milisegundos y convertir en FPS librería/módulo/función-clase
        self.temporizador = TIEMPO_MAXIMO_PARTIDA #Viene del __init__ #180000 milisegundos = 18 segundos. Son los segundos que dura el juego

        self.bola = Bola(ANCHO // 2, ALTO // 2, color=BLANCO)
        self.raqueta1 = Raqueta(20, ALTO // 2, w=20, h=120, color=BLANCO)
        self.raqueta1.vy = 5
        self.raqueta2 = Raqueta(ANCHO - 20, ALTO // 2, w=20, h=120, color=BLANCO)
        self.raqueta2.vy = 5

        self.puntuacion1 = 0
        self.puntuacion2 = 0

        self.fuenteMarcador = pg.font.Font("pong/fonts/staatliches.ttf", 40) #Se indica el tipo de fuente de la letra
        self.fuenteTemporizador = pg.font.Font("pong/fonts/staatliches.ttf", 20)

        self.contadorFotogramas = 0 #se utiliza para empezar a parpadear la pantalla a X fotogramas
        self.fondoPantalla = NEGRO

        
    def fijar_fondo(self): #se definen los fondos para cambiar en función de los segundos que queden de juego
        self.contadorFotogramas += 1
        if self.temporizador > PRIMER_AVISO:
            self.contadorFotogramas = 0            
        elif self.temporizador > SEGUNDO_AVISO:
            #cada 10 fotogramas cambia de naranja a negro y viceversa
            if self.contadorFotogramas == 10: #Cada 10 fotogramas, si la pantalla es negro, cambia a naranja, si no, se queda igual
                if self.fondoPantalla == NEGRO:
                    self.fondoPantalla = NARANJA
                else:
                    self.fondoPantalla = NEGRO
                self.contadorFotogramas = 0
        else:
            #cada 5 fotogramas cambia de rojo a negro y viceversa
            if self.contadorFotogramas == 5: #Cada 5 fotogramas, si la pantalla es negro, cambia a rojo, si no, se queda igual
                if self.fondoPantalla == NEGRO:
                    self.fondoPantalla = ROJO
                else:
                    self.fondoPantalla = NEGRO
                self.contadorFotogramas = 0
        
        return self.fondoPantalla
           
                

    def bucle_ppal(self):
        self.bola.vx = 5
        self.bola.vy = -5

        #Bucle más importante para pygame 
        game_over = False
        while not game_over and \
            self.puntuacion1 < 10 and \
            self.puntuacion2 < 10 and \
            self.temporizador > 0: #Entro en el bucle mientras la puntuacion sea menor de 10 y temporizador es mayor que 0
            salto_tiempo = self.cronometro.tick(FPS) #dt = diferencial de tiempo -> Indicar los FPS dentro de los () -> 60 FPS /// Devuelve los milisegundos que tarda en mostrar en pantalla
            #Eventos que hace el usuario y devuelve una lista de eventos
            self.temporizador -= salto_tiempo #Contar el tiempo hacia atrá basándonos en los FPS, es decir, va a la misma velocidad

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True


            self.raqueta2.mover(pg.K_UP, pg.K_DOWN) #Aquí estaba lo que está indicado en la función "mover" en entidades
            self.raqueta1.mover(pg.K_w, pg.K_s)
            quien = self.bola.mover()
            if quien == "RIGHT":
                self.puntuacion2 += 1
                print(f"{self.puntuacion1} - {self.puntuacion2}")
            elif quien == "LEFT":
                self.puntuacion1 += 1
                print(f"{self.puntuacion1} - {self.puntuacion2}")
            
            #if self.puntuacion1 > 9 or self.puntuacion2 > 9:
             #   game_over = True  -> Se indica en el while y nos ahorramos hacer otro if. Se utiliza para cerrar/reiniciar el juego una vez llegue a 10


            self.bola.comprobar_choque(self.raqueta1, self.raqueta2) #Se usa la función dentro de bola para ver si rebota en las raquetas (r1 & r2 en entidades)

            #color_fondo = self.fijar_fondo()
            #self.pantalla_principal.fill(color_fondo) #Se haría de esta manera si indicaramos el atributo color_fondo

            self.pantalla_principal.fill(self.fijar_fondo()) #Aquí se pinta el fondo de la pantalla
            self.bola.dibujar(self.pantalla_principal) #Se dibuja la bola
            self.raqueta1.dibujar(self.pantalla_principal) #Se dibuja raqueta1
            self.raqueta2.dibujar(self.pantalla_principal) #Se dibuja raqueta2

            p1 = self.fuenteMarcador.render(str(self.puntuacion1), True, BLANCO) #Se indica el marcador a cada esquina de la pantalla
            self.pantalla_principal.blit(p1, (40,10))
            p2 = self.fuenteMarcador.render(str(self.puntuacion2), True, BLANCO)
            self.pantalla_principal.blit(p2, (ANCHO - 60,10))
            temporizador = self.fuenteTemporizador.render(str(self.temporizador / 1000), True, BLANCO) #Es el marcador en la pantalla (una imagen), el contador es Contador
            self.pantalla_principal.blit(temporizador, (ANCHO // 2, 10))
            

            #Le pasa la información a la tarjeta gráfica
            pg.display.flip()
        #Hasta aquí