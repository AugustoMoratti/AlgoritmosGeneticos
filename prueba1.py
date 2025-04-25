import random

def generacionDeCromosoma(tam):
    a = []
    for i in range(tam):
        a.append(random.randint(0,1))
    return a


def funcion(x):
    coef = 2**30-1
    a = (x/coef)**2
    return a

def numberToBinario(number):
    binario = format(number, '30b') #transforma a binario, 05 indica la cantidad de digitos en binario y la b que pasa a binario
    return [int(digito) for digito in binario]

def binarioToNumber(binario): #Convierte una lista de 1 y 0 (binario) a entero
    binario_str = ''.join(str(digito) for digito in binario)  #Es lo que se pondra entre los elementos
    return int(binario_str, 2)

def torneo(iteraciones, poblacion):
    ...
    #devolver un arreglo de la cantidad especificada de miembros

def mutacion(seleccionados, i, tam):
    cromo = seleccionados[i]
    for j in range(tam):
        if cromo[j] == 0:
            cromo[j] = 1
        else :
            cromo[j] = 0


def crossover(seleccionados, i):
    n = random.randint(0,29)
    print("n crossover :")
    print(n)
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1.cromosoma[:n] + elemento2.cromosoma[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2.cromosoma[:n] + elemento1.cromosoma[n:]#devuelve el cromosoma cambiado
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
    def __init__(self, miembros, posmax, posmin):
        self.miembros = miembros
        self.posmax = posmax
        self.posmin = posmin

    def ruleta(self, cantidad):
        roulette = []
        elegidos = [] 
        for j in range(cantidad): 
            cantPos = self.miembros[j].fitness
            for k in range(int(cantPos*100)):
                roulette.append(self.miembros[j].valor)
        # for a in range(100):
        #     print(a+1, " : ", roulette[a])    para ver ruleta
        if len(roulette)!=100:
            print("ERROR: CANTIDAD DE POSICIONES DE RULETA ERRONEA")
        for i in range(cantidad):
            pos = random.randint(0,99)
            #print (pos)
            val = roulette[pos]
            j = 0
            while self.miembros[j].valor != val:
                j = j + 1
            elegidos.append(self.miembros[j])
        return elegidos


    def mostrar_miembros(self):
        for miembro in self.miembros:
            print(miembro)
        print('El cromosomas responsable del valor maximo ', self.miembros[self.posmax].funcionObjetivo, ' es ' , self.miembros[self.posmax])
        print('El cromosomas responsable del valor minimo ', self.miembros[self.posmin].funcionObjetivo, ' es ' , self.miembros[self.posmin])


def siguientePoblacion(poblacion, cantMiembros, tamCromo) :
    PC = 0.75
    PM = 0.05
    suma = 0
    acumFitness = 0
    miembros = []
    cambiados = [] 
    seleccionados = poblacion.ruleta(cantMiembros)
    # print("seleccionados : ")
    # for s in seleccionados :
    #     print(s)
    for i in range (cantMiembros//2): #valores posibles de i 0 y 1
        cross = random.randint(1,100)
        print("probabilidad de crossover :",cross)
        if cross <= PC*100:
            cambiados.extend(crossover(seleccionados, i)) #arreglo de los nuevos cromosomas
        else :
            arregloProvisorio = [seleccionados[i*2].cromosoma , seleccionados[(i*2)+1].cromosoma]
            cambiados.extend(arregloProvisorio)
    for i in range(cantMiembros):
        muta = random.randint(1,100)
        if muta <= PM*100:
            cambiados[i] = (mutacion(cambiados, i, tamCromo))
    for i in range(cantMiembros) :
        valor = binarioToNumber(cambiados[i])
        fObj = funcion(valor)
        suma = suma + fObj
        if i == 0 :
            min = fObj
            posmin = i
            max = fObj
            posmax = i
        else :
            if min > fObj : 
                min = fObj
                posmin = i
            if max < fObj :
                max = fObj
                posmax = i
    for y in range(cantMiembros):
        valor = binarioToNumber(cambiados[y])
        miembros.append(Miembro(cambiados[y], valor, suma))
        acumFitness = acumFitness + miembros[y].fitness
    if acumFitness != 1.00:
        rest = round(1.00 - acumFitness, 2)
        miembros[y].fitness = round(miembros[y].fitness + rest, 2)
    pob = Poblacion(miembros, posmax , posmin)
    print('Los miembros de la población y son:') #FALTA AGREGAR EL NUMERO DE LA ITERACION QUE VIENE DE AFUERA
    pob.mostrar_miembros()
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
            posmin = i
            max = fObj
            posmax = i
        else :
            if min > fObj : 
                min = fObj
                posmin = i
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
    pob0 = Poblacion(miembros, posmax , posmin)
    print('Los miembros de la población inicial son:')
    pob0.mostrar_miembros()
    return pob0
    #siguientePoblacion(p,cantMiembros)
    #al ponerlo dentro de un bucle controlaremos las iteraciones / ver donde ponerlo 

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

population = createPoblationInicial(10,30) #se ingresa numero deseado de integrantes de la población y numero de bits por cromosoma

population = siguientePoblacion(population,10,30)

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