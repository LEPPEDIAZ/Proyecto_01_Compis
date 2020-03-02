import sys
import os
from expresion_regular import *
from generadorAFN import *

if __name__ == '__main__':
	print("Generador de AFN")
	expresion_regular = input("Ingrese la expresion regular: ")
	thompson = Thompson(expresion_regular)
	thompson = thompson.expresionregular_a_AFN()
	thompson.imprimir_Transformaciones()
	os.system("dot -Tgif afn.txt > afn.png")
	print("observa las imagenes afn.txt y afn.png")
	