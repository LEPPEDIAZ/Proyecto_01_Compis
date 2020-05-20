#Parser 
#producciones
#acciones semanticas
#atributos
#any
#ll1

class Build_Parser:
    def __init__(self):
        self.gramatica = []
        self.terminales = []
        self.no_terminales = []
        self.first = dict()
        self.follow = dict()
        self.tabla_de_parseo = dict()
        self.Leer()
        self.encontrar_first()
        self.encontrar_follow()
        self.create_tabla_de_parseo()

    def Leer(self):
        #cambia la gramatica segun producciones
        self.gramatica = [['S','=','a','A'],['A','=','a']]
        #cambia la gramatica segun sus producciones
        for i in range(len(self.gramatica)):
            for j in range(len(self.gramatica[i])):
                if(self.gramatica[i][j].isupper() and self.gramatica[i][j] not in self.no_terminales ):
                    self.no_terminales.append(self.gramatica[i][j])
                if(self.gramatica[i][j] not in self.no_terminales and self.gramatica[i][j] not in ['=','@'] and self.gramatica[i][j] not in self.terminales):
                    self.terminales.append(self.gramatica[i][j])
        print("Terminales", self.terminales)
        print("No Terminales", self.no_terminales )

    def escribir_first(self,k,valor,l):
        for i in range(len(self.gramatica)):
            if(k == self.gramatica[i][0]):
                # si el primer token es un epsion y sino si es una no terminal
                if(self.gramatica[i][2] == '@' and len(self.gramatica[i])-1 == 2):
                    valor.add(self.gramatica[i][2])
                
                elif(self.gramatica[i][2] in self.no_terminales ):
                        self.escribir_first(self.gramatica[i][2],valor,l)
                        if ('@' in valor and len(self.gramatica[i]) > 3):
                            self.escribir_first(self.gramatica[i][l+1],valor,l+1)

                    # Si el primer token es una terminal
                else:
                    valor.add(self.gramatica[i][2])
        return valor
    
    def escribir_follow(self,k,valor):
        if (self.gramatica[0][0] == k):
            valor.add('$')
        for i in range(len(self.gramatica)):
            if(k in self.gramatica[i][2:len(self.gramatica[i])]):
                j = self.gramatica[i][:].index(k)
                if(j+1 <= len(self.gramatica[i])-1):
                    if(self.gramatica[i][j+1] in self.first):
                        if('@' not in self.first[self.gramatica[i][j+1]]):
                            t = (self.first[self.gramatica[i][j+1]])
                            for elemento in t:
                                valor.add(elemento)
                        else:
                            n = j+1
                            flag = 0
                            while(n <= len(self.gramatica[i])-1):
                                t = self.first[self.gramatica[i][n]]
                                if('@' in self.first[self.gramatica[i][n]]):
                                    t.remove('@')
                                    for elemento in t:
                                        valor.add(elemento)
                                else:
                                    for elemento in t:
                                        valor.add(elemento)
                                    flag = 1
                                    break
                                n = n+1
                            if(flag == 0 and self.gramatica[i][0] != self.gramatica[i][n-1] and self.gramatica[i][n-1] in self.no_terminales ):
                                self.escribir_follow(self.gramatica[i][0],valor)
                            else:
                                t = self.first[self.gramatica[i][n-1]]
                                for elemento in t:
                                    valor.add(elemento)

                elif(len(self.gramatica[i])-1 == j+1 and self.gramatica[i][0] != self.gramatica[i][j+1]):     
                    t = self.first[self.gramatica[i][j+1]]
                    if('@' in t):
                        t.remove('@')
                        for elemento in t:
                            valor.add(elemento)
                        self.escribir_follow(self.gramatica[i][0],valor)
                    else:
                        for elemento in t:
                            valor.add(elemento)
                else:
                    if(len(self.follow[self.gramatica[i][0]])):
                        t = self.follow[self.gramatica[i][0]]
                        for elemento in t:
                            valor.add(elemento)
                    else:
                        self.escribir_follow(self.gramatica[i][0],valor)
        return valor


    def encontrar_first(self):
        for i in range(len(self.no_terminales )):
            valor = set()
            self.first[self.no_terminales [i]] = self.escribir_first(self.no_terminales [i],valor,2)
        for i in range(len(self.terminales)):
            valor = set()
            valor.add(self.terminales[i])
            self.first[self.terminales[i]] = valor
        print("First: ", self.first)


    def encontrar_follow(self):
        for k in self.no_terminales :
            valor = set()
            self.follow[k] = self.escribir_follow(k,valor)
        print("Follow : " , self.follow)

    def create_tabla_de_parseo(self):
        head = self.terminales
        head.insert(len(self.terminales),'$')
        self.tabla_de_parseo['NT/T'] = head
        alerta = 0

        for i in self.no_terminales :
            lista_final = dict()
            final = list()
            for rule in range(len(self.gramatica)):
                if i == self.gramatica[rule][0]:
                    if('@' not in self.gramatica[rule]):   
                        t = self.first[self.gramatica[rule][0]]
                        for elemento in t:
                            if(self.gramatica[rule][2] == elemento):
                                if(head.index(elemento) in lista_final):
                                    alerta = 1
                                else:
                                    lista_final[head.index(elemento)] = self.gramatica[rule]
                            else:
                                t_nt = self.first[self.gramatica[rule][2]]  
                                if('@' in t_nt):
                                    t_nt.remove('@')
                                if(elemento in t_nt):
                                    if(head.index(elemento) in lista_final):
                                        alerta = 1
                                    else:
                                        lista_final[head.index(elemento)] = self.gramatica[rule]
                    else: 
                        t_fol = self.follow[self.gramatica[rule][0]]
                        for elemento in t_fol:
                            if(head.index(elemento) in lista_final):
                                    alerta = 1
                            else:
                                lista_final[head.index(elemento)] = self.gramatica[rule]
            for fl in range(0,len(head)):
                if(fl in lista_final):
                    final.append(lista_final[fl])
                else:
                    final.append('0')
            self.tabla_de_parseo[i] = final
        if(alerta == 1):
            print("No cumple con una gramatica")
        else:
            print()
            print("Tabla de Parseo: \n")
            for i in self.tabla_de_parseo:
                print(i,"\t",self.tabla_de_parseo[i])



if __name__ == "__main__":
    Parseo = Build_Parser()
