from transformacion import Transformacion 
from graphviz import Digraph

def graficar_AFD(transformacion_final, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/afn_to_afd')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for i in range(len(inicial_final)):
        f.node(str(inicial_final[i][1]))
    f.attr('node', shape='circle')
    for i in range(len(transformacion_final)):
        f.edge(str(transformacion_final[i][0]), str(transformacion_final[i][2]), label= str(transformacion_final[i][1]))
    f.view()

def graficar_AFN(transformacion_final, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/afn')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for i in range(len(inicial_final)):
        f.node(str(inicial_final[i][1]))
    f.attr('node', shape='circle')
    for i in range(len(transformacion_final)):
        f.edge(str(transformacion_final[i][0]), str(transformacion_final[i][2]), label= str(transformacion_final[i][1]))
    f.view()
def generacion_de_archivo(transformacion_final, inicial_final):
    stdos = []
    simb = []
    for i in range(len(transformacion_final)):
        if transformacion_final[i][0] not in stdos:
            stdos.append(transformacion_final[i][0])
                
        if transformacion_final[i][1] not in stdos:
            stdos.append(transformacion_final[i][1])
                
        if transformacion_final[i][2] not in simb:
            simb.append(transformacion_final[i][2])
    f= open("Textos_Generados/afn.txt","w+")
    f.write("AFN\n") 
    f.write("ESTADOS: " + str(stdos) +  "\n")
    f.write("SIMBOLOS: " + str(simb) + "\n")    
    for i in range(len(inicial_final)):
        f.write("INICIO: " + str(inicial_final[i][0]) + "\n")
    for i in range(len(inicial_final)):
        f.write("ACEPTACION: " + str(inicial_final[i][1]) + "\n")
    f.write("TRANSICION: " + str(transformacion_final) + "\n") 	

def generacion_de_archivo_afd(transformacion_final, inicial_final):
    stdos = []
    simb = []
    for i in range(len(transformacion_final)):
        if transformacion_final[i][0] not in stdos:
            stdos.append(transformacion_final[i][0])
                
        if transformacion_final[i][1] not in stdos:
            stdos.append(transformacion_final[i][1])
                
        if transformacion_final[i][2] not in simb:
            simb.append(transformacion_final[i][2])
    f= open("Textos_Generados/afd.txt","w+")
    f.write("AFN\n") 
    f.write("ESTADOS: " + str(stdos) +  "\n")
    f.write("SIMBOLOS: " + str(simb) + "\n")    
    for i in range(len(inicial_final)):
        f.write("INICIO: " + str(inicial_final[i][0]) + "\n")
    for i in range(len(inicial_final)):
        f.write("ACEPTACION: " + str(inicial_final[i][1]) + "\n")
    f.write("TRANSICION: " + str(transformacion_final) + "\n")


class afn(object):
	op = ["(","*","+","|",".","?", ")"]

	def __init__(self, initialState,finalState,Cambio_de_Estado):
		self.initialState = initialState 
		self.finalState = finalState 
		self.Cambio_de_Estado = Cambio_de_Estado 
	

	def estado_final(self):
		return self.finalState
	
	def concatenar(self,s):
		
		numero_of_Cambio_de_Estado = self.estado_final() 
		nuevo_Cambio_de_Estado = [] #
		for t in self.Cambio_de_Estado:
			nuevo_Cambio_de_Estado.append(t) 
		for t in s.Cambio_de_Estado:
			t.qFrom += numero_of_Cambio_de_Estado -1
			t.qTo += numero_of_Cambio_de_Estado -1
			nuevo_Cambio_de_Estado.append(t) 
			print("concatenar", t)
		nuevo_afn = afn(self.initialState,s.finalState+numero_of_Cambio_de_Estado- 1,nuevo_Cambio_de_Estado) 
		return nuevo_afn

	def union(self,s):
		
		nuevo_Cambio_de_Estado = [] 
		numero_of_Cambio_de_Estado = self.estado_final() 
	
		finalState = s.finalState + numero_of_Cambio_de_Estado + 2 
		
		for t in self.Cambio_de_Estado:
			t.qFrom += 1
			t.qTo += 1
			nuevo_Cambio_de_Estado.append(t)
		for t in s.Cambio_de_Estado:
			t.qFrom += numero_of_Cambio_de_Estado+1
			t.qTo += numero_of_Cambio_de_Estado+1
			nuevo_Cambio_de_Estado.append(t) 
			print("union", t)
		nuevo_Transformacion1 = Transformacion(1,2,"E") 
		nuevo_Transformacion2 = Transformacion(1,s.initialState+numero_of_Cambio_de_Estado+1,"E") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,finalState,"E") 
		nuevo_Transformacion4 = Transformacion(s.finalState+numero_of_Cambio_de_Estado+1,finalState,"E") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion2)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4)
		nuevo_afn = afn(1,finalState,nuevo_Cambio_de_Estado) 

		return nuevo_afn

	def variable_kleene(self):
		nuevo_Cambio_de_Estado = [] 
		for t in self.Cambio_de_Estado:
			t.qFrom += 1
			t.qTo += 1
			nuevo_Cambio_de_Estado.append(t) 
			print("variable kleene", t)
		nuevo_Transformacion1 = Transformacion(1,2,"E") 
		nuevo_Transformacion2 = Transformacion(1,self.finalState+2,"E") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,self.initialState+1, "E") 
		nuevo_Transformacion4 = Transformacion(self.finalState+1,self.finalState+2,"E") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion2)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4)
		nuevo_afn = afn(1,self.finalState+2,nuevo_Cambio_de_Estado) 
		return nuevo_afn



	def cerradura_positiva(self):
		nuevo_Cambio_de_Estado = []
		for t in self.Cambio_de_Estado:
			t.qFrom += 1
			t.qTo += 1
			nuevo_Cambio_de_Estado.append(t) 
			print("cerradura positiva", t )
		nuevo_Transformacion1 = Transformacion(1,2,"E") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,self.initialState+1, "E")
		nuevo_Transformacion4 = Transformacion(self.finalState+1,self.finalState+2,"E") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1) 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3) 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4) 
		nuevo_afn = afn(1,self.finalState+2,nuevo_Cambio_de_Estado) 
		return nuevo_afn


	def imprimir_texto(self):
		def chunks(l, n):
			for i in range(0, len(l), n):
				yield l[i:i+n]
		arreglo = []
		arreglo2 = []
		for t in self.Cambio_de_Estado:
			print(t)
			t = str(t)
			one= t.split()
			variable0 = one[0]
			variable0 = variable0.replace('q', '')
			arreglo.append(int(variable0))
			variable= one[5]
			variable1 = variable[1]
			arreglo.append(variable1)
			variable2 = one[2]
			variable2 = variable2.replace('q', '')
			arreglo.append(int(variable2))
			arreglo2 = list(chunks(arreglo, 3))
			print("next", arreglo2)
		return arreglo2
	
	

	def imprimir_Transformaciones(self):
		
		f= open("afn.txt","w+")
		f.write("digraph AFN_AnaLucia{\n")
		f.write("rankdir=LR; \n q[shape = circle];\n")
		f.write("qI [shape=point];\n")
		for i in range(self.finalState):
			f.write("q"+str(i+1)+" [name=\""+str(i+1)+"\"];\n")
			if (i+1) == self.finalState:
				f.write("q"+str(i+1)+" [name=\""+str(i+1)+"\" shape = \"doublecircle\"];\n")
			i+=1
		f.write("qI -> q1 [label = \"q0\"];\n")
		for t in self.Cambio_de_Estado:
			f.write(str(t) + "\n")
		f.write("}\n")

	
	def inicio_final(self):
		arreglo = []
		arreglo.append(self.initialState)
		arreglo.append(self.finalState)
		return arreglo


