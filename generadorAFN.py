from transformacion import Transformacion 
class afn(object):
	op = ["(","*","+","|","."]

	def __init__(self, initialState,finalState,Cambio_de_Estado):
		self.initialState = initialState 
		self.finalState = finalState 
		self.Cambio_de_Estado = Cambio_de_Estado 
	

	def estado_final(self):
		return self.finalState
	
	def concatenar(self,s):
		numero_of_Cambio_de_Estado = self.estado_final() 
		nuevo_Transformaciones = [] #
		for t in self.Cambio_de_Estado:
			nuevo_Cambio_de_Estado.append(t) 
		for t in s.Cambio_de_Estado:
			t.nodeFrom += numero_of_Cambio_de_Estado -1
			t.nodeTo += numero_of_Cambio_de_Estado -1
			nuevo_Cambio_de_Estado.append(t) 
		nuevo_afn = afn(self.initialState,s.finalState+numero_of_Cambio_de_Estado- 1,nuevo_Cambio_de_Estado) 
		return nuevo_afn

	def union(self,s):
		nuevo_Cambio_de_Estado = [] 
		numero_of_Cambio_de_Estado = self.estado_final() 
	
		finalState = s.finalState + numero_of_Cambio_de_Estado + 2 
		
		for t in self.Cambio_de_Estado:
			t.nodeFrom += 1
			t.nodeTo += 1
			nuevo_Cambio_de_Estado.append(t)
		for t in s.Cambio_de_Estado:
			t.nodeFrom += numero_of_Cambio_de_Estado+1
			t.nodeTo += numero_of_Cambio_de_Estado+1
			nuevo_Cambio_de_Estado.append(t) 
		nuevo_Transformacion1 = Transformacion(1,2,"epsilon") 
		nuevo_Transformacion2 = Transformacion(1,s.initialState+numero_of_Cambio_de_Estado+1,"epsilon") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,finalState,"epsilon") 
		nuevo_Transformacion4 = Transformacion(s.finalState+numero_of_Cambio_de_Estado+1,finalState,"epsilon") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion2)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4)
		nuevo_afn = afn(1,finalState,nuevo_Cambio_de_Estado) 

		return nuevo_afn

	def variable_kleene(self):
		nuevo_Cambio_de_Estado = [] 
		for t in self.Cambio_de_Estado:
			t.nodeFrom += 1
			t.nodeTo += 1
			nuevo_Cambio_de_Estado.append(t) 
		nuevo_Transformacion1 = Transformacion(1,2,"epsilon") 
		nuevo_Transformacion2 = Transformacion(1,self.finalState+2,"epsilon") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,self.initialState+1, "epsilon") 
		nuevo_Transformacion4 = Transformacion(self.finalState+1,self.finalState+2,"epsilon") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion2)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3)
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4)
		nuevo_afn = afn(1,self.finalState+2,nuevo_Cambio_de_Estado) 
		return nuevo_afn

	def cerradura_positiva(self):
		nuevo_Cambio_de_Estado = []
		for t in self.Cambio_de_Estado:
			t.nodeFrom += 1
			t.nodeTo += 1
			nuevo_Cambio_de_Estado.append(t) 
		nuevo_Transformacion1 = Transformacion(1,2,"epsilon") 
		nuevo_Transformacion3 = Transformacion(self.finalState+1,self.initialState+1, "epsilon")
		nuevo_Transformacion4 = Transformacion(self.finalState+1,self.finalState+2,"epsilon") 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion1) 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion3) 
		nuevo_Cambio_de_Estado.append(nuevo_Transformacion4) 
		nuevo_afn = afn(1,self.finalState+2,nuevo_Cambio_de_Estado) 
		return nuevo_afn

	def imprimir_Transformaciones(self):

		f= open("afn.txt","w+")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR; \n node[shape = circle];\n")
		f.write("nodeI [shape=point];\n")
		for i in range(self.finalState):
			f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\"];\n")
			if (i+1) == self.finalState:
				f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\" shape = \"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label = \"I\"];\n")
		for t in self.Cambio_de_Estado:
			f.write(str(t) + "\n")
		f.write("}\n")

