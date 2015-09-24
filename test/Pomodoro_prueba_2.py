import threading
from time import sleep

global seguir
seguir = True
segs = 0
class proceso(threading.Thread):
    def run(self):
        print("iniciado proceso paralelo")
        print(input())
        proceso().start()
        """
        entrada = input()
        if entrada == "p":
            print(entrada + " cacaaaaaa")
            seguir = False
        """

proceso().start()
while seguir:
    print(segs)
    sleep(1)
    segs += 1
    if segs == 20:
        seguir = False
else:
    print("terminado")
