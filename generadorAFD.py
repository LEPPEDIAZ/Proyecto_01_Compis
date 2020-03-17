from copy import deepcopy
from expresion_regular import *
from graphviz import Digraph

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
    f= open("Textos_Generados/afd_generado.txt","w+")
    f.write("AFN\n") 
    f.write("ESTADOS: " + str(stdos) +  "\n")
    f.write("SIMBOLOS: " + str(simb) + "\n")    
    for i in range(len(inicial_final)):
        f.write("INICIO: " + str(inicial_final[i][0]) + "\n")
    for i in range(len(inicial_final)):
        f.write("ACEPTACION: " + str(inicial_final[i][1]) + "\n")
    f.write("TRANSICION: " + str(transformacion_final) + "\n") 	

def graficar_AFD_generado(resultado, inicial_final):
    f = Digraph('finite_state_machine', filename='./Automatas_Graficados/generador_afd')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for i in range(len(inicial_final)):
        f.node(str(inicial_final[i][1]))
    f.attr('node', shape='circle')
    for i in range(len(resultado)):
        f.edge(str(resultado[i][0]), str(resultado[i][2]), label= str(resultado[i][1]))
    f.view()

class generador_AFD:
    def __init__(self,Estados_Marcados,Lista_de_Estados,funcion_delta,inicial,final):
        self.Estados_Marcados = Estados_Marcados
        self.Lista_de_Estados = Lista_de_Estados
        self.funcion_delta = funcion_delta
        self.inicial = inicial
        self.final = final

    def inicio_final(self):
        arreglo = []
        arreglo_final = []
        arreglo.append(self.inicial)
        arreglo.append(self.final[0])
        arreglo_final.append(arreglo)
        return arreglo_final

    def L(self, r):
        if len(set(r) - self.Lista_de_Estados) != 0:
            print('Error de caracteres',(set(r)-self.Lista_de_Estados),'ya que no pertenece al alfabeto')
            exit(0)
    
        estado_inicial = self.inicial
        for i in r:
         
            if estado_inicial >= len(self.funcion_delta):
                print('Cadena L(r) aceptada')
                exit(0)
            if i not in self.funcion_delta[estado_inicial].keys():
                print('Cadena L(r) no aceptada')
                exit(0)
       
            estado_inicial = self.funcion_delta[estado_inicial][i]
        
        if estado_inicial in self.final:
            print('Cadena L(r) aceptada')
        else:
            print('Cadena L(r) no aceptada')

    def escribir(self):
        write_direct_afd = []
        for i in range(len(self.Estados_Marcados)):
            print("funcion escribir",i,self.funcion_delta[i],'final' if i in self.final else '')
            for key,value in self.funcion_delta[i].items():
                temp = [i,key,value]
                write_direct_afd.append(temp)
                print("TESTING", write_direct_afd)
        return write_direct_afd
    
    def escribir_02(self):
        #print("escribir 02",self.Estados_Marcados)
        write_direct_afd = []
        for i in range(len(self.Estados_Marcados)):
            print(i,self.funcion_delta[i],'final' if i in self.final else '')
            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            print("final", 'final' if i in self.final else '')
            print("!!!!!!!!!!!!!!!!!!!!!!!!")
            for key,value in self.funcion_delta[i].items():
                temp = [i,key,(value)]
                write_direct_afd.append(temp)
                print("TESTING", write_direct_afd)
        lenght_matrix = len(write_direct_afd)
        last_array = write_direct_afd[lenght_matrix - 1]
        write_direct_afd.pop()
        lenght_array = len(last_array)
        last_value = last_array[lenght_array - 1]
        last_array.pop()
        last_array.append(last_value +1)
        write_direct_afd.append(last_array)
        return write_direct_afd

		
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
        cerradura_positiva = -1 
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
            if expresion_regular[i] == '+':
                if cerradura_positiva == -1:
                    cerradura_positiva = i
                continue
            if expresion_regular[i] == '|':
                if operador_or == -1:
                    operador_or = i
        if cerradura_positiva != -1:
            self.elemento = '+'
            self.hijos.append(NodoExpresionRegular(self.validar_brackets(expresion_regular[:cerradura_positiva])))
        elif operador_or != -1:
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
        
        elif self.elemento == '+':
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


print("---------------------------------------------------")

rama = False
simbolo = '_'
alfabeto = None
#expresion_regular = '(b|b)*abb(a|b)*'
expresion_regular= open("expresion_regular.txt", "r+")
expresion_regular = expresion_regular.read()
p_expresion_regular = preprocesamiento(expresion_regular)
print(p_expresion_regular)
alfabeto = todo_el_alfabeto(p_expresion_regular)
print(alfabeto)
extra = ''
alfabeto = alfabeto.union(set(extra))
print(alfabeto)

arbol = ArbolitoER(p_expresion_regular)
print(arbol)

generador_AFD = arbol.Convertir_a_AFD()
print(generador_AFD)

#message = 'babbaaaaa'
print("-----------------------------------------------")
print('Automata AFD : \n')
generador_AFD.escribir()
transformacion_resultados = generador_AFD.escribir_02()
print("transformacion", transformacion_resultados)
#generador_AFD.imprimir_Transformaciones()
init_end = generador_AFD.inicio_final()
print("inicio final",init_end)
graficar_AFD_generado(transformacion_resultados, init_end)
generacion_de_archivo(transformacion_resultados, init_end)
print("**************************************************")
print("**************************************************")
message = input("Ingrese la cadena w: ")
print('\nPertenece o no a L(r): "'+message+'" : ')
generador_AFD.L(message)
print("**************************************************")
print("**************************************************")
	

