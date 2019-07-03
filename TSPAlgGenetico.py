import random
from random import randint
import math
import numpy as np
import operator

import matplotlib.pyplot as plt

x_max = 300
y_max = 300

class Ciudad:
    def __init__ (self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Recorrido:
    def __init__ (self, secuencia, matriz_ady):
        self.secuencia = secuencia
        self.aptitud = self.CalcAptitud(self.secuencia, matriz_ady)

    def CalcAptitud(self, recor, matriz_ady):         
        dist = 0.0
        for i in range (0, len(recor)-1):
            dist += matriz_ady[recor[i]][recor[i+1]]
        #print ("X ",matriz_ady[len(recor)-1][recor[0]])
        dist += matriz_ady[recor[len(recor)-1]][recor[0]]
        return dist
            

num_ciudades = int(input("Ingrese numero de ciudades"))
citys = []
poblacion = []   #poblacion de recorridos
poblacion_mem = []
pool = []       #pool de reproduccion
calculada = []
calculada_mem = []
lista_x =[]
lista_y =[]
pesimo =[] #recorridos que no deben volver a usarse
padre = np.empty([num_ciudades], dtype = int)

#Generacion x,y ciudades
for i in range(0, num_ciudades):
    x = random.random() * x_max
    y = random.random() * y_max
    c = Ciudad(i, x, y)
    citys.append(c)

#Generacion matriz adyacencia ponderada
m_ady = np.zeros((num_ciudades,num_ciudades), dtype=float)

for i in range(0, num_ciudades):
    for j in range(i+1, num_ciudades):
        dist = math.sqrt(pow(citys[i].x - citys[j].x,2) +
         pow(citys[i].y - citys[j].y,2))
        m_ady[i][j] = m_ady[j][i] = dist

#Generacion poblacion inicial
#recorrido basico padre = 0,1,2,3...
padre = np.empty([num_ciudades], dtype = int)
for i in range(0,num_ciudades):
    padre[i] = i

#genero mutaciones de padre e inserto en poblacion inicial
def PoblacionInicial(size_pobla):
    for i in range(0,size_pobla):
        ar = np.array(padre, copy = True)
        np.random.shuffle(ar)
        R = Recorrido(ar, m_ady)
        poblacion.append(R)
        poblacion_mem.append(R)

#Funcion para ordenar la poblacion por aptitud
def Ranking (poblacion):
    poblacion.sort(key = operator.attrgetter('aptitud'))

#Funcion para conservar poblacion con peores valores
def Memetico (poblacion):
    pesimo.append(poblacion[-memetico_size])

#Cruzamiento a partir de dos padres
def Cruzamiento (padre, madre):
    cad_padre = []
    cad_madre = []

    hijo = np.empty([num_ciudades], dtype = int)
    mascara = np.zeros([num_ciudades], dtype = bool)

    gen1 = randint(0, num_ciudades-1)
    gen2 = randint(0, num_ciudades-1)

    inicio = min(gen1,gen2)
    fin = max(gen1,gen2)

    for i in range(inicio,fin):
        cad_padre.append(padre[i])
        mascara[i] = 1
    
    for item in madre:
        if not item in cad_padre:
            cad_madre.append(item)

    i_m = 0
    i_p = 0
    for i in range(0,num_ciudades):    
        if mascara[i]:
            hijo[i] = cad_padre[i_p]
            i_p+=1
        else:
            hijo[i] = cad_madre[i_m]
            i_m+=1
    return hijo

#Generacion de pool para Reproduccion
def GenPool (poblacion):
    for i in range(0, pool_size+1):
        pool.append(poblacion[i])

#Mutacion
def Mutacion(poblacion):
    for i in range(0,mutacion_size):
        especimen = random.choice(poblacion)
        gen1 = randint(0, num_ciudades-1)
        gen2 = randint(0, num_ciudades-1)
        especimen.secuencia[gen1], especimen.secuencia[gen2] = \
            especimen.secuencia[gen2], especimen.secuencia[gen1]


#Creacion de la siguiente generacion de la poblacion
def Generacion (poblacion):
    #Conservar poblacion elite y elegir padre y madre desde pool
    for i in range(elitism_size, size_pobla):
        while (True):
            candidato = Recorrido (Cruzamiento(random.choice(pool).secuencia,
            random.choice(pool).secuencia), m_ady)
            try :
                pesimo.index(candidato)
            except:
                poblacion[i] = candidato
                #print("No Hallado")
                break

def AlgGenetico():
    Ranking(poblacion)
    for i in range(0,num_generaciones):   
        GenPool(poblacion)
        Generacion(poblacion)
        #Mutacion(poblacion)
        Ranking(poblacion)
        calculada.append(poblacion[0].aptitud)
        

def AlgMemetico():
    Ranking(poblacion_mem)
    for i in range(0,num_generaciones):   
        GenPool(poblacion_mem)
        Generacion(poblacion_mem)
        Mutacion(poblacion_mem)
        Ranking(poblacion_mem)
        calculada_mem.append(poblacion_mem[0].aptitud)
        Memetico(poblacion_mem)
    

def PuntosRecorrido(camino, color):
    for i in range(0,len(camino)-1):
        x1 = citys[camino[i]].x
        y1 = citys[camino[i]].y
        x2 = citys[camino[i+1]].x
        y2 = citys[camino[i+1]].y
        plt.plot([x1,x2],[y1,y2], color)
    x1 = citys[camino[len(camino)-1]].x
    y1 = citys[camino[len(camino)-1]].y
    x2 = citys[camino[0]].x
    y2 = citys[camino[0]].y
    plt.plot([x1,x2],[y1,y2], color)

def Ploteo(calculada, pob, titulo):
    plt.title(titulo)
    plt.plot(calculada)
    plt.show()
    for i in range(0, num_ciudades):
        lista_x.append(citys[i].x)
        lista_y.append(citys[i].y)
    plt.plot(lista_x,lista_y, 'ro')
    for i in range(len(lista_x)):
        x, y = lista_x[i], lista_y[i]
        plt.annotate(xy=(x, y), s="{0}".format(citys[i].id))
    PuntosRecorrido(pob[0].secuencia, 'k-')
    plt.title(titulo)
    plt.show()
    lista_x.clear()
    lista_y.clear()

## main ##
while (True):
    
    size_pobla = int(input("Ingrese numero de poblacion: "))
    num_generaciones = int(input("Ingrese numero de generaciones: "))

    elitism_pc = 0.2 #porcentaje de especimenes elite de poblacion
    pool_pc = 0.3 #porcentaje de especimenes para reproduccion
    mutacion_pc = 0.01 #porcentaje de especimenes para mutar
    memetico_pc = 0.1

    elitism_size = int(size_pobla * elitism_pc) #numero de especimenes
    pool_size = int(size_pobla * pool_pc)       #elitismo y reproduccion
    mutacion_size = int(size_pobla* mutacion_pc)
    memetico_size = int(size_pobla* memetico_pc)

    PoblacionInicial(size_pobla)
    AlgGenetico()
    AlgMemetico()
    #Ranking(poblacion)
    print ("Recorrido: ", poblacion[0].secuencia)
    print ("Distancia recorrida: ", poblacion[0].aptitud)
    
    print ("Distancia recorrida memetico: ", poblacion_mem[0].aptitud)

    Ploteo(calculada, poblacion, "Algoritmo Genetico")
    Ploteo(calculada_mem, poblacion_mem, "Algoritmo Memetico")
    poblacion.clear()
    poblacion_mem.clear()
    calculada_mem.clear()
    calculada.clear()
    lista_x.clear()
    lista_y.clear()
    pool.clear()








