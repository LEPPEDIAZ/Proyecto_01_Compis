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




    
   
    
  

                
    