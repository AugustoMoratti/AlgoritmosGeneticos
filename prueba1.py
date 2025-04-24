import random

def generacionDeCromosoma(tam):
    a = []
    for i in range(tam):
        a.append(random.randint(0,1))
    return a

# def numBetween0_1() :
#     a = random.randint(0,1)
#     return a

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

def mutacion():
    ...

def crossover(seleccionados, i):
    n = random.randint(1,5)
    print("n crossover :")
    print(n)
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1.cromosoma[:n] + elemento2.cromosoma[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2.cromosoma[:n] + elemento1.cromosoma[n:]#devuelve el cromosoma cambiado
    print(elemento3)
    print(elemento4)
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
        seleccionados = random.choices(
            self.miembros, 
            weights = [e.fitness*100 for e in self.miembros],  #recorre miembro por miembro y le asigna un porcentaje
            k = cantidad 
        )
        return seleccionados
    #Vector otra forma, preguntar si es valida esta forma 

    # Funcion del random que elige al azar entre una lista de elementos, tomando
    # en cuenta un peso especifico y la cantidad que debe seleccionar
    def mostrar_miembros(self):
        for miembro in self.miembros:
            print(miembro)
        print('El cromosomas responsable del valor maximo ', self.miembros[self.posmax].funcionObjetivo, ' es ' , self.miembros[self.posmax])
        print('El cromosomas responsable del valor minimo ', self.miembros[self.posmin].funcionObjetivo, ' es ' , self.miembros[self.posmin])


def siguientePoblacion(poblacion, cantidadMiembros) :
    PC = 0.75
    PM = 0.05
    suma = 0
    miembros = []
    cambiados = [] #Arreglo de 4 cromosomas [1, 0 , 0, 1, 0]
    #seleccion =  4 #cantidad de miembros seleccionados para formar la proxima poblacion
    seleccionados = poblacion.ruleta(cantidadMiembros)
    print("seleccionados : ")
    for s in seleccionados :
        print(s)
    for i in range (cantidadMiembros//2): #valores posibles de i 0 y 1
        a = random.randint(1,100)
        print("probabilidad de crossover :",a)
        if a <= PC*100:
            cambiados.extend(crossover(seleccionados, i)) #arreglo de los nuevos cromosomas
            print(cambiados)
        else :
            arregloProvisorio = [seleccionados[i*2].cromosoma , seleccionados[(i*2)+1].cromosoma]
            cambiados.extend(arregloProvisorio)
    #for i in range(cantidadMiembros):
        #a = random.randint(1,100)
        #if a <= PM*100:
            #cambiados.extend(mutacion(cambiados, i))
        #else:
            #cambiados.extend(seleccionados)
    for j in range(cantidadMiembros) :
        valor = binarioToNumber(cambiados[j])
        suma = suma + funcion(valor)
    for y in range(cantidadMiembros):
        cromosoma = cambiados[y]
        valor = binarioToNumber(cambiados[y])
        if y == 0 :
            min = valor
            max = valor
        if y >= 1 :
            if min > valor : 
                min = valor
            if max < valor :
                max = valor
        miembros.append(Miembro(cromosoma, valor, suma))
    p = Poblacion(miembros, posmax , posmin)
    p.mostrar_miembros()
            #Devuelve los modificados  
            # RECORDAR = Una vez terminado el bucle establecemos la suma y 
            # lo actualizamos en la nueva poblacion

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
    print(y)
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

pob = createPoblationInicial(10,30) #se ingresa numero deseado de integrantes de la población y numero de bits por cromosoma
#siguientePoblacion(pob,10)

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