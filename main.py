import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *
from AFD import *

if __name__ == '__main__':
	print("Generador de AFN")
	expresion_regular = input("Ingrese la expresion regular: ")
	expresion_regular = expresion_regular.replace('ε', 'e')
	print("-------------------------------------------------------")
	first_char = expresion_regular[0]
	print('First character : ', first_char)
	if first_char in "()":
		print("|------------Thompson--------------|")
		if "?" in expresion_regular:
			expresion_regular.replace("?", "|e")
		if "ε" in expresion_regular:
			expresion_regular.replace("ε", "@")
		a = Thmp(expresion_regular)
		sacar_variable =a.FunctionsNFA()
		sacar_variable2 = a.InEnd()
		graficar_AFNVS2(sacar_variable,sacar_variable2)
		generacion_de_archivo_AFN(sacar_variable,sacar_variable2)
		print("|------------Subconjuntos--------------|")
		b = Subconjunto(a.afn)
		sacar_variable =b.TransposicionFinalAFD()
		sacar_variable2 = b.InEndAFD()
		graficar_AFDVS2(sacar_variable,sacar_variable2)
		generacion_de_archivo_afd_test(sacar_variable,sacar_variable2)
		print("|------------MINIMIZACION--------------|")
		b.minimizador()
		sacar_variable =b.TransposicionFinalMIN()
		sacar_variable2 = b.InEndMIN()
		graficar_MIN(sacar_variable,sacar_variable2)
		generacion_de_archivo_min(sacar_variable,sacar_variable2)
		keypass = open("expresion_regular.txt", "w")
		keypass.write(expresion_regular)
		keypass.close()
	else:
		print("|------------Thompson--------------|")
		keypass = open("expresion_regular.txt", "w")
		keypass.write(expresion_regular)
		keypass.close()
		thompson = Thompson(expresion_regular)
		thompson = thompson.expresionregular_a_AFN()
		imprimir = thompson.imprimir_texto()
		inicio_final = thompson.inicio_final()
		arreglo = []
		arreglo.append(inicio_final)
		graficar_AFN(imprimir, arreglo)
		generacion_de_archivo(imprimir, arreglo)
		print("|------------Subconjuntos--------------|")
		imprimir_2, inicio_final_nuevo = afd_generado_de_afn(imprimir, arreglo)
		graficar_AFD(imprimir_2, inicio_final_nuevo)
		generacion_de_archivo_afd(imprimir_2, inicio_final_nuevo)
		print("|------------MINIMIZACION--------------|")
		a = Thmp(expresion_regular)
		b = Subconjunto(a.afn)
		b.minimizador()
		sacar_variable =b.TransposicionFinalMIN()
		sacar_variable2 = b.InEndMIN()
		graficar_MIN(sacar_variable,sacar_variable2)
		generacion_de_archivo_min(sacar_variable,sacar_variable2)
		expresion_regular = expresion_regular.replace('ε', 'e')
		keypass = open("expresion_regular.txt", "w")
		keypass.write(expresion_regular)
		keypass.close()

	print("|------------DIRECTO--------------|")
	from generadorAFD import *
	p_expresion_regular = preprocesamiento(expresion_regular)
	alfabeto = todo_el_alfabeto(p_expresion_regular)
	extra = ''
	alfabeto = alfabeto.union(set(extra))
	arbol = ArbolitoER(p_expresion_regular)
	from generadorAFD import generador_AFD



	
	
		