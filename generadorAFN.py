from transformacion import Transformacion 
from collections import defaultdict
from graphviz import Digraph , render
global array_last
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
    [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
    [chr(i) for i in range(ord('0'), ord('9') + 1)]
epsilon = 'ε'

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
def graficar_AFDVS2(transformacion_final, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/afn_to_afd2')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for i in range(len(inicial_final)):
        f.node(str(inicial_final[i][1]))
    f.attr('node', shape='circle')
    for i in range(len(transformacion_final)):
        f.edge(str(transformacion_final[i][0]), str(transformacion_final[i][2]), label= str(transformacion_final[i][1]))
    f.view()
def graficar_MIN(transformacion_final, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/min')
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
def graficar_AFNVS2(transformacion_final, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/afn_02')
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
	    array_init = []
	    array_init.append(str(inicial_final[i][0]))
    f.write("INICIO: " + str(array_init) + "\n")
    array_last = []
    for i in range(len(inicial_final)):
	    array_last.append(str(inicial_final[i][1]))
	    print(str(array_last))
    f.write("ACEPTACION: " + str(array_last) + "\n")
    f.write("TRANSICION: " + str(transformacion_final) + "\n")

def generacion_de_archivo_afd_test(transformacion_final, inicial_final):
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
    stdos = str(stdos)
    stdos = stdos.replace('[', '')
    stdos = stdos.replace(']', '')
    f.write("states," + str(stdos) +  "\n")
    simb = str(simb)
    simb = simb.replace('[', '')
    simb = simb.replace(']', '')
    f.write("alpha," + str(simb) + "\n")    
    for i in range(len(inicial_final)):
	    array_init = []
	    array_init.append(str(inicial_final[i][0]))
    array_init = ','.join(array_init)
    f.write("start, " + str(array_init) + "\n")
    array_last = []
    for i in range(len(inicial_final)):
	    array_last.append(str(inicial_final[i][1]))
	    print(str(array_last))
    array_last = ','.join(array_last)
    f.write("final, " + str(array_last) + "\n")
    #transformacion_final = ','.join(str(transformacion_final[0]))
    transformacion_final2 = str(transformacion_final)
    transformacion_final2 = transformacion_final2.replace('[', '')
    transformacion_final2 = transformacion_final2.replace(']', '')
	#transformacion_final2 = transformacion_final2.replace("'", "")
    print("FINAL", transformacion_final2)
    print("FINAL2", str(transformacion_final2))
    f.write("trans-func, " + str(transformacion_final2) + "\n")

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
class AFN_ESTADO:

    def __init__(self, simbolo = set([])):
        self.estados = set()
        self.simbolo = simbolo    
        self.transiciones = defaultdict(defaultdict)
        self.init_estado = None
        self.estado_final = []
    
    def inicio_final(self):
        arreglo = []
        arreglo.append(self.init_estado)
        arreglo.append(self.estado_final[0])
        arreglo_final2 = []
        arreglo_final2.append(arreglo)
        print(arreglo_final2)
        return arreglo_final2

    def transformacion_vs2(self):
        arreglofinal = []
        for estado_anterior, nuevo_estados in self.transiciones.items():
            subarray = []
            for estado in nuevo_estados:
                variable_pasada = ''
                for s in nuevo_estados[estado]:
                    variable_pasada += s + '|'
                    #arreglofinal.append(subarray)
                    #('s' + str(estado_anterior), 's' + str(estado), label = variable_pasada[:-1])
                print("Resultado02", str(estado_anterior) + "," + variable_pasada[:-1] + ","+ str(estado))
                array = []
                array.append(estado_anterior)
                array.append(variable_pasada[:-1])
                array.append(estado)
                arreglofinal.append(array)                    
        print("TRANSICION", arreglofinal)
        print("final",arreglofinal, self.init_estado, self.estado_final)
        return arreglofinal
       
    def Marcar_Inicio(self, estado):
        self.init_estado = estado
        self.estados.add(estado)

    def Agregar_Final(self, estado):
        if isinstance(estado, int):
            estado = [estado]
        for s in estado:
            if s not in self.estado_final:
                self.estado_final.append(s)

    def Agregar_Transicion(self, estado_anterior, nuevo_estado, expresion):  
        if isinstance(expresion, str):
            expresion = set([expresion])
        self.estados.add(estado_anterior)
        self.estados.add(nuevo_estado)
        if estado_anterior in self.transiciones and nuevo_estado in self.transiciones[estado_anterior]:
            self.transiciones[estado_anterior][nuevo_estado] = \
            self.transiciones[estado_anterior][nuevo_estado].union(expresion)
        else:
            self.transiciones[estado_anterior][nuevo_estado] = expresion

    def Agregar_Transicion_dict(self, transiciones):  
        for estado_anterior, nuevo_estados in transiciones.items():
            for estado in nuevo_estados:
                self.Agregar_Transicion(estado_anterior, estado, nuevo_estados[estado])
                print("mostrar transicion", str(self.Agregar_Transicion(estado_anterior, estado, nuevo_estados[estado])) )

    def Construir_Por_Num(self, ninicio):
   
        translations = {}
        for i in self.estados:
            translations[i] = ninicio
            ninicio += 1
        re_construir = AFN_ESTADO(self.simbolo)
        re_construir.Marcar_Inicio(translations[self.init_estado])
        re_construir.Agregar_Final(translations[self.estado_final[0]])
        
        for estado_anterior, nuevo_estados in self.transiciones.items():
            for estado in nuevo_estados:
                re_construir.Agregar_Transicion(translations[estado_anterior], translations[estado], nuevo_estados[estado])
        return [re_construir, ninicio]
	
    def ObtenerEpsilonCl(self, findestado):
	    todos_los_estados = set()
	    estados = [findestado]
	    while len(estados):
		    estado = estados.pop()
		    todos_los_estados.add(estado)
		    if estado in self.transiciones:
			    for i in self.transiciones[estado]:
				    if epsilon in self.transiciones[estado][i] and \
                        i not in todos_los_estados:
					    estados.append(i)
	    return todos_los_estados

    def RealizarMovida(self, estado, charllave):
        if isinstance(estado, int):
            estado = [estado]
        movida = set()
        for j in estado:
            if j in self.transiciones:
                for tns in self.transiciones[j]:
                    if charllave in self.transiciones[j][tns]:
                        movida.add(tns)
        print("movida", movida)
        return movida
	
    def Cambio_de_estados_despues_de_Merge(self, interseccion, carac):
        reconstruir = AFN_ESTADO(self.simbolo)
        for estadodestino, estado_destinos in self.transiciones.items():
            for estado in estado_destinos:
                reconstruir.Agregar_Transicion(carac[estadodestino], carac[estado], estado_destinos[estado])
        reconstruir.Marcar_Inicio(carac[self.init_estado])
        for i in self.estado_final:
            reconstruir.Agregar_Final(carac[i])
    
        return reconstruir

class Exp_AFNVS2:

    def __init__(self, expreg):
        self.expreg = expreg
        self.ConstruirSecAFN()

    def InEnd(self):
        variable = self.afn.inicio_final()
        return variable
    def FunctionsNFA(self):
        variable = self.afn.transformacion_vs2()
        return variable
    
    def tomar_prioridad(op):
        if op == '|':
            return 1
        elif op == '·':
            return 2
        elif op == '*':
            return 3
        else:       
            return 0

    
    def unico_caracter(expresion):   
        estado1 = 1
        estado2 = 2
        estructura = AFN_ESTADO(set([expresion]))
        estructura.Marcar_Inicio(estado1)
        estructura.Agregar_Final(estado2)
        estructura.Agregar_Transicion(estado1, estado2, expresion)
        return estructura

    def union(a, b):  
        [a, sec] = a.Construir_Por_Num(2)
        [b, sec2] = b.Construir_Por_Num(sec)
        estado1 = 1
        estado2 = sec2
        unionAFN = AFN_ESTADO(a.simbolo.union(b.simbolo))
        unionAFN.Marcar_Inicio(estado1)
        unionAFN.Agregar_Final(estado2)
        unionAFN.Agregar_Transicion(unionAFN.init_estado, a.init_estado, epsilon)
        unionAFN.Agregar_Transicion(unionAFN.init_estado, b.init_estado, epsilon)
        unionAFN.Agregar_Transicion(a.estado_final[0], unionAFN.estado_final[0], epsilon)
        unionAFN.Agregar_Transicion(b.estado_final[0], unionAFN.estado_final[0], epsilon)
        unionAFN.Agregar_Transicion_dict(a.transiciones)
        unionAFN.Agregar_Transicion_dict(b.transiciones)
        return unionAFN

  
    def concatenar(a, b):   
        [a, sec] = a.Construir_Por_Num(1)
        [b, sec2] = b.Construir_Por_Num(sec)
        estado1 = 1
        estado2 = sec2 - 1
        concatenarAFN = AFN_ESTADO(a.simbolo.union(b.simbolo))
        concatenarAFN.Marcar_Inicio(estado1)
        concatenarAFN.Agregar_Final(estado2)
        concatenarAFN.Agregar_Transicion(a.estado_final[0], b.init_estado, epsilon)
        concatenarAFN.Agregar_Transicion_dict(a.transiciones)
        concatenarAFN.Agregar_Transicion_dict(b.transiciones)
        return concatenarAFN

  
    def variable_kleene(a):  
        [a, sec] = a.Construir_Por_Num(2)
        estado1 = 1
        estado2 = sec
        Kleene = AFN_ESTADO(a.simbolo)
        Kleene.Marcar_Inicio(estado1)
        Kleene.Agregar_Final(estado2)
        Kleene.Agregar_Transicion(Kleene.init_estado, a.init_estado, epsilon)
        Kleene.Agregar_Transicion(Kleene.init_estado, Kleene.estado_final[0], epsilon)
        Kleene.Agregar_Transicion(a.estado_final[0], Kleene.estado_final[0], epsilon)
        Kleene.Agregar_Transicion(a.estado_final[0], a.init_estado, epsilon)
        Kleene.Agregar_Transicion_dict(a.transiciones)
        return Kleene
    
    def cerradura_positiva(a):  
        [a, sec] = a.Construir_Por_Num(2)
        estado1 = 1
        estado2 = sec
        CerraduraPositiva = AFN_ESTADO(a.simbolo)
        CerraduraPositiva.Marcar_Inicio(estado1)
        CerraduraPositiva.Agregar_Final(estado2)
        CerraduraPositiva.Agregar_Transicion(CerraduraPositiva.init_estado, a.init_estado , epsilon)
        CerraduraPositiva.Agregar_Transicion(CerraduraPositiva.init_estado + 2 , CerraduraPositiva.estado_final[0] , epsilon)
        #CerraduraPositiva.Agregar_Transicion(a.estado_final[0], CerraduraPositiva.estado_final[0], epsilon)
        CerraduraPositiva.Agregar_Transicion(a.estado_final[0], a.init_estado, epsilon)
        CerraduraPositiva.Agregar_Transicion_dict(a.transiciones)
        return CerraduraPositiva


    def ConstruirSecAFN(self):
        caracter = ''
        exp1 = ''
        simbolo = set()
        for token in self.expreg:
            if token in alphabet:
                simbolo.add(token)
            if token in alphabet or token == '(':
                if exp1 != '·' and (exp1 in alphabet or exp1 in ['*', ')']):
                    caracter += '·'
            caracter += token
            exp1 = token
        self.expreg = caracter
        caracter = ''
        final_array = []
        for token in self.expreg:
            if token in alphabet:
                caracter += token
            elif token == '(':
                final_array.append(token)
            elif token == ')':
                while(final_array[-1] != '('):
                    caracter += final_array[-1]
                    final_array.pop()
                final_array.pop()    
            else:
                while(len(final_array) and Exp_AFNVS2.tomar_prioridad(final_array[-1]) >= Exp_AFNVS2.tomar_prioridad(token)):
                    caracter += final_array[-1]
                    final_array.pop()
                final_array.append(token)
        while(len(final_array) > 0):
            caracter += final_array.pop()
        self.expreg = caracter
        self.automata = []
        for token in self.expreg:
            if token in alphabet:
                self.automata.append(Exp_AFNVS2.unico_caracter(token))
            elif token == '|':
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Exp_AFNVS2.union(a, b))
            elif token == '·':
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Exp_AFNVS2.concatenar(a, b))
            elif token == '*':
                a = self.automata.pop()
                self.automata.append(Exp_AFNVS2.variable_kleene(a))
            elif token == '+':
                a = self.automata.pop()
                self.automata.append(Exp_AFNVS2.cerradura_positiva(a))
        self.afn = self.automata.pop()
        self.afn.simbolo = simbolo
