
from generadorAFN import *
def afd_generado_de_afn(transformaciones, inicial_final):
    alfabeto =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    def e_cerradura(estado_s, conjunto_de_estado):
        if isinstance(estado_s, int):
            nodo = []
            nodo.append(estado_s)
        else: 
            nodo = list(estado_s)
        if isinstance(nodo, list):
            for n in nodo:
                mover = dtran_para_d(n, "E", conjunto_de_estado)
                for estado_s in mover:
                    if estado_s[2] not in nodo:
                        nodo.append(estado_s[2])
        estado = set()
        for variable in nodo:
            estado.add(variable)
        return estado
    sim = []
    for i in range(len(transformaciones)):
        if transformaciones[i][1] != "E":
            if transformaciones[i][1] not in sim:
                sim.append(transformaciones[i][1])
    i = 0
    destados =[]
    trans = []
    destados.append(e_cerradura(inicial_final[0], transformaciones))
    inicial_final_nuevo =[]
    inicial_final_nuevo.append(e_cerradura(inicial_final[0], transformaciones))
    while i < len(destados):
        for n in sim:
            u = e_cerradura(mover(destados[i],n,transformaciones),transformaciones)
            trans.append([destados[i],n,u])
            for w in inicial_final:
                if w[1] in u:
                    inicial_final_nuevo.append(u)
            if u not in destados and u is not None:
                destados.append(u)         
        i+=1
    estado_s = 0
    while estado_s < len(trans):
        if trans[estado_s][0] == set() or trans[estado_s][2] == set():
            trans.pop(estado_s)
            estado_s-=1   
        estado_s +=1
    estado_s = 0 
    while estado_s < len(trans):
        indice1 = destados.index(trans[estado_s][0])
        trans[estado_s][0] = alfabeto[indice1]
        indice1 = destados.index(trans[estado_s][2])
        trans[estado_s][2] = alfabeto[indice1]
        estado_s +=1
    estado_s = 0
    while estado_s < len(inicial_final_nuevo):
        indice1 = destados.index(inicial_final_nuevo[estado_s])
        inicial_final_nuevo[estado_s]= alfabeto[indice1]
        estado_s+=1
    init_end = []
    for i in range(1,len(inicial_final_nuevo)):
        init_end.append([inicial_final_nuevo[0],inicial_final_nuevo[i]])
    return trans, init_end
        
def mover(nodo, entrada, conjunto_de_estado):
    nodo = list(nodo)
    movimiento = []
    if isinstance(nodo, list):
        for n in nodo:
            mover = dtran_para_d(n, entrada, conjunto_de_estado)
            for estado_s in mover:
                if estado_s[2] not in movimiento:
                    movimiento.append(estado_s[2])
        i = set()
        for variable in movimiento:
            i.add(variable)
        return i
    
    else:
        mover = dtran_para_d(nodo, entrada, conjunto_de_estado)
        for estado_s in mover:
            if estado_s[2] not in movimiento:
                movimiento.append(estado_s[2])
        i = set()
        for variable in movimiento:
            i.add(variable)
        return i

def dtran_para_d(nodo,entrada, automata):
    movimientos = []
    for i in automata:
        if i[0] == nodo and i[1] == str(entrada):
            movimientos.append(i) 
    return movimientos


