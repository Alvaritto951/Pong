from random import randint

import pygame as pg


class Bola:
    def __init__(self, center_x, center_y, radio=10, color=(255, 255, 0)):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.radio = radio
        
        self.vx = 0
        self.vy = 0
    
    def dibujar(self, pantalla):
        pg.draw.circle(pantalla, self.color, (self.center_x, self.center_y), self.radio)

    def mover(self, x_max = 800, y_max = 600): #Dimensiones del rectángulo donde se mueve la bola  ---  Cambiar center_x & center_y (para que se mueva) y x_max e y_max (para definir los rebotes)
        self.center_x += self.vx #Velocidad de x -> positivo hacia dcha; negativo hacia izda
        self.center_y += self.vy #velocidad de y -> positivo hacia abajo; negativo hacia arriba
        if self.center_y >= y_max - self.radio or self.center_y < self.radio: #Rebota en 0 y en 600
            #self.center_y += self.vy * -1 --> Si se hace así, lo que hace la bola es seguir el borde de la pantalla, no rebota.
            self.vy *= -1 #Cambiar dirección de la bola rebotando
        
        if self.center_x >= x_max: #Si entra gol, sale desde el centro de la pantalla
            self.center_x = x_max // 2
            self.center_y = y_max // 2

            self.vx *= -1 #Cambiar dirección a la bola, justo la contraria al marcar gol
            self.vy *= -1
            #self.vx *= randint() #Cambiar dirección a la bola aleatoriamente
            #self.vy *= randint
            
            return "LEFT"
        
        if self.center_x < 0:
            self.center_x = x_max // 2
            self.center_y = y_max // 2

            self.vx *= -1 #Cambiar dirección a la bola, justo la contraria al marcar gol
            self.vy *= -1

            return "RIGHT"

    
    @property #Decorador que sirve para quitar los paréntesis del final. Métodos enmascarados como atributos.
    def izquierda(self): #Sirve para ver si la bola y la raqueta coinciden en coordenadas (intersección). Son métodos.
        return self.center_x - self.radio
    @property
    def derecha(self):
        return self.center_x + self.radio
    @property
    def arriba(self):
        return self.center_y - self.radio
    @property
    def abajo(self):
        return self.center_y + self.radio
    
    def comprobar_choque(self, *raquetas):  
        #Rebote genérico de bola en raqueta
        for raqueta_activa in raquetas:
            if self.derecha >= raqueta_activa.izquierda and \
                self.abajo >= raqueta_activa.arriba and \
                self.arriba <= raqueta_activa.abajo and \
                self.izquierda <= raqueta_activa.derecha:
                    self.vx *= -1
                    return
            
   
  
class Raqueta:
    """
    x: posicion centro x
    y: posicion centro y
    w: anchura de la raqueta
    h: altura de la raqueta
    color: tupla RGB de color
    """
    
    file_imagenes = {
        "izq": ["electric00.png", "electric01.png", "electric02.png"],
        "dcha": ["electric00_.png", "electric01_.png", "electric02_.png"]
    } #Diccionario de imágenes

    def __init__(self, center_x, center_y, w=120, h=20, color=(255, 255, 0)):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.w = w
        self.h = h

        self.vx = 0
        self.vy = 0

        self.imagenes = self.__cargar_imagenes()
        self.direccion = 'izq'
        self.imagen_activa = 0
        self.cambio_cada_x_fotogramas = 5 #Cada X fotogramas, la imagen va a rotar para que no vaya a velocidad indefinida
        self.cuenta_fotogramas = 0

        #self._imagen = pg.image.load(f"pong/images/{self.imagenes['izq']}") #para una sola imagen --- #convert.alpha() --- pixels transparentes

    def __cargar_imagenes(self):
        calcomanias = {}
        for lado in self.file_imagenes: #Te busca dentro de claves
            calcomanias[lado] = []
            for img in self.file_imagenes[lado]: #Te busca dentro de valor
                nueva_surface = pg.image.load(f"pong/images/{img}")
                calcomanias[lado].append(nueva_surface) #Añadimos la imagen al diccionario

        return calcomanias        
    """
    @property #Recupera algo --- Getter --- Propiedad de Lectura
    def imagen(self): 
        return self._imagen

    @imagen.setter #Graba algo --- Setter --- Propiedad de Escritura
    def imagen(self, valor):
        self._imagen = pg.image.load(f"pong/images/{self.imagenes[valor]}") #Sirve para poder escribir la dcha o la izqda
    """

    def dibujar(self, pantalla):
        pantalla.blit(self.imagenes[self.direccion][self.imagen_activa], (self.center_x - self.w // 2, self.center_y - self.h // 2))
        self.cuenta_fotogramas += 1 #Cuenta fotogramas
        if self.cuenta_fotogramas == self.cambio_cada_x_fotogramas: #Si el tiempo que pasa es igual a los fotogramas indicados
            self.imagen_activa += 1 #Añade 1, es decir, cambia a la siguiente imagen
            if self.imagen_activa >= len(self.imagenes[self.direccion]): #Si las imágenes superan la longitud del total de la lista,
                self.imagen_activa = 0  #Se le añade una imagen cada vez, pero hay que ponerle tope indicando que si es mayor o igual a la longitud de la cadena, me lo vuelva a poner en la posición inicial (0)
            self.cuenta_fotogramas = 0  #Pone el contador de fotogramas a 0
        #pantalla.blit(self._imagen, (self.center_x - self.w // 2, self.center_y - self.h // 2)) #Utilizando una sola imagen
        #pg.draw.rect(pantalla, self.color, (self.center_x - self.w // 2, self.center_y - self.h // 2, self.w, self.h)) --- Este es el rectángulo blanco
    
    def mover(self, tecla_arriba, tecla_abajo, y_max=600): #Son parámetros que luego se indican en main con la tecla que quieres pulsar y ver el máximo de pantalla (ymax)
        estado_teclas = pg.key.get_pressed() #Devuelve lista de 512 teclas -> Función que indica estado del teclado -> De cada tecla devuelve False si no tocas nada
        if estado_teclas[tecla_arriba]: #Tecla que se va a pulsar hacia arriba
            self.center_y -= self.vy
        if self.center_y < 0 + self.h // 2: #Movimiento de la raqueta hacia arriba
            self.center_y = self.h // 2
        if estado_teclas[tecla_abajo]:
            self.center_y += self.vy
        if self.center_y > y_max - self.h // 2: #Movimiento de la raqueta hacia abajo
            self.center_y = y_max - self.h // 2
    
    @property #Decorador que sirve para quitar los paréntesis del final. Métodos enmascarados como atributos.
    def izquierda(self): #Sirve para ver si la bola y la raqueta coinciden en coordenadas (intersección). Son métodos.
        return self.center_x - self.w // 2
    @property
    def derecha(self):
        return self.center_x + self.w // 2
    @property
    def arriba(self):
        return self.center_y - self.h // 2
    @property
    def abajo(self):
        return self.center_y + self.h // 2





