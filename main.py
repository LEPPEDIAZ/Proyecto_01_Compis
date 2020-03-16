import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *


if __name__ == '__main__':
	print("Generador de AFN")
	expresion_regular = input("Ingrese la expresion regular: ")
	keypass = open("expresion_regular.txt", "w")
	keypass.write(expresion_regular)
	keypass.close()
	thompson = Thompson(expresion_regular)
	print("thompson",str(thompson))
	thompson = thompson.expresionregular_a_AFN()

	#print(thompson)
	thompson.imprimir_Transformaciones()
	os.system("dot -Tgif afn.txt > afn.png")
	print("observa las imagenes afn.txt y afn.png")
	#test = thompson.imprimir_texto()
	imprimir = thompson.imprimir_texto()
	print("transformacion final", imprimir)
	inicio_final = thompson.inicio_final()
	arreglo = []
	arreglo.append(inicio_final)
	print("inicio y final", arreglo)
	graficar_AFN(imprimir, arreglo)
	generacion_de_archivo(imprimir, arreglo)
	imprimir_2, inicio_final_nuevo = afd_generado_de_afn(imprimir, arreglo)
	print("imprimir_2 AFD de AFN", imprimir_2)
	print("inicio final AFD de AFN", inicio_final_nuevo)
	graficar_AFD(imprimir_2, inicio_final_nuevo)
	generacion_de_archivo_afd(imprimir_2, inicio_final_nuevo)
	#generacion_de_archivo(imprimir_2, inicio_final_nuevo)
	from generadorAFD import *
	p_expresion_regular = preprocesamiento(expresion_regular)
	alfabeto = todo_el_alfabeto(p_expresion_regular)
	extra = ''
	alfabeto = alfabeto.union(set(extra))
	arbol = ArbolitoER(p_expresion_regular)
	from generadorAFD import generador_AFD
	#generador_AFD = arbol.Convertir_a_AFD()
	#print(test)


	
	
		