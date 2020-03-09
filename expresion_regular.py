from pythonds.basic.stack import Stack
from transformacion import Transformacion 
from generadorAFN import *
from generadorAFD import *
import queue
import json 
#infix:Cuando un operador se encuentra entre cada par de operandos.
#postfix: la expresión de la forma a b op. Cuando se sigue a un operador para cada par de operandos
def infix_a_postfix(expresion_infix): 
    expresion = {}
    expresion["*"] = 4
    expresion["+"] = 4
    expresion["."] = 3
    expresion["|"] = 2
    expresion["("] = 1
    opStack = Stack()
    postfix = []

    for token in expresion_infix:
        if token in "ABCDEFGHIJKLMNOPqRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvwyz" or token in "0123456789":
            postfix.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            tokentop = opStack.pop()
            while tokentop != '(':
                postfix.append(tokentop)
                tokentop = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (expresion[opStack.peek()] >= expresion[token]):
                  postfix.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfix.append(opStack.pop())
    return "".join(postfix)

def evaluarexp(exp):
	op = ["(","|",".",")"]
	aux = ""
	i = 0
	n = 0
	while (i + 1) < len(exp):
		if exp[i] in op:
			if exp[i] == ")" and exp[i+1] == "+" or exp[i+1] == "*":
				aux += exp[i]
				aux += exp[i+1]
			elif exp[i] == ")" and exp[i+1] not in op and exp[i+1] != "+" and exp[i+1] != "*":
				aux += exp[i]
				aux+= "."
			else:
				aux += exp[i]
		elif exp[i] == "+" or exp[i] == "*":
			if(exp[i+1] not in op) or exp[i+1] == "(":
				aux+= "."
		elif exp[i] not in op and exp[i + 1] not in op and exp[i + 1] != "*" and exp[i + 1] != "+":
			aux += exp[i]
			aux += "."		
		elif exp[i] not in op and exp[i + 1] == "*" or exp[i + 1] == "+":
			aux += exp[i]
			aux += exp[i+1]	
		elif (exp[i] not in op and exp[i+1] in op):
			aux += exp[i]
		else:
			print(aux)
			break
		i+=1
		n = i
		if exp[i] not in op and exp[i] != "*" and exp[i] != "+" and n + 1 == len(exp):
			aux += exp[i]
		
	return aux
	
class Thompson(object):
	def __init__(self, regexp):
		self.infix = evaluarexp(regexp)
		self.postfix = infix_a_postfix(regexp)

	def expresionregular_a_AFN(self):
		stack = []  
		postfix = infix_a_postfix(self.infix)
		for s in postfix:
			if s == '*':
				automata = stack.pop() 
				stack.append(automata.variable_kleene()) 
			elif s == '+':
				automata = stack.pop() 
				stack.append(automata.cerradura_positiva()) 
			elif s == '|':
				derecha = stack.pop() 
				izquierda = stack.pop() 
				stack.append(izquierda.union(derecha)) 
			elif s == '.':
				derecha = stack.pop() 
				izquierda = stack.pop() 
				stack.append(izquierda.concatenar(derecha)) 
			else:
				inicializacion_de_Transformaciones = [] 
				inicializacion_de_Transformaciones.append(Transformacion(1,2,s)) 
				afn_generado = afn(1,2,inicializacion_de_Transformaciones) 
				stack.append(afn_generado) 
		#print((str(stack)))
		return stack.pop() 
