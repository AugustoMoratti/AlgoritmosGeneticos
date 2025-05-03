#crom = [1,1,1,0,0,1,0,1,0,0,0,1,0,1,0,1,0]

# cromI = crom[::-1]
# decimal = 0
# for i in range(len(cromI)):
#     decimal = decimal + cromI[i] * (2**i)
# print(decimal)

decimal = 11520
binario = []
while decimal != 0:
    resto = decimal % 2
    decimal = decimal // 2
    binario.append(resto)
if len(binario)!=30:
    for i in range(30-len(binario)):
        binario.append(0)
crom = binario[::-1]
print (crom)