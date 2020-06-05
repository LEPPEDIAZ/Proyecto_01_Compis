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

#!productions

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
   archivo_seleccionado = open("grammar_values.txt", "r+")
   archivo_seleccionado = archivo_seleccionado.read()
   x = archivo_seleccionado.split(",")
   #print("Arreglo", x)
   reglas = open("reglas.txt", "r+")
   reglas = reglas.read()
   follows = open("follows.txt", "r+")
   follows = follows.read()
   firsts = open("firsts.txt", "r+")
   firsts = firsts.read()
   n = -1 
   for i in x:
      n = n + 1 
      #get_index = (archivo_seleccionado.index(i))
      print("VALUE:   " + str(n) + "      " + i)
      
 
   print("-----------------------------------------")
   reglas = reglas.replace("\n", " ")
   reglas = reglas.replace("\t", " ")
   print("REGLAS", reglas)
   print("-----------------------------------------")
   follows = follows.replace("\n", " ")
   follows = follows.replace("\t", " ")
   print("FOLLOW", follows)
   print("-----------------------------------------")
   firsts = firsts.replace("\n", " ")
   firsts = firsts.replace("\t", " ")
   print("FIRSTS", firsts)
   
   
      



