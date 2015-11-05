import os
import curses
import threading
from sys import argv
from time import sleep

# inicializar
pantalla = curses.initscr()
pantalla.timeout(0)
curses.start_color()
curses.init_pair(1, 7, 7)
curses.init_pair(2, 0, 0)
curses.init_pair(3, 5, 5)
from datos import *
curses.noecho()
curses.cbreak()

x, y = 0, 0


def numeroAletra(segundos):
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


class cronometro(threading.Thread):
    def run(self):
        self.ahora = ""
        self.parado = False
        self.segundos = 0
        while True:
            while not self.parado:
                self.segundos += 1
                self.letra = numeroAletra(self.segundos)

                # transforma los segundos en una string utilizable
                if self.segundos < 60: # en segundos
                    self.ahora = self.letra[6:]
                elif self.segundos < 3600: # con minutos
                    self.ahora = self.letra[3:]
                else: # con horas
                    self.ahora = self.letra
                sleep(1)

    def cambiar_estado(self):
        if self.parado:
            self.parado = False # seguir xq está parado
        elif not self.parado:
            self.parado = True  # parar xq no está parado
    def reiniciar(self):
        self.segundos = 0

cronometro = cronometro()


def dibujar(string_, color="blanco"):
    global x, y
    string = []
    for i in string_:
        string += i
        string += " "
    for caracter in range(0, len(string)):
        for fila in range(0, len(numeros[string[caracter]])):
            for pixel in range(0, len(numeros[string[caracter]][fila])):
                exceso = pixel * 2
                if numeros[string[caracter]][fila][pixel] != " ":
                    pantalla.addstr(y+fila, x+exceso,
                                    numeros[string[caracter]][fila][pixel],
                                    colores[color])
                    pantalla.addstr(y+fila, x+exceso+1,
                                    numeros[string[caracter]][fila][pixel],
                                    colores[color])
                else:
                    if color == "blanco":
                        pantalla.addstr(fila+y, exceso+x,
                                        numeros[string[caracter]][fila][pixel],
                                        colores["negro"])
                        pantalla.addstr(fila+y, exceso+x+1,
                                        numeros[string[caracter]][fila][pixel],
                                        colores["negro"])
                    if color == "negro":
                        pantalla.addstr(fila+y, exceso+x,
                                        numeros[string[caracter]][fila][pixel],
                                        colores["blanco"])
                        pantalla.addstr(fila+y, exceso+x+1,
                                        numeros[string[caracter]][fila][pixel],
                                        colores["blanco"])
                    else:
                        pass
        pantalla.move(pantalla.getmaxyx()[0]-1, pantalla.getmaxyx()[1]-1)
        x += len(numeros[string[caracter]][0])*2
    pantalla.refresh()


def pene():
    dibujar("p", "rosa")


def main():
    global cronometro
    global x, y
    pantalla.clear()
    cronometro.start()
    #cronometro.segundos = 3599


    while True:
        entrada = pantalla.getch()
        dibujar(cronometro.ahora)
        pantalla.refresh()

        if entrada == ord('t'):
            break
        elif entrada == ord('p'):
            cronometro.cambiar_estado() # parar
        elif entrada == ord('s'):
            cronometro.segundos = 0
        elif entrada == ord('m'):
            cronometro.segundos = 58
        elif entrada == ord('h'):
            cronometro.segundos = 3598
        x, y = 0, 0
        sleep(0.01)


main()
curses.nocbreak()
curses.echo()
curses.endwin()
os._exit(0)
