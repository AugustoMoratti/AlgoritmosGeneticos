import random
import matplotlib.pyplot as plt

def generacionDeCromosoma(tam):
    a = []
    for i in range(tam):
        a.append(random.randint(0,1))
    return a

def binarioToNumber(binario): #Convierte una lista de 1 y 0 (binario) a entero
    cromI = binario[::-1]
    decimal = 0
    for i in range(len(cromI)):
        decimal = decimal + cromI[i] * (2**i)
    return decimal

def mutacion(cromo, tam):
    pos = random.randint(0,tam-1)
    print("Pos cambiada = ", pos)
    if cromo[pos] == 0:
        cromo[pos] = 1
    else :
        cromo[pos] = 0
    return cromo

def crossover(seleccionados, i, tam):
    n = random.randint(0,tam-1)
    print("Pos corte = ", n)
    #print("n crossover :")
    #print(n)
    elemento1 = seleccionados[i*2]
    elemento2 = seleccionados[(i*2)+1]
    elemento3 = elemento1[:n] + elemento2[n:]#devuelve el cromosoma cambiado
    elemento4 = elemento2[:n] + elemento1[n:]#devuelve el cromosoma cambiado
    #print(elemento3)
    #print(elemento4)
    return [elemento3, elemento4]

cromosomas = []
i = 0
j = 0
k = 0
t = 0
mutados = []
cambiados = []
for i in range(6):
    crom = generacionDeCromosoma(5)
    cromosomas.append(crom)
print("Nueva poblacion")
for j in range(6):
    print(cromosomas[j], binarioToNumber(cromosomas[j]))
print(" ")
print("Poblacion mutada")
for k in range(6):
    crom = mutacion(cromosomas[k], 5)
    mutados.append(crom)
    print(mutados[k], binarioToNumber(mutados[k]))
print(" ")
print("Poblacion pasada por crossover")
for w in range(3):
    cambiados.extend(crossover(mutados, w, 5))
for t in range(6):
    print(cambiados[t])

    

    