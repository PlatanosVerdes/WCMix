#Un semaforo contador hombres
#Un semaforo contador mujeres
#Un semaforo mutex hombres/mujeres

import threading
from random import randint # generar un int aleatorio
from time import sleep     # esperar
import random

HOMBRES_COUNT = 6 # Consumers
MUJERES_COUNT = 6 # Consumers
MAX_PERSONAS = 3
MAX_REPEATS_WC = 2

WC = [] #Buffer

mutex = threading.Lock() #Semaforo de exclusion mutua
WC_noLleno = threading.Semaphore(MAX_PERSONAS) #Semaforo contador de personas dentro

class Hombre (threading.Thread):
    
    nombre = ""
    vecesWC = 0
    def __init__(self):
        super().__init__()
        self.nombre = random.choice(list(open("MALE_NAMES", encoding="utf8"))).split("\n")[0]
    
    def presentacion(self):
        print(f"{self.nombre.upper()} llega a la oficina")
    
    def trabajar(self):
        print(f"{self.nombre.upper()} trabaja")
        sleep(randint(1,5))

    def ir_WC(self):
        global WC

        WC_noLleno.acquire()
        with mutex:
            WC.append(self)
        self.vecesWC = self.vecesWC + 1

        print(f"{self.nombre.upper()} va al baño {self.vecesWC}/2")
        sleep(randint(1,2))
        print(f"{self.nombre.upper()} sale del baño")
        
        with mutex:
            WC.pop(WC.index(self))
            print(len(WC))
            if len(WC) == 0:
                print("*** El baño esta vacio ***")

        WC_noLleno.release()
        
    def despedida(self):
        print(f"{self.nombre.upper()} acaba el trabajo")
        
    def run(self):
        self.presentacion()
        self.trabajar()
        self.ir_WC()
        self.trabajar()
        self.ir_WC()
        self.trabajar()
        self.despedida()


class Mujer (threading.Thread):
    
    nombre = ""
    vecesWC = 0
    def __init__(self):
        super().__init__()
        self.nombre = random.choice(list(open("FEMALE_NAMES", encoding="utf8"))).split("\n")[0]

    def presentacion(self):
        print(f"{self.nombre.upper()} llega a la oficina")
    
    def trabajar(self):
        print(f"{self.nombre.upper()} trabaja")
        sleep(randint(1,5))

    def ir_WC(self):
        global WC

        WC_noLleno.acquire()

        with mutex:
            WC.append(self)

        self.vecesWC = self.vecesWC + 1
        print(f"{self.nombre.upper()} va al baño {self.vecesWC}/2")
        sleep(randint(1,2))
        print(f"{self.nombre.upper()} sale del baño")
        
        with mutex:
            WC.pop(WC.index(self))
            print(len(WC))
            if len(WC) == 0:
                print("*** El baño esta vacio ***")

        WC_noLleno.release()
        
    def despedida(self):
        print(f"{self.nombre.upper()} acaba el trabajo")

    def run(self):
        self.presentacion()
        self.trabajar()
        self.ir_WC()
        self.trabajar()
        self.ir_WC()
        self.trabajar()
        self.despedida()


def main():
    personas = []
    
    # Generacion de procesos 
    for i in range(HOMBRES_COUNT):
        personas.append(Hombre())
    
    for i in range(MUJERES_COUNT):
        personas.append(Mujer())

    random.shuffle(personas)

    # Iniciamos todos los procesos
    for i in personas:
        i.start()

    # Esperamos que todos acaben
    for i in personas:
        i.join()

    print("End")
    

if __name__ == "__main__":
    main()

# []