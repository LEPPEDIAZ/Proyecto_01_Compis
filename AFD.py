from generadorAFN import *

class afn2afd:
    def __init__(self, afn):
        self.AFD_ConsFix(afn)

    def TransposicionFinalAFD(self):
        variable = self.afd.transformacion_vs2()
        return variable

    def InEndAFD(self):
        variable = self.afd.inicio_final()
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
  

                
    