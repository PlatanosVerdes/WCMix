import threading
from random import randint                    # Generar un int aleatorio
from time import sleep                        # Esperar
import random                                 # Generación de números aleatorios
from sty import fg, ef, rs                    # Salida colorida

HOMBRES_COUNT_OFFICE = 6                      # Cantidad de hombres en la oficina
MUJERES_COUNT_OFFICE = 6                      # Cantidad de mujeres en la oficina
MAX_PERSONAS = 3                              # Cantidad de personas concurrentes en el baño
MAX_REPEATS_WC = 2                            # Veces que cada persona tiene que ir al baño 

counter_wc_hombres = 0                        # Cantidad de hombres en el baño 
counter_wc_mujeres = 0                        # Cantidad de mujeres en el baño 

mutexHombres = threading.Lock()               # Modificar el contador de los hombres
mutexMujeres = threading.Lock()               # Modificar el contador de las mujeres

SCHombres = threading.Semaphore(MAX_PERSONAS) # Semáforo contador para los hombres
SCMujeres = threading.Semaphore(MAX_PERSONAS) # Semáforo contador para las mujeres

waiting_room = threading.Lock()               # Sala de espera
access_WC = threading.Lock()                  # Acceso al baño 

def prwoman(skk): return fg(201) + f"{skk}" + fg.rs # Print pink string
def prman(skk): return fg.cyan + f"{skk}" + fg.rs   # Print cyan string

class Hombre (threading.Thread):
    
    nombre = ""
    vecesWC = 0
    def __init__(self):
        super().__init__()
        self.nombre = random.choice(list(open("MALE_NAMES", encoding="utf8"))).split("\n")[0]
    
    def presentacion(self):
        print(prman(self.nombre.upper()) + " llega a la oficina")
    
    def trabajar(self):
        print(prman(self.nombre.upper()) + " trabaja")
        sleep(randint(1,5))

    def ir_WC(self):
        global counter_wc_hombres

    #Pre-protocolo 

        # Sala de espera ¿Hay gente en el baño? Lock 
        waiting_room.acquire() 

        #Si es el primer Hombre cogera el genero
        with mutexHombres:
            if(counter_wc_hombres == 0):
                access_WC.acquire()
        
        SCHombres.acquire() # Esperamos hasta que el baño tenga sitio
        # Aumentar contador del baño del genero pertinente variable
        with mutexHombres:
            counter_wc_hombres = counter_wc_hombres + 1
            print(prman(self.nombre.upper()) + f" entra {self.vecesWC+1}/{MAX_REPEATS_WC}. {type(self).__name__} en el baño: {counter_wc_hombres}")
        
        waiting_room.release()      # "Abrir puerta de sala de espera"

    #Protocolo
        # Estamos en el baño
        sleep(randint(1,5)) # Necesidades
            
    #Post-protocolo
        # Evitar display "Hay 4 hombres en el baño"
        with mutexHombres:
            counter_wc_hombres = counter_wc_hombres - 1
        
        # Decrementar contador del baño del genero pertinente variable
        SCHombres.release()
        print(prman(self.nombre.upper()) +" sale del baño")
        # Decrementar contador del baño del genero pertinente Semaforo 
        with mutexHombres:
            if (counter_wc_hombres == 0): # El baño esta vacio para todos
                print(ef.italic + "*** El baño está vacio ***" + rs.italic + "\n")
                access_WC.release()


    def despedida(self):
        print(prman(self.nombre.upper()) +" acaba el trabajo")
        
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
        print(prwoman(self.nombre.upper()) +" llega a la oficina")
    
    def trabajar(self):
        print(prwoman(self.nombre.upper()) +" trabaja")
        sleep(randint(1,5))

    def ir_WC(self):
        global counter_wc_mujeres
        #print(f"{self.nombre.upper()} va al baño {self.vecesWC+1}/{MAX_REPEATS_WC}")
    #Pre-protocolo 

        # Sala de espera ¿Hay gente en el baño? Lock 
        waiting_room.acquire() 

        #Si es el primer Hombre cogera el genero
        with mutexMujeres:
            if(counter_wc_mujeres == 0):
                access_WC.acquire()
        
        SCMujeres.acquire() # Esperamos hasta que el baño tenga sitio
        # Aumentar contador del baño del genero pertinente variable
        with mutexMujeres:
            counter_wc_mujeres = counter_wc_mujeres + 1
            print(prwoman(self.nombre.upper()) + f" entra {self.vecesWC+1}/{MAX_REPEATS_WC}. {type(self).__name__} en el baño: {counter_wc_mujeres}")
        
        waiting_room.release()      # "Abrir puerta de sala de espera"

    #Protocolo
        # Estamos en el baño
        sleep(randint(1,5)) # Necesidades
            
    #Post-protocolo
        # Evitar error de display "hay 4 mujeres en el baño"
        with mutexMujeres:
            counter_wc_mujeres = counter_wc_mujeres - 1
        # Decrementar contador del baño del genero pertinente variable
        SCMujeres.release()
        # Decrementar contador del baño del genero pertinente Semaforo 
        print(prwoman(self.nombre.upper()) +" sale del baño")

        with mutexMujeres:
            if (counter_wc_mujeres == 0): # El baño esta vacio para todos
                print(ef.italic + "*** El baño está vacio ***" + rs.italic + "\n")
                access_WC.release()

    def despedida(self):
        print(prwoman(self.nombre.upper()) +" acaba el trabajo")

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
