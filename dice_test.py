import random
import numpy as np

resposta = input('Digite a LIB de teste:')
while True:
    if resposta == "random":
            dado = random.randint(1, 20)
            print(dado)
    if resposta == "numpy":
        numero = np.random.randint(1, 21)
        print(numero)
    else:
        print('ERRO')