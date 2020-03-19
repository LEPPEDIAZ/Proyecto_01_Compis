from generadorAFN import *

class Conversion_AFN_AFD:
    def __init__(self, afn):
        self.AFD_ConsFix(afn)

    def TransposicionFinalAFD(self):
        variable = self.afd.transformacion_vs2()
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

    def AFD_ConsFix(self, afn):   
        todos_los_estados = dict()  
        closure = dict()   
        primer_estado = afn.ObtenerEpsilonCl(afn.init_estado)
        closure[afn.init_estado] = primer_estado
        numero_subsets = 1
        afd = AFN_ESTADO(afn.simbolo)
        afd.Marcar_Inicio(numero_subsets)
        estados = [[primer_estado, afd.init_estado]] 
        todos_los_estados[numero_subsets] = primer_estado
        numero_subsets += 1
        while len(estados):
            [estado, index_de_origen] = estados.pop()
            for x in afd.simbolo:
                movida = afn.RealizarMovida(estado, x)
                for i in list(movida):    
                    if i not in closure:
                        closure[i] = afn.ObtenerEpsilonCl(i)
                    movida = movida.union(closure[i])
                if len(movida):
                    if movida not in todos_los_estados.values():
                        estados.append([movida, numero_subsets])
                        todos_los_estados[numero_subsets] = movida
                        index_destino = numero_subsets
                        numero_subsets += 1
                    else:
                        index_destino = [movida == j for j, u in todos_los_estados.items() if u ][0]
                    afd.Agregar_Transicion(index_de_origen, index_destino, x)
            for caracter, estado in todos_los_estados.items():
                if afn.estado_final[0] in estado:
                    afd.Agregar_Final(caracter)
            self.afd = afd

    def minimizador(self): 
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
            Conversion_AFN_AFD.retorno_de_numeros(estados, carac)
            self.minafd = self.afd.Cambio_de_estados_despues_de_Merge(interseccion, carac)
  
    def retorno_de_numeros(estados, sets):  
        numero_subsets = 1
        cambios = dict()
        for i in estados:
            if sets[i] not in cambios:
                cambios[sets[i]] = numero_subsets
                numero_subsets += 1
            sets[i] = cambios[sets[i]]
                
    