import threading
import time


class Teclado(threading.Thread):
    def run(self):
        global seguir
        entrada = input()

        if entrada == "p":
            seguir = False
        else:
            Teclado().start()

seguir = True
segs = 0

Teclado().start()
print("Cronómetro iniciado.")
while seguir:
    print(time.ctime(segs)[14:19])
    time.sleep(1)
    segs += 1
else:
    print("Cronómetro terminado.")
