import threading

terminar = False
parar = False


class Teclado(threading.Thread):
    def run(self):
        global terminar
        global parar
        self.entrada = input()

        if self.entrada == "t":
            terminar = True

        elif self.entrada == "p":
            parar = True

        else:
            self.run()
