from copy import deepcopy
from errorhandlers import *


        
class generador_AFD:
    def __init__(self,Estados_Marcados,Lista_de_Estados,funcion_delta,inicial,final):
        self.Estados_Marcados = Estados_Marcados
        self.Lista_de_Estados = Lista_de_Estados
        self.funcion_delta = funcion_delta
        self.inicial = inicial
        self.final = final

    def L(self, r):
        if len(set(r) - self.Lista_de_Estados) != 0:
            print('ERROR characters',(set(r)-self.Lista_de_Estados),'are not in the automata\'s alfabeto')
            exit(0)
    
        estado_inicial = self.inicial
        for i in r:
         
            if estado_inicial >= len(self.funcion_delta):
                print('Message NOT accepted, state has no transitions')
                exit(0)
            if i not in self.funcion_delta[estado_inicial].keys():
                print('Message NOT accepted, state has no transitions with the character')
                exit(0)
       
            estado_inicial = self.funcion_delta[estado_inicial][i]
        
        if estado_inicial in self.final:
            print('Message accepted!')
        else:
            print('Message NOT accepted, stopped in an unfinal state')

    def escribir(self):
        for i in range(len(self.Estados_Marcados)):
            print(i,self.funcion_delta[i],'final' if i in self.final else '')


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



	

