import pygame as pg
from pong import ALTO, ANCHO
from pong.pantallas import Menu, Partida #Records

class Controlador:
    def __init__(self): #Inicialización del objeto --- se empaqueta todo
        pantalla_principal = pg.display.set_mode((ANCHO, ALTO))
        cronometro = pg.time.Clock()

        self.menu = Menu(pantalla_principal, cronometro) #Instancia la clase Menú --- En la variable menú, tengo el objeto Menu
        self.partida = Partida(pantalla_principal, cronometro) #Instancia la clase Partida
        #records = Records() #Arrastra la clase Records
        
    def jugar(self): #Lanza el objeto -- Método Launch
        #Poner lógica de navegación entre escenas:
        salida = False
        while not salida: #Bucle infinito
            salida = self.menu.bucle_ppal() #Es el bucle que inicia la pantalla Menú
            if salida: #Para cerrar la pantalla
                break
            salida = self.partida.bucle_ppal() #Es el bucle que inicia la pantalla Juego
            
            #elif opcion == 2:
            #   self.records.bucle_ppal() #Es el bucle que inicia la pantalla Records
            

        
        pass