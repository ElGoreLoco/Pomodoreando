from time import sleep
correr = True
segs = 10
while correr:
    print(segs)
    sleep(1)
    segs += 1
    if segs == 15:
        correr = False

else:
    print("terminado")
