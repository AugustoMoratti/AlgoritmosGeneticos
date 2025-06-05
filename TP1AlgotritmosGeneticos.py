import random
import matplotlib.pyplot as plt
from openpyxl import Workbook
import time


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
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1[:n] + elemento2[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2[:n] + elemento1[n:]#devuelve el cromosoma cambiado
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
            if int(cantPos*100) == 0:
                roulette.append(self.miembros[j].valor)   
        tam = len(roulette)
        for i in range(cantidad):
            pos = random.randint(0,tam-1)
            #print ("elegido: ",roulette[pos])
            val = roulette[pos]
            j = 0
            while self.miembros[j].valor != val:
                j = j + 1
            elegidos.append(self.miembros[j].cromosoma)
        return elegidos
    
    def torneo(self, cantidad):
        seleccionados = []
        for i in range(cantidad):
            elegidos = []
            for j in range(int(cantidad*0.4)):
                numAleatorio = random.randint(0,cantidad-1)
                elegidos.append(self.miembros[numAleatorio])
            for k in range(int(cantidad*0.4)):
                if k == 0:
                    max = elegidos[0]
                else:
                    if max.funcionObjetivo < elegidos[k].funcionObjetivo :
                        max = elegidos[k]
            seleccionados.append(max.cromosoma)
        return seleccionados
    
    def elitismo(self, cant):
        maximos = []
        posmax = -1
        for j in range(2):
            for i in range (cant):
                if i == posmax :
                    continue
                fObj = self.miembros[i].funcionObjetivo
                if i == 0 :
                    posmax1 = i
                    max1 = fObj
                else :
                    if (max1 < fObj):
                        posmax1 = i
                        max1 = fObj
            posmax = posmax1
            maximos.append(self.miembros[posmax].cromosoma)
        return maximos


    def mostrar_miembros(self):
        for miembro in self.miembros:
            print(miembro)

    def mostrarPoblacion(self, num):
        linea = [num, str(self.crommax), self.max, self.min, self.prom]
        ws.append(linea)
        print(num, "       : ", self.crommax," : ", self.max," : ", self.min," : ", self.prom)

def siguientePoblacion(poblacion, cantMiembros, tamCromo, numCorr, metodo) :
    PC = 0.75
    PM = 0.05
    suma = 0
    fObj = 0
    miembros = []
    cambiados = [] 
    if metodo == "a":
        seleccionados = poblacion.ruleta(cantMiembros)
    elif metodo == "b":
        seleccionados = poblacion.torneo(cantMiembros)
    elif metodo == "c":
        cambiados.extend(poblacion.elitismo(cantMiembros))
        cantMiembros = cantMiembros - 2
        seleccionados = poblacion.ruleta(cantMiembros)
    for i in range (cantMiembros//2): # la division // devuelve numero entero, mientras que / devuelve flotante
        cross = random.randint(1,100)
        if cross <= PC*100:
            crossoverAplied = crossover(seleccionados, i, tamCromo)
            cambiados.extend(crossoverAplied) #arreglo de los nuevos cromosomas
        else :
            arregloProvisorio = [seleccionados[i*2] , seleccionados[(i*2)+1]]
            cambiados.extend(arregloProvisorio)
    for j in range(cantMiembros):
        muta = random.randint(1,100)
        if muta <= PM*100:
            cambiados[j] = (mutacion(cambiados, j, tamCromo))
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
    pob = Poblacion(miembros, cambiados[posmax], max, min, suma/cantMiembros) #El promedio es suma/cantMiembros (estaba mal antes, suma/tamCromo)
    minGlobales.append(min)
    maxGlobales.append(max)
    promGlobales.append(suma/cantMiembros)
    pob.mostrarPoblacion(numCorr)
    return pob


def createPoblationInicial(cantMiembros, tamCromo): 
    suma = 0
    cromosomas = []
    miembros = []  
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
    pob = Poblacion(miembros, cromosomas[posmax], max, min, suma/cantMiembros)
    minGlobales.append(min)
    maxGlobales.append(max)
    promGlobales.append(suma/cantMiembros)
    print(" POBLACIÓN : CROMOSOMA CORRESPONDIENTE A VALOR MÁXIMO                                                    : MAX    : MIN    : PROM ") 
    pob.mostrarPoblacion(1)
    return pob


opcion = " "
while opcion != "s" :
    minGlobales = []
    maxGlobales = []
    promGlobales = []
    print("=" * 40)
    print("|{:^38}|".format("Elija un método de selección"))
    print("=" * 40)
    print("| {:<37}|".format("a) Ruleta"))
    print("| {:<37}|".format("b) Torneo"))
    print("| {:<37}|".format("c) Elitismo"))
    print("| {:<37}|".format("s) Salir"))
    print("=" * 40)
    

    opcion = input("Seleccione una opción (a, b, c, s): ").lower()
    while opcion not in ['a', 'b', 'c', 's']:
        opcion = input("Opción inválida. Intente de nuevo (a, b, c, s): ").lower()
    if opcion != "s":

        try:
            corridas = int(input("Ingresá la cantidad de iteraciones: "))
        except ValueError:
            print("Eso no es un número entero válido.")
        
        #Creación de excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos de población"
        ws.append(["POBLACIÓN", "CROMOSOMA CORRESPONDIENTE A VALOR MÁXIMO", "MÁXIMO", "MÍNIMO", "PROMEDIO"])
        ###

        population = createPoblationInicial(10,30) 

        for c in range(corridas-1):
            population = siguientePoblacion(population,10,30, c+2, opcion)

        wb.save(f"datos_poblacion_{int(time.time())}.xlsx")

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
        plt.savefig(f"grafica_datos_poblacion_metodo{str(opcion)}_{int(time.time())}.png")  #PARA GUARDAR
        plt.show()
if opcion == "s":
    print("Nos vemos la próxima!")



