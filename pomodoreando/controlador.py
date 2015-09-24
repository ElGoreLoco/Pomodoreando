import sys

import cronometro

argumento = sys.argv[1]
"""
hay tres opciones:
    - poner "pomodoro" para que inicie la secuencia de 25 y 5 minutos
    - poner el tiempo(en minutos) que se desea que cronometre
    - no poner nada o "ayuda" para que imprima la ayuda
"""

if argumento == "":
    print(
"""AYUDA
Ponga como primer argumento el número de minutos que quiere que
espere el cronómetro, o «pomodoro» para que haga intervalos de
25 y 5 minutos.
Cuando esté corriendo el cronómetro, puede pulsar la tecla «p»
para parar o proseguir el cronómetro, y la letra «t» para terminar
el cronómetro.""")

elif argumento == "pomodoro":
    siguiente = "p"     # variable que indica si el siguiente tiempo es un pomodoro o un descanso
    pomodoros = 0
    
    while siguiente != "t":
        if siguiente == "p":
            cronometro.cronometro(25*60, "Pomodoro")
            print("""
Si desea empezar el descanso corto de 5min, introduzca «d»,
y si desea empezar el descanso largo de 15min, introduzca «dl».
Si en cambio desea terminar, introduzca «t».""")
            pomodoros += 1
            siguiente = input()
        
        elif siguiente == "d":
            cronometro.cronometro(5*60, "Descanso")
            print("""
Si desea comenzar el siguiente pomodoro, introduzca «p».
Si en cambio desea terminar, introduzca «t».""")
            siguiente = input()

        elif siguiente == "dl":
            cronometro.cronometro(15*60, "Descanso")
            print("""
Si desea comenzar el siguiente pomodoro, introduzca «p».
Si en cambio desea terminar, introduzca «t».""")
            siguiente = input()

        else:
            print(
"""La letra que ha introducido no forma parte del intérprete.
Por favor, lea otra vez las instrucciones que le han sido proporcionadas.""")
            siguiente = input()

else:
    argumento = int(argumento)*60   # ahora está en número y en segundos
    cronometro.cronometro(argumento, "Cronómetro")

if argumento == "pomodoro":
    print("Número de pomodoros completados: %i" % pomodoros)