import threading
import time


class Teclado(threading.Thread):
    def run(self):
        global terminar
        global parar
        entrada = input()

        if entrada == "t":
            terminar = True
        elif entrada == "p":
            parar = True
        else:
            Teclado().start()

terminar = False
parar = False
segs = 0

Teclado().start()

print("Cronómetro iniciado.")
while not terminar:
    print(time.ctime(segs)[14:19])
    time.sleep(1)
    segs += 1
    while parar:
        print("Cronómetro pausado.")
        entrada = input()
        if entrada == "p":
            parar = False
            Teclado().start()
            print("Cronómetro proseguido.")
        elif entrada == "t":
            terminar = True
            parar = False
else:
    print("Cronómetro terminado.")
