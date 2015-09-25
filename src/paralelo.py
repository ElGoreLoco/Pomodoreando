import threading

terminar = False
parar = False


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
