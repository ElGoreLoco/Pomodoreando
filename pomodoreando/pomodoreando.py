"""Usage:
    pomodoreando [-cid] pomodoro [-p NUMERO]
    pomodoreando [-ci] <intervalo>...

Opciones:
    -h --help               Muestra la ayuda
    -v --version            Muestra la versión
    -i --infinito           Hace que los intervalos sean infinitos
    -c --continuo           Hace que no tengas que confirmar para que comience
                            el siguiente intervalo
    -p --pomodoros NUMERO   El número de pomodoros que correrá [default: infinitos]
    -d --desc_largo         Hace que cada 4 pomodoros haya un descanso largo
"""

import os
import curses
import threading
import time
from sys import argv
from docopt import docopt

from datos import *
from __version__ import __version__

# Incializar docopt
argumentos = docopt(__doc__, version=__version__)

# Inicializar curses
pantalla = curses.initscr()
pantalla.timeout(0)
curses.start_color()
curses.init_pair(1, 7, 7)
curses.init_pair(2, 0, 0)
curses.init_pair(3, 5, 5)

colores = {"blanco": curses.color_pair(1),
           "negro": curses.color_pair(2),
           "rosa": curses.color_pair(3)
           }

curses.noecho()
curses.cbreak()

x, y = 0, 0


def lista_intervalos():
    if argumentos["pomodoro"]:
        lista = []
        for i in range(0, int(argumentos["--pomodoros"])):
            lista.append(25)
            # Cada 4 pomodoros deja un descanso largo
            if (i+1) % 4 == 0 and argumentos["--desc_largo"]:
                lista.append(15)
            else:
                lista.append(5)
        return { "intervalo": lista, "tipo": "pomodoro", "infinito": argumentos["--pomodoros"] == "infinitos" }
    else:
        """Pasa los intervalos a segundos (dependiendo de la última letra
        del argumento) y los añade a una lista que se retorna."""
        intervalo = argumentos["<intervalo>"]
        lista = []
        for i in intervalo:
            if i[-1] == 's':
                lista.append(int(i[:-1]))
            elif i[-1] == 'm':
                lista.append(int(i[:-1])*60)
            elif i[-1] == 'h':
                lista.append(int(i[:-1])*3600)
            else:
                try:
                    lista.append(int(i)*60)
                except ValueError:
                    print("El intervalo no ha sido reconocido.\n",
                          "Vuelva a intentarlo.")
        return { "intervalo": lista, "tipo": "intervalo", "infinito": argumentos["--infinito"] }


argumentos = lista_intervalos()


def numeroAletra(segundos):
    """Transforma los segundos en una string utilizable"""
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    letra = "%02d:%02d:%02d" % (h, m, s)
    if segundos < 60:  # en segundos
        return letra[6:]
    elif segundos < 3600:  # con minutos
        return letra[3:]
    else:  # con horas
        return letra


class cronometro():
    def __init__(self):
        self.inicio = int(time.time())
        self.parado = False
        self.tiempo_parado = 0

    def segundos(self):
        if self.parado:
            return (self.inicio_parado - self.inicio) - self.tiempo_parado
        else:
            return (int(time.time()) - self.inicio) - self.tiempo_parado

    def ahora(self):
        return numeroAletra(self.segundos())

    def cambiar_estado(self):
        if self.parado:
            self.parado = False  # seguir xq está parado
            self.final_parado = int(time.time())
            self.tiempo_parado += self.final_parado - self.inicio_parado
        elif not self.parado:
            self.parado = True  # parar xq no está parado
            self.inicio_parado = int(time.time())

    def reiniciar(self):
        self.inicio = int(time.time())


cronometro = cronometro()


def dibujar(string_, color="blanco"):
    global x, y
    pantalla.clear()
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
    x, y = 0, 0
    pantalla.refresh()


def pene():
    dibujar("p", "rosa")


def contar_intervalo(pos):
    while True:
        entrada = pantalla.getch()

        if entrada == ord('t') or cronometro.segundos() == argumentos["intervalo"][pos]:
            dibujar(cronometro.ahora())
            break
        elif entrada == ord('p'):
            cronometro.cambiar_estado()

        dibujar(cronometro.ahora())

        time.sleep(0.01)


def main():
    #while True:
    for i in range(len(argumentos["intervalo"])):
        contar_intervalo(i)
        time.sleep(1)
        cronometro.reiniciar()


main()
curses.nocbreak()
curses.echo()
curses.endwin()
os._exit(0)
