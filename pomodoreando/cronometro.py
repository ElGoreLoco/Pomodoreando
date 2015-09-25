import time
import pomodoreando.paralelo as paralelo


def cronometro(fin, nombre):
    segs = 0
    paralelo.terminar = False
    paralelo.parar = False

    paralelo.Teclado().start()
    print("El %s ha sido iniciado a %imin." % (nombre.lower(), fin/60))

    while not paralelo.terminar:
        print(time.ctime(segs)[14:19])
        time.sleep(1)
        segs += 1

        while paralelo.parar:
            print("%s pausado." % nombre)
            entrada = input()

            if entrada == "p":
                paralelo.parar = False
                paralelo.Teclado().start()
                print("%s proseguido." % nombre)

            elif entrada == "t":
                paralelo.terminar = True
                paralelo.parar = False

        if segs == fin:
            paralelo.terminar = True

    else:
        print("El %s ha terminado." % nombre.lower())
