#Un semaforo contador hombres
#Un semaforo contador mujeres
#Un semaforo mutex hombres/mujeres

import threading
from random import randint # Generar un int aleatorio
from time import sleep     # Esperar
import random

HOMBRES_COUNT_OFFICE = 6 
MUJERES_COUNT_OFFICE = 6 
MAX_PERSONAS = 3
MAX_REPEATS_WC = 2

COUNTER_WC_HOMBRES = 0
COUNTER_WC_MUJERES = 0

mutexHombres = threading.Lock() # Modificar el contador de los hombres
mutexMujeres = threading.Lock() # Modificar el contador de las mujeres

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
        print("Hola")

    def despedida(self):
        print(f"{self.nombre.upper()} acaba el trabajo")
        
    def run(self):
        self.presentacion()
        self.trabajar()
        while(self.vecesWC != MAX_REPEATS_WC): # Mientras tenga que ir al baño
            self.ir_WC()
            self.trabajar()
            self.vecesWC = self.vecesWC + 1
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
        print("Hola")

    def despedida(self):
        print(f"{self.nombre.upper()} acaba el trabajo")

    def run(self):
        self.presentacion()
        self.trabajar()
        while(self.vecesWC != MAX_REPEATS_WC): # Mientras tenga que ir al baño
            self.ir_WC()
            self.trabajar()
            self.vecesWC = self.vecesWC + 1
        self.despedida()

def main():
    personas = []
    
    # Generacion de procesos 
    for i in range(HOMBRES_COUNT_OFFICE):
        personas.append(Hombre())
    
    for i in range(MUJERES_COUNT_OFFICE):
        personas.append(Mujer())

    # Randomizamos el "orden" de entrada
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