class NodoExpresionRegular:
    @staticmethod
    def validar_brackets(expresion_regular):
        while expresion_regular[0] == '(' and expresion_regular[-1] == ')' and regularexp_valido(expresion_regular[1:-1]):
            expresion_regular = expresion_regular[1:-1]
        return expresion_regular
    
    @staticmethod
    def concatenar(c):
        return c == '(' or NodoExpresionRegular.letra_recibida(c)
    
    @staticmethod
    def letra_recibida(c):
        return c in alfabeto

    def __init__(self, expresion_regular):
        self.anulable = None
        self.primera_posicion = []
        self.ultima_posicion = []
        self.elemento = None
        self.posicion = None
        self.hijos = []

        if DEBUG:
            print('Actual : '+expresion_regular)
      
        if len(expresion_regular) == 1 and self.letra_recibida(expresion_regular):
            self.elemento = expresion_regular
            if rama:
                if self.elemento == simbolo:
                    self.anulable = True
                else:
                    self.anulable = False
            else:
                self.anulable = False
            return
        variable_kleene = -1
        operador_or = -1
        concatenacion = -1
        i = 0   
        while i < len(expresion_regular):
            if expresion_regular[i] == '(':
                nivel_de_brackets = 1
                i+=1
                while nivel_de_brackets != 0 and i < len(expresion_regular):
                    if expresion_regular[i] == '(':
                        nivel_de_brackets += 1
                    if expresion_regular[i] == ')':
                        nivel_de_brackets -= 1
                    i+=1
            else:
                i+=1

            if i == len(expresion_regular):
                break
            if self.concatenar(expresion_regular[i]):
                if concatenacion == -1:
                    concatenacion = i
                continue
            if expresion_regular[i] == '*':
                if variable_kleene == -1:
                    variable_kleene = i
                continue
            if expresion_regular[i] == '|':
                if operador_or == -1:
                    operador_or = i
        
        if operador_or != -1:
            self.elemento = '|'
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[:operador_or])))
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[(operador_or+1):])))
        elif concatenacion != -1:
            self.elemento = '.'
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[:concatenacion])))
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[concatenacion:])))
        elif variable_kleene != -1:
            self.elemento = '*'
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[:variable_kleene])))

    def calcular_funciones(self, posicion, siguiente_posicion):
        if self.letra_recibida(self.elemento):
            self.primera_posicion = [posicion]
            self.ultima_posicion = [posicion]
            self.posicion = posicion
            siguiente_posicion.append([self.elemento,[]])
            return posicion+1
        for child in self.hijos:
            posicion = child.calcular_funciones(posicion, siguiente_posicion)
    

        if self.elemento == '.':
            if self.hijos[0].anulable:
                self.primera_posicion = sorted(list(set(self.hijos[0].primera_posicion + self.hijos[1].primera_posicion)))
            else:
                self.primera_posicion = deepcopy(self.hijos[0].primera_posicion)
            if self.hijos[1].anulable:
                self.ultima_posicion = sorted(list(set(self.hijos[0].ultima_posicion + self.hijos[1].ultima_posicion)))
            else:
                self.ultima_posicion = deepcopy(self.hijos[1].ultima_posicion)
            self.anulable = self.hijos[0].anulable and self.hijos[1].anulable
            for i in self.hijos[0].ultima_posicion:
                for j in self.hijos[1].primera_posicion:
                    if j not in siguiente_posicion[i][1]:
                        siguiente_posicion[i][1] = sorted(siguiente_posicion[i][1] + [j])

        elif self.elemento == '|':
            self.primera_posicion = sorted(list(set(self.hijos[0].primera_posicion + self.hijos[1].primera_posicion)))
            self.ultima_posicion = sorted(list(set(self.hijos[0].ultima_posicion + self.hijos[1].ultima_posicion)))
            self.anulable = self.hijos[0].anulable or self.hijos[1].anulable

        elif self.elemento == '*':
            self.primera_posicion = deepcopy(self.hijos[0].primera_posicion)
            self.ultima_posicion = deepcopy(self.hijos[0].ultima_posicion)
            self.anulable = True
            for i in self.hijos[0].ultima_posicion:
                for j in self.hijos[0].primera_posicion:
                    if j not in siguiente_posicion[i][1]:
                        siguiente_posicion[i][1] = sorted(siguiente_posicion[i][1] + [j])

        return posicion

    def escribir_nivel(self, nivel):
        print(str(nivel) + ' ' + self.elemento, self.primera_posicion, self.ultima_posicion, self.anulable, '' if self.posicion == None else self.posicion)
        for child in self.hijos:
            child.escribir_nivel(nivel+1)

class ArbolitoER:

    def __init__(self, expresion_regular):
        self.inicioderaiz = NodoExpresionRegular(expresion_regular)
        self.siguiente_posicion = []
        self.funciones()
    
    def escribir(self):
        self.inicioderaiz.escribir_nivel(0)

    def funciones(self):
        posicions = self.inicioderaiz.calcular_funciones(0, self.siguiente_posicion)   
        if DEBUG == True:
            print(self.siguiente_posicion)
    
    def Convertir_a_AFD(self):
        def contiene_hashtag(variable):
            for i in variable:
                if self.siguiente_posicion[i][0] == '#':
                    return True
            return False

        Estados_Marcados = [] 
        Lista_de_Estados = [] 
        automata_alfabeto = alfabeto - {'#', simbolo if rama else ''} 
        funcion_delta = []
        estado_final = [] 
        inicio = self.inicioderaiz.primera_posicion

        Lista_de_Estados.append(inicio)
        if contiene_hashtag(inicio):
            estado_final.append(Lista_de_Estados.index(inicio))
        
        while len(Lista_de_Estados) - len(Estados_Marcados) > 0:
            variable = [i for i in Lista_de_Estados if i not in Estados_Marcados][0]
            funcion_delta.append({})
            Estados_Marcados.append(variable)
            for a in automata_alfabeto:
                estado_destino = []
                for i in variable:
                    if self.siguiente_posicion[i][0] == a:
                        estado_destino = estado_destino + self.siguiente_posicion[i][1]
                estado_destino = sorted(list(set(estado_destino)))
                if len(estado_destino) == 0:
                    continue
                if estado_destino not in Lista_de_Estados:
                    Lista_de_Estados.append(estado_destino)
                    if contiene_hashtag(estado_destino):
                        estado_final.append(Lista_de_Estados.index(estado_destino))
            
                funcion_delta[Lista_de_Estados.index(variable)][a] = Lista_de_Estados.index(estado_destino)
        
        return generador_AFD(Lista_de_Estados,automata_alfabeto,funcion_delta,Lista_de_Estados.index(inicio),estado_final)

	

