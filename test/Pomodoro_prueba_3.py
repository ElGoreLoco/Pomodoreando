import threading
import time

seguir = True
segs = 0
class proceso(threading.Thread):
    def run(self):
        global seguir
        entrada = input()
        if entrada == "p":
            seguir = False
        else:
            proceso().start()

proceso().start()
while seguir:
    print(time.ctime(segs)[14:19])
    time.sleep(1)
    segs += 1
    if segs == 20:
        seguir = False
else:
    print("terminado")