class Subconjunto:
    def __init__(self, afn):
        self.DTran(afn)


    def TransposicionFinalAFD(self):
        variable = self.afd.transformacion_vs2()
        print("variable",variable)
        return variable

    def InEndAFD(self):
        variable = self.afd.inicio_final()
        return variable
    
    def TransposicionFinalMIN(self):
        variable = self.minafd.transformacion_vs2()
        return variable

    def InEndMIN(self):
        variable = self.minafd.inicio_final()
        return variable

    def DTran(self, afn):   
        todos_los_estados = dict()
        print(todos_los_estados)  
        closure = dict()   
        print(closure)
        primer_estado = afn.ObtenerEpsilonCl(afn.init_estado)
        print(primer_estado)
        closure[afn.init_estado] = primer_estado
        print(closure[afn.init_estado])
        numero_subsets = 1
        afd = AFN_ESTADO(afn.simbolo)
        print(afd)
        afd.Marcar_Inicio(numero_subsets)
        print(afd.Marcar_Inicio(numero_subsets))
        estados = [[primer_estado, afd.init_estado]] 
        print(estados)
        todos_los_estados[numero_subsets] = primer_estado
        print(todos_los_estados)
        numero_subsets += 1
        print(numero_subsets)
        while len(estados):
            [estado, index_de_origen] = estados.pop()
            for x in afd.simbolo:
                movida = afn.RealizarMovida(estado, x)
                for i in list(movida):    
                    if i not in closure:
                        closure[i] = afn.ObtenerEpsilonCl(i)
                    movida = movida.union(closure[i])
                    print(movida)
                if len(movida):
                    if movida not in todos_los_estados.values():
                        estados.append([movida, numero_subsets])
                        todos_los_estados[numero_subsets] = movida
                        index_destino = numero_subsets
                        numero_subsets += 1
                    else:
                        index_destino = [ j for j, u in todos_los_estados.items() if u == movida][0]
                    afd.Agregar_Transicion(index_de_origen, index_destino, x)
            for caracter, estado in todos_los_estados.items():
                if afn.estado_final[0] in estado:
                    afd.Agregar_Final(caracter)
            self.afd = afd

    def minimizador(self): 
        def retorno_de_numeros(estados, sets):
            numero_subsets = 1
            cambios = dict()
            for i in estados:
                if sets[i] not in cambios:
                    cambios[sets[i]] = numero_subsets
                    numero_subsets += 1
                sets[i] = cambios[sets[i]]

        estados = list(self.afd.estados)
        estado_destino = dict(set())
        interseccion = dict()
        carac = dict() 
        interseccion = {1: set(), 2: set()}
        sin_revisar = []
        numero_subsets = 3 
        for i in estados:
            for j in self.afd.simbolo:
                if i in estado_destino:
                    if j in estado_destino[i]:
                        estado_destino[i][j] = estado_destino[i][j].union(self.afd.RealizarMovida(i, j))
                    else:
                        estado_destino[i][j] = self.afd.RealizarMovida(i, j)
                else:
                    estado_destino[i] = {j : self.afd.RealizarMovida(i, j)}
                if len(estado_destino[i][j]):
                    estado_destino[i][j] = estado_destino[i][j].pop()
                else:
                    estado_destino[i][j] = 0
        for i in estados:
            if i not in self.afd.estado_final:
                interseccion[1] = interseccion[1].union(set([i]))
                carac[i] = 1
        for k in self.afd.estado_final:
            interseccion[2] = interseccion[2].union(set([k]))
            carac[k] = 2
        sin_revisar.extend([[interseccion[1], 1], [interseccion[2], 2]])
        while len(sin_revisar):
            [estados_iguales, id] = sin_revisar.pop()
            for j in self.afd.simbolo:
                diferencial = dict()
                for i in estados_iguales:
                    if estado_destino[i][j] == 0:
                        if 0 in diferencial:
                            diferencial[0].add(i)
                        else:
                            diferencial[0] = set([i])
                    else:
                        if carac[estado_destino[i][j]] in diferencial:
                            diferencial[carac[estado_destino[i][j]]].add(i)
                        else:
                            diferencial[carac[estado_destino[i][j]]] = set([i])
                if len(diferencial) > 1:
                    for k, v in diferencial.items():
                        if k:
                            for i in v:
                                interseccion[id].remove(i)
                                if numero_subsets in interseccion:
                                    interseccion[numero_subsets] = interseccion[numero_subsets].union(set([i]))
                                else:
                                    interseccion[numero_subsets] = set([i])
                            if len(interseccion[id]) == 0:
                                interseccion.pop(id)
                            for i in v:
                                carac[i] = numero_subsets
                            sin_revisar.append([interseccion[numero_subsets], numero_subsets])
                            numero_subsets += 1
                    break
        if len(interseccion) == len(estados):
            self.minafd = self.afd
        else:
            retorno_de_numeros(estados, carac)
            self.minafd = self.afd.Cambio_de_estados_despues_de_Merge(interseccion, carac)

   
    




    
   
    
  

                
    