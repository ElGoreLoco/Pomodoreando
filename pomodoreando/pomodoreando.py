"""Usage:
    pomodoreando [-cid] pomodoro [-p NUMERO]
    pomodoreando [-ci] <intervalo>...

Opciones:
    -h --help               Muestra la ayuda
    -v --version            Muestra la versión
    -i --infinito           Hace que la lista de intervalos se repita
                            infinitamente
    -c --continuo           Hace que no tengas que confirmar para que comience
                            el siguiente intervalo
    -p --pomodoros NUMERO   El número de pomodoros que correrá
                            [default: infinitos]
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

# Inicializar docopt
entrada = docopt(__doc__, version=__version__)

# Inicializar ncurses
pantalla = curses.initscr()
pantalla.timeout(0)
curses.start_color()
curses.init_pair(1, 7, 7)
curses.init_pair(2, 0, 0)
curses.init_pair(3, 5, 5)
curses.init_pair(4, 7, 0)
curses.init_pair(5, 0, 7)

colores_planos = {
        "blanco": curses.color_pair(1),
        "negro": curses.color_pair(2),
        "rosa": curses.color_pair(3)
}
colores_texto = {
        "blanco": curses.color_pair(4),
        "negro": curses.color_pair(5),
}

curses.noecho()
curses.cbreak()

x, y = 0, 0


def lista_intervalos():
    """Devuelve un diccionario con la entrada."""
    if entrada["pomodoro"]:
        intervalo = []
        if entrada["--pomodoros"] == "infinitos":
            for i in range(0, 4):
                intervalo.append(25)
                # Cada 4 pomodoros deja un descanso largo
                if (i+1) % 4 == 0 and entrada["--desc_largo"]:
                    intervalo.append(15)
                else:
                    intervalo.append(5)
        else:
            for i in range(0, int(entrada["--pomodoros"])):
                intervalo.append(25)
                # Cada 4 pomodoros deja un descanso largo
                if (i+1) % 4 == 0 and entrada["--desc_largo"]:
                    intervalo.append(15)
                else:
                    intervalo.append(5)
        return {"intervalo": intervalo, "tipo": "pomodoro",
                "infinito": entrada["--pomodoros"] == "infinitos"}
    else:
        intervalo = []
        for i in entrada["<intervalo>"]:
            """Crea una lista de intervalos con los entrada que se han dado.
            """
            if i[-1] == 's':
                intervalo.append(int(i[:-1]))
            elif i[-1] == 'm':
                intervalo.append(int(i[:-1])*60)
            elif i[-1] == 'h':
                intervalo.append(int(i[:-1])*3600)
            else:
                try:
                    intervalo.append(int(i)*60)
                except ValueError:
                    print("El intervalo no ha sido reconocido.\n",
                          "Vuelva a intentarlo.")
        return {"intervalo": intervalo, "tipo": "intervalo",
                "infinito": entrada["--infinito"]}


argumentos = lista_intervalos()


def numeroAletra(segundos):
    """Transforma los segundos en una cadena utilizable"""
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    letra = "%02d:%02d:%02d" % (h, m, s)
    if segundos < 60:  # en segundos
        return letra[6:]
    elif segundos < 3600:  # con minutos
        return letra[3:]
    else:  # con horas
        return letra


class Cronometro():
    """Gestiona el contador."""
    def __init__(self):
        self.inicio = int(time.time())
        self.parado = False
        self.tiempo_parado = 0

    def segundos(self):
        """Devuelve el número de segundos que han pasado desde que se inició el
        cronómetro.
        """
        if self.parado:
            return (self.inicio_parado - self.inicio) - self.tiempo_parado
        else:
            return (int(time.time()) - self.inicio) - self.tiempo_parado

    def ahora(self):
        """Devuelve una cadena estilizada con el tiempo que ha pasado desde que
        se inició el cronómetro.
        """
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


cronometro = Cronometro()


class Dibujar():
    def tiempo(self, cadena_arg, color="blanco"):
        """Dibuja en la terminal los carácteres dados."""
        global x, y
        ancho = 0
        alto = 5
        pantalla.clear()
        cadena = []
        for i in cadena_arg:
            """Transforma la cadena dada en una cadena con la que se puede
            trabajar.
            """
            cadena += i
            cadena += " "
        for i in cadena:
            ancho += len(numeros[i][0])*2
        ancho -= 2
        y = int(pantalla.getmaxyx()[0]/2 - alto/2)
        x = int(pantalla.getmaxyx()[1]/2 - ancho/2)
        for caracter in range(0, len(cadena)):
            for fila in range(0, len(numeros[cadena[caracter]])):
                for pixel in range(0, len(numeros[cadena[caracter]][fila])):
                    exceso = pixel * 2
                    if numeros[cadena[caracter]][fila][pixel] != " ":
                        pantalla.addstr(
                                y+fila, x+exceso,
                                numeros[cadena[caracter]][fila][pixel],
                                colores_planos[color]
                        )
                        pantalla.addstr(
                                y+fila, x+exceso+1,
                                numeros[cadena[caracter]][fila][pixel],
                                colores_planos[color]
                        )
                    else:
                        if color == "blanco":
                            pantalla.addstr(
                                    fila+y, exceso+x,
                                    numeros[cadena[caracter]][fila][pixel],
                                    colores_planos["negro"]
                            )
                            pantalla.addstr(
                                    fila+y, exceso+x+1,
                                    numeros[cadena[caracter]][fila][pixel],
                                    colores_planos["negro"]
                            )
                        elif color == "negro":
                            pantalla.addstr(
                                    fila+y, exceso+x,
                                    numeros[cadena[caracter]][fila][pixel],
                                    colores_planos["blanco"]
                            )
                            pantalla.addstr(
                                    fila+y, exceso+x+1,
                                    numeros[cadena[caracter]][fila][pixel],
                                    colores_planos["blanco"]
                            )
            x += len(numeros[cadena[caracter]][0])*2
        pantalla.move(pantalla.getmaxyx()[0]-1, pantalla.getmaxyx()[1]-1)

    def mensaje(self, texto, color="blanco"):
        centro = [pantalla.getmaxyx()[0]/2, pantalla.getmaxyx()[1]/2]
        y = int(centro[0] + 3)
        x = int(centro[1] - len(texto)/2)
        pantalla.addstr(y, x, texto, colores_texto[color])
        pantalla.move(pantalla.getmaxyx()[0]-1, pantalla.getmaxyx()[1]-1)

    def pene(self):
        self.tiempo("p", "rosa")


dibujar = Dibujar()


def salir():
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    os._exit(0)


def main():
    primera_vez = True
    while argumentos["infinito"] or primera_vez:
        for i in argumentos["intervalo"]:
            while True:
                entrada = pantalla.getch()
                if entrada == ord('t') or cronometro.segundos() == i:
                    dibujar.tiempo(cronometro.ahora())
                    dibujar.mensaje("El cronómeto ha terminado")
                    pantalla.refresh()
                    time.sleep(1)
                    cronometro.reiniciar()
                    break
                elif entrada == ord('T'):
                    salir()
                elif entrada == ord('p'):
                    cronometro.cambiar_estado()
                dibujar.tiempo(cronometro.ahora())
                pantalla.refresh()
                time.sleep(0.01)
        primera_vez = False


main()
salir()
