import sys
import os
from expresion_regular import *
from generadorAFN import *



if __name__ == '__main__':
	print("Generador de AFN")
	expresion_regular = input("Ingrese la expresion regular 1: ")
	keypass = open("expresion_regular.txt", "w")
	keypass.write(expresion_regular)
	keypass.close()
	thompson = Thompson(expresion_regular)
	print(str(thompson))
	thompson = thompson.expresionregular_a_AFN()
	#print(thompson)
	thompson.imprimir_Transformaciones()
	os.system("dot -Tgif afn.txt > afn.png")
	print("observa las imagenes afn.txt y afn.png")
	test = thompson.imprimir_texto()
	from generadorAFD import *
	p_expresion_regular = preprocesamiento(expresion_regular)
	alfabeto = todo_el_alfabeto(p_expresion_regular)
	extra = ''
	alfabeto = alfabeto.union(set(extra))
	arbol = ArbolitoER(p_expresion_regular)
	from generadorAFD import generador_AFD
	#generador_AFD = arbol.Convertir_a_AFD()
	#print(test)


	
	
		