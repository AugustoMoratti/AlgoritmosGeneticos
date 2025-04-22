import random

def numBetween0_1() :
    a = random.randint(0,1)
    return a

def funcion(x):
    a = x*x
    return a

def numberToBinario(number):
    binario = format(number, '05b') #transforma a binario, 05 indica la cantidad de digitos en binario y la b que pasa a binario
    return [int(digito) for digito in binario]

def binarioToNumber(binario): #Convierte una lista de 1 y 0 (binario) a entero
    binario_str = ''.join(str(digito) for digito in binario)  #Es lo que se pondra entre los elementos
    return int(binario_str, 2)

def mutacion():
    ...

def crossover(seleccionados, i):
    n = random.randint(1,5)
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1.cromosoma[:n] + elemento2.cromosoma[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2.cromosoma[:n] + elemento1.cromosoma[n:]#devuelve el cromosoma cambiado
    return [elemento3, elemento4]
    
    
class Miembro:
    def __init__(self, cromosoma, valor, suma):
          self.cromosoma = cromosoma
          self.valor = valor
          self.funcionObjetivo = funcion(valor)
          self.fitness = valor/suma

    def __str__(self):
        return f"Cromosoma: {self.cromosoma} Valor: {self.valor} FuncionObj: {self.funcionObjetivo} fitness: {self.fitness} "

class Poblacion:
    def __init__(self, miembros, max, min):
        self.miembros = miembros
        self.max = max
        self.min = min

    def ruleta(self, cantidad):
        seleccionados = random.choices(
            self.miembros, 
            weights = [e.fitness*100 for e in self.miembros],
            k = cantidad
        )
        return seleccionados
    # Funcion del random que elige al azar entre una lista de elementos, tomando
    # en cuenta un peso especifico y la cantidad que debe seleccionar

    def mostrar_miembros(self):
        for miembro in self.miembros:
            print(miembro)


def siguientePoblacion(poblacion, cantidadMiembros) :
    PC = 0.90
    PM = 0.001
    j = 0
    suma = 0
    miembros = []
    cambiados = [] #Arreglo de 4 miembros nuevos
    seleccion =  4 #cantidad de miembros seleccionados para formar la proxima poblacion
    seleccionados = poblacion.ruleta(seleccion)
    print("seleccionados : ")
    for s in seleccionados :
        print(s)
    
    #CROSSOVER
    for i in range (seleccion//2): #valores posibles de i 0 y 1
        a = random.randint(1,100)
        if a <= PC*100:
            cambiados.extend(crossover(poblacion, seleccionados, i)) #arreglo de los nuevos cromosomas
            print(cambiados)
    
    #MUTACION
    for i in cambiados :
        a = random.randint(1,100)
        if a <= PM*100:
            cambiados.extend(mutacion(cambiados, i)) #arreglo de los nuevos cromosomas
            print(cambiados)
    
    #ARMADO DE NUEVA POBLACION
    while j < cantidadMiembros :
      valor = binarioToNumber(cambiados[j])
      suma = suma + valor
      j = j + 1
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
    poblacion = Poblacion(miembros, max , min)
    poblacion.mostrar_miembros()


def createPoblationInicial():
    a = []
    i = 0
    cantidadMiembros = 4
    suma = 0
    miembros = []
    min = int
    max = int
    while i < cantidadMiembros :
      a.append(random.randint(0 , 31))
      suma = suma + a[i]
      i = i + 1
    for y in range(cantidadMiembros):
        cromosoma = numberToBinario(a[y])
        valor = a[y]
        if y == 0 :
            min = valor
            max = valor
        if y >= 1 :
            if min > valor : 
                min = valor
            if max < valor :
                max = valor
        miembros.append(Miembro(cromosoma, valor, suma))
    p = Poblacion(miembros, max , min)
    p.mostrar_miembros()
    siguientePoblacion(p, cantidadMiembros) #al ponerlo dentro de un bucle controlaremos las iteraciones      

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

createPoblationInicial()

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