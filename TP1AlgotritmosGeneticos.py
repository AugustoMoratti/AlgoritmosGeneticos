import random
import matplotlib.pyplot as plt

def generacionDeCromosoma(tam):
    a = []
    for i in range(tam):
        a.append(random.randint(0,1))
    return a


def funcion(x):
    coef = (2**30)-1
    a = (x/coef)**2
    return a

def numberToBinario(number):
    binario = []
    while number != 0:
        resto = number % 2
        number = number // 2
        binario.append(resto)
    if len(binario)!=30:
        for i in range(30-len(binario)):
            binario.append(0)
    crom = binario[::-1] #para invertir listas
    return crom

def binarioToNumber(binario): #Convierte una lista de 1 y 0 (binario) a entero
    cromI = binario[::-1]
    decimal = 0
    for i in range(len(cromI)):
        decimal = decimal + cromI[i] * (2**i)
    return decimal


def mutacion(seleccionados, i, tam):
    cromo = seleccionados[i]
    pos = random.randint(0,tam-1)
    if cromo[pos] == 0:
        cromo[pos] = 1
    else :
        cromo[pos] = 0
    return cromo

def crossover(seleccionados, i, tam):
    n = random.randint(0,tam-1)
    #print("n crossover :")
    #print(n)
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1[:n] + elemento2[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2[:n] + elemento1[n:]#devuelve el cromosoma cambiado
    #print(elemento3)
    #print(elemento4)
    return [elemento3, elemento4]

class Miembro:
    def __init__(self, cromosoma, valor, suma):
          self.cromosoma = cromosoma
          self.valor = valor
          self.funcionObjetivo = round(funcion(valor),3)
          self.fitness = round(self.funcionObjetivo/suma,2)

    def __str__(self):
        return f"Cromosoma: {self.cromosoma} Valor: {self.valor} FuncionObj: {self.funcionObjetivo} fitness: {self.fitness} "

class Poblacion:
    def __init__(self, miembros, cromMax, max, min, promedio):
        self.miembros = miembros
        self.crommax = cromMax
        self.max = round(max, 3)
        self.min = round(min, 3)
        self.prom = round(promedio, 3)
        
    def ruleta(self, cantidad):
        roulette = []
        elegidos = [] 
        for j in range(cantidad): 
            cantPos = self.miembros[j].fitness
            for k in range(int(cantPos*100)):
                roulette.append(self.miembros[j].valor)
        #print("RULETA: ",roulette)
        if len(roulette)!=100:
            print("ERROR: CANTIDAD DE POSICIONES DE RULETA ERRONEA")
        for i in range(cantidad):
            pos = random.randint(0,99)
            #print ("elegido: ",roulette[pos])
            val = roulette[pos]
            j = 0
            while self.miembros[j].valor != val:
                j = j + 1
            elegidos.append(self.miembros[j].cromosoma)
        return elegidos
    
    def torneo(self, cantidad):
        elegidos = []
        seleccionados = []
        for i in range(cantidad):
            j = 0
            for j in range(cantidad):
                numAleatorio = random.randint(0,cantidad-1)
                elegidos.append(self.miembros[numAleatorio])
            k = 0
            for k in range(cantidad):
                if k == 0:
                    max = elegidos[0]
                else:
                    if max.funcionObjetivo < elegidos[k].funcionObjetivo :
                        max = elegidos[k]
            seleccionados.append(max)
        return seleccionados


    def mostrar_miembros(self):
        for miembro in self.miembros:
            print(miembro)
        #print('El cromosomas responsable del valor maximo ', self.miembros[self.posmax].funcionObjetivo, ' es ' , self.miembros[self.posmax])
        #print('El cromosomas responsable del valor minimo ', self.miembros[self.posmin].funcionObjetivo, ' es ' , self.miembros[self.posmin])

    def mostrarPoblacion(self, num):
        print(num, "       : ", self.crommax," : ", self.max," : ", self.min," : ", self.prom)

def siguientePoblacion(poblacion, cantMiembros, tamCromo, numCorr) :
    PC = 0.75
    PM = 0.05
    suma = 0
    acumFitness = 0
    fObj = 0
    miembros = []
    cambiados = [] 
    seleccionados = poblacion.ruleta(cantMiembros)
    # print("CROMOSOMAS SELECCIONADOS: ")
    # for i in range(cantMiembros):
    #     print(seleccionados[i])
    for i in range (cantMiembros//2): # la division // devuelve numero entero, mientras que / devuelve flotante
        cross = random.randint(1,100)
        #print("probabilidad de crossover en ",i, " :",cross)
        if cross <= PC*100:
            cambiados.extend(crossover(seleccionados, i, tamCromo)) #arreglo de los nuevos cromosomas
        else :
            arregloProvisorio = [seleccionados[i*2] , seleccionados[(i*2)+1]]
            cambiados.extend(arregloProvisorio)
        #print('COLECCION DE CAMBIADOS ', i, cambiados)
    for j in range(cantMiembros):
        muta = random.randint(1,100)
        #print("probabilidad de mutacion en ",j, " :",muta)
        if muta <= PM*100:
            cambiados[j] = (mutacion(cambiados, j, tamCromo))
    #     print('COLECCION DE CAMBIADOS ', j, cambiados)
    # print(cambiados)
    for k in range(cantMiembros) :
        valor = binarioToNumber(cambiados[k])
        fObj = funcion(valor)
        suma = suma + fObj
        if k == 0 :
            min = fObj
            max = fObj
            posmax = k
        else :
            if min > fObj : 
                min = fObj

            if max < fObj :
                max = fObj
                posmax = k
    for y in range(cantMiembros):
        valor = binarioToNumber(cambiados[y])
        miembros.append(Miembro(cambiados[y], valor, suma))
        acumFitness = acumFitness + miembros[y].fitness
    if acumFitness != 1.00:
        rest = round(1.00 - acumFitness, 2)
        miembros[y].fitness = round(miembros[y].fitness + rest, 2)
    pob = Poblacion(miembros, cambiados[posmax], max, min, suma/cantMiembros) #El promedio es suma/cantMiembros (estaba mal antes, suma/tamCromo)
    minGlobales.append(min)
    maxGlobales.append(max)
    promGlobales.append(suma/cantMiembros)
    # print('Los miembros de la población ', numCorr,' son:') #FALTA AGREGAR EL NUMERO DE LA ITERACION QUE VIENE DE AFUERA
    # pob.mostrar_miembros()
    # print(" POBLACIÓN : CROMOSOMA CORRESPONDIENTE A VALOR MÁXIMO                                                    : MAX    : MIN    : PROM ") 
    pob.mostrarPoblacion(numCorr)
    return pob


def createPoblationInicial(cantMiembros, tamCromo): 
    suma = 0
    cromosomas = []
    miembros = []  
    acumFitness = 0
    rest = 0.00

    for i in range(cantMiembros) : 
        crom = generacionDeCromosoma(tamCromo)
        cromosomas.append(crom)
        valor = binarioToNumber(cromosomas[i])
        fObj = funcion(valor)
        suma = suma + fObj
        if i == 0 :
            min = fObj
            max = fObj
            posmax = i
        else :
            if min > fObj : 
                min = fObj
            if max < fObj :
                max = fObj
                posmax = i
    for y in range(cantMiembros):
        valor = binarioToNumber(cromosomas[y])
        miembros.append(Miembro(cromosomas[y], valor, suma))
        acumFitness = acumFitness + miembros[y].fitness
    if acumFitness != 1.00:
        rest = round(1.00 - acumFitness, 2)
        miembros[y].fitness = round(miembros[y].fitness + rest, 2)
    pob = Poblacion(miembros, cromosomas[posmax], max, min, suma/cantMiembros)
    minGlobales.append(min)
    maxGlobales.append(max)
    promGlobales.append(suma/cantMiembros)
    print('Los miembros de la población inicial son:')
    pob.mostrar_miembros()
    print(" POBLACIÓN : CROMOSOMA CORRESPONDIENTE A VALOR MÁXIMO                                                    : MAX    : MIN    : PROM ") 
    pob.mostrarPoblacion(1)
    return pob

minGlobales = []
maxGlobales = []
promGlobales = []
corridas = 20
population = createPoblationInicial(10,30) #se ingresa numero deseado de integrantes de la población y numero de bits por cromosoma
for c in range(corridas-1):
    population = siguientePoblacion(population,10,30, c+2)

x = list(range(1, corridas + 1))

plt.plot(x, maxGlobales, label='Fitness máximo')
plt.plot(x, minGlobales, label='Fitness mínimo')
plt.plot(x, promGlobales, label='Fitness promedio')

plt.title('Evolución del fitness por iteración')
plt.xlabel('Iteración')
plt.ylabel('Fitness')
plt.ylim(0, 1)  # Escala del eje Y de 0 a 1

plt.legend()  # Muestra la leyenda con las etiquetas
plt.grid(True)  # Opcional: muestra una grilla para facilitar la lectura
plt.tight_layout()
plt.show()

#ALGUNAS FUNCIONES EXPLICADAS

#1)
#random.choice(poblacion, weights=none, k)
    #Parametros:
    # poblacion: la lista de elementos de la cual querés elegir.
    # weights: (opcional) una lista de **pesos numéricos** (o probabilidades relativas). No tienen que sumar 100.
    # k: cuántos elementos querés seleccionar.

#2)
# format(number, ‘05b’)
    #number es el numero que queremos cambiar el formato.
    # ‘05b’ = 05 - indica la cantidad de digitos a tener y b - indica que es binario

#3)
#''.join(str(digito) for digito in lista_binaria)
#int(binario_str, 2)

 #join() es una función de string en Python que se usa 
 # para unir los elementos de una lista (u otra secuencia) en una sola cadena de texto.

 #''.join(...)` une los números como una cadena binaria: `'10110'`.
 #int(..., 2)` convierte esa cadena binaria a entero base 10.


#CROSSOVER PASOS = 
# - Realizar el crossover en la funcion y guardarlos en un arreglo aparte , solo los cromosomas
# - Luego pasarlos a enteros 
# - Realizar la suma de los miembros nuevos
# - Guardar los nuevos como miembros de la poblacion

#CONSULTA =
# Puede pasar que en la poblacion haya un elemento repetido?
# Como puedo mantener siempre la misma cantidad de elementos en la poblacion

    #OPCION PERO CON ELEMENTOS SIN REPETIR
"""
    suma = 0
    miembros = []
    conjunto = list(range(0, 31))  # Conjunto del 0 al 31
    arreglo = random.sample(conjunto, 10)  # Selecciona 10 números sin repetir
    for i in range(10) :
        cromosoma = numberToBinario(arreglo[i])
        valor = arreglo[i]
        suma = suma + arreglo[i]
        if i == 1 :
            min = valor
            max = valor
        if i > 1 :
            if min > valor : 
                min = valor
            if max < valor :
                max = valor
        miembros.append(Miembro(cromosoma, valor, suma))
    p = Poblacion(miembros, max , min)
    p.mostrar_miembros()
    siguientePoblacion(p) #al ponerlo dentro de un bucle controlaremos las iteraciones   
    # Para tener 10 numeros distintos sin repeticion
    """

