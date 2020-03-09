from pythonds.basic.stack import Stack
from transformacion import Transformacion 
from generadorAFN import *
import queue
import json 
DEBUG = False
rama = False
simbolo = '_'
alfabeto = None
def regularexp_valido(expresion_regular):
    return brackets_validos(expresion_regular) 

def preprocesamiento(expresion_regular):
    expresion_regular = variable_kleene_limpia(expresion_regular)
    expresion_regular = expresion_regular.replace(' ','')
    expresion_regular = '(' + expresion_regular + ')' + '#'
    while '()' in expresion_regular:
        expresion_regular = expresion_regular.replace('()','')
    return expresion_regular

def variable_kleene_limpia(expresion_regular):
    for i in range(0, len(expresion_regular) - 1):
        while i < len(expresion_regular) - 1 and expresion_regular[i + 1] == expresion_regular[i] and expresion_regular[i] == '*':
            expresion_regular = expresion_regular[:i] + expresion_regular[i + 1:]
    return expresion_regular

def todo_el_alfabeto(expresion_regular):
    return set(expresion_regular) - set('()|*')

def brackets_validos(expresion_regular):
    brackets_abiertos = 0
    for c in expresion_regular:
        if c == '(':
            brackets_abiertos += 1
        if c == ')':
            brackets_abiertos -= 1
        if brackets_abiertos < 0:
            print('falta un bracket')
            return False
    if brackets_abiertos == 0:
        return True
    return False
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

	

