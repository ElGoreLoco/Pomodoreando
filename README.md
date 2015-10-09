Pomodoreando
============
## Introducción
Pomodoreando es un programa pensado para manejar tus pomodoros de una manera
rápida y sencilla.
Además de su función de control de pomodoros, puedes utilizarlo como un
cronómetro normal.

## Instalación
De momento no he creado ningún paquete compilado para ninguna distribución,
pero por ahora puedes instalarlo desde el código fuente.
Para instalarlo simplemente muevete al sitio en el que tienes el código y
ejecuta el siguiente comando en la terminal:
```sudo python3 setup.py install```
Ya deberías tener instalado el programa. Ahora puedes ejecutar `pomodoreando`
en la terminal.

## Instrucciones de uso
El funcionamiento del programa es muy sencillo: ejecuta `pomodoreando <tiempo>`,
y sustituye `<tiempo>` por el número de minutos que quieres que cuente el
cronómetro, o por `pomodoro`, que hará que empiece un ciclo de 25 y 5 minutos.

Cuando esté el cronómetro corriendo puedes escribir `p` y pulsar `<ENTER>`
para parar el cronómetro, y hacer lo mismo otra vez para proseguirlo.

Si quieres terminar el cronómetro escribe `t` y pulsa `<ENTER>`.
