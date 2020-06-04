#begin
import sys
from OriginalScanner import Token
from OriginalScanner import Escaner
from OriginalScanner import Posicion

class Parser( object ):
#!constantes
   T= True
   x= False
   distancia_minima_de_error = 2

#!declarations
   def __init__( self ):
      self.escaner= None
      self.token= None          
      self.lookahead_token= None           
      self.escaner_generado  = False
      self.string_del_token = ''             
      self.tokens_literales= '-none-'       
      self.error_de_distancia= Parser.distancia_minima_de_error

   def obtener_posicion_del_parser( self ):
      return self.lookahead_token.tipo_token, self.lookahead_token.columna_token

   def sincronizar_errores( self, error_numeral ):
      if self.error_de_distancia >= Parser.distancia_minima_de_error:
         print("errores de sync")

      self.error_de_distancia = 0

   def error_semantico( self, mensaje ):
      if self.error_de_distancia >= Parser.distancia_minima_de_error:
         print("Errores semanticos")

      self.error_de_distancia = 0

   def mensaje_de_aviso( self, mensaje ):
      if self.error_de_distancia >= Parser.distancia_minima_de_error:
         print("advertir errores")

      self.error_de_distancia = 0

   def logro_entrar_el_mensaje( self ):
       print("contador de errores")

   def string_lexico( self ):
      return self.token.token_valor

   def string_look_ahead( self ):
      return self.lookahead_token.token_valor

   def Get( self ):
      while True:
         self.token = self.lookahead_token
         self.lookahead_token = self.escaner.Scan( )
         if self.lookahead_token.tipo_token <= Parser.maxT:
            self.error_de_distancia += 1
            break
#!pragmas
         self.lookahead_token = self.token

   def Expect( self, i ):
      if self.lookahead_token.tipo_token == i:
         self.Get( )
      else:
         self.sincronizar_errores(i)

   def Marcar_inicio( self,i):
      return self.set[i][self.lookahead_token.tipo_token]

   def Esperar_Bajo( self, n, follow ):
      if self.lookahead_token.tipo_token == n:
         self.Get( )
      else:
         self.sincronizar_errores( n )
         while not self.Marcar_inicio(follow):
            self.Get( )

   def separador_bajo( self, n, syFollow, repFollow ):
      a = [ False for i in xrange( Parser.maxT+1 ) ]
      if self.lookahead_token.tipo_token == n:
         self.Get( )
         return True
      elif self.Marcar_inicio(repFollow):
         return False
      else:
         for i in xrange( Parser.maxT ):
            a[i] = self.set[syFollow][i] or self.set[repFollow][i] or self.set[0][i]
         self.sincronizar_errores( n )
         while not a[self.lookahead_token.tipo_token]:
            self.Get( )
         return self.Marcar_inicio( syFollow )

   def Expr():
        
       while (get() ==";" or get() =="."):
           if( get() ==";"):
               Stat (";")

           if( get() =="."):
               Stat (";")


   def Stat ():
       value=0
 

   def Expression (result):
       result1=0 
       result2=0

       while (get() =="+" or get() =="-"):
           if( get() =="+"):
               Term(result2)
               result1+=result2

           if( get() =="-"):
               Term(result2)
               result1-=result2

   def Term(result):
       result1=0 
       result2=0

       while (get() =="*" or get() =="/"):
           if( get() =="*"):
               Factor(result2)
               result1*=result2

           if( get() =="/"):
               Factor(result2)
               result1/=result2

   def Factor (result):
       signo=1

   def Number (result):
       number(result=0)


   def Parsear( self, escaner ):
      self.escaner = escaner
      self.lookahead_token = Token( )
      self.lookahead_token.token_valor = u''
      self.Get( )
#!parseRoot

   set = [
#!initialization
      ]

   mensaje_de_error = {
#!errors
      }
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


