
import os
import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *


if __name__ == '__main__':
	print("Generador de AFN")
	ver_archivo = input("Ingrese el nombre del archivo de COCO/R que quiere observar: ")
	keypass_01 = open("seleccionar_archivo.txt", "w")
	keypass_01.write(ver_archivo)
	keypass_01.close()
	os.system("python3 Core.py")
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
		mensaje = input("Ingrese el mensaje que desea saber si pertenece al lenguaje: ")
		sacar_variable2 = [[str(num) for num in item] for item in sacar_variable2]
		print("sacar variable2 ", sacar_variable2)
		sacar_variable = [[str(num) for num in item] for item in sacar_variable]
		print("sacar_variable", sacar_variable)
		print(existe(mensaje,sacar_variable,sacar_variable2))
		#print("|------------MINIMIZACION--------------|")
		#b.minimizador()
		#sacar_variable =b.TransposicionFinalMIN()
		#sacar_variable2 = b.InEndMIN()
		#graficar_MIN(sacar_variable,sacar_variable2)
		#generacion_de_archivo_min(sacar_variable,sacar_variable2)
		#keypass = open("expresion_regular.txt", "w")
		#keypass.write(expresion_regular)
		#keypass.close()
	else:
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
		mensaje = input("Ingrese el mensaje que desea saber si pertenece al lenguaje: ")
		sacar_variable2 = [[str(num) for num in item] for item in sacar_variable2]
		print("sacar variable2 ", sacar_variable2)
		sacar_variable = [[str(num) for num in item] for item in sacar_variable]
		print("sacar_variable", sacar_variable)
		print(existe(mensaje,sacar_variable,sacar_variable2))




	
	
		