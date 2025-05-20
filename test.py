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
    print("Pos cambiada", pos)
    if cromo[pos] == 0:
        cromo[pos] = 1
    else :
        cromo[pos] = 0
    return cromo

cromosomas = []
i = 0
j = 0
k = 0
mutados = []
for i in range(3):
    crom = generacionDeCromosoma(10)
    cromosomas.append(crom)
print("Nueva poblacion")
for j in range(3):
    print(cromosomas[j], binarioToNumber(cromosomas[j]))
print(" ")
print("Poblacion mutada")
for k in range(3):
    crom = mutacion(cromosomas[k], 10)
    mutados.append(crom)
    print(mutados[k], binarioToNumber(mutados[k]))
    

    