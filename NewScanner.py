#!inicio
import sys
from copy import deepcopy
with open("Textos_Generados/analizador_lexico.txt", "w") as txt_file:
         txt_file.write("ANALIZADOR LEXICO\n")
         txt_file.write("_____________________________________________\n")
         txt_file.write("_____________________________________________\n")
ver_archivo = input("Ingrese el archivo del cual desea ver tokens:  ")
archivo_para_scanner = open(ver_archivo, 'r')
lineas = archivo_para_scanner.readlines()
lineas = ", ".join(lineas)
archivo_para_scanner.close()
class Nodos():
    arreglo_nodo = []
    ntipo = ["    ", "t   ", "pr  ", "nt  ", "clas", "chr ", "wt  ", "any ", "eps ","sync", "sem ", "alt ", "iter", "opt ", "rslv"]
    simbolo_de_terminal    =  1 
    pragma   =  2  
    no_terminal  =  3  
    clase_de_caracter =  4  
    charac  =  5  
    simbolo_terminal_debil   =  6  
    any_sim =  7  
    vacio  =  8  
    sync_simbolo =  9  
    accion_semantica  = 10  
    alternativo  = 11  
    iteracion = 12  
    opcion  = 13  
    resolver_expresion = 14
    transicion_normal  = 0
    contextTrans = 1
    def __init__(self, typ, symOrNodeOrInt, line=None):
        assert isinstance( typ, int )
        assert isinstance( line, int ) or (line is None)
        self.typ   =  0
        self.nombre = ''
        self.contenido = []
        self.excepciones = [] 
    @staticmethod
    def DelGrafico( p ):
       return (p is None) or Nodos.DelNodos(p) and Nodos.DelGrafico(p.linked_list)

    @staticmethod
    def DelSbGrafo( p ):
       return p is None or Nodos.DelNodos(p) and (p.up or Nodos.DelSbGrafo(p.linked_list))

    @staticmethod
    def DelA( p ):
       return p is None or Nodos.DelNodos(p) and (p.up or Nodos.DelA(p.linked_list))

    @staticmethod
    def DelNodos( p ):
       if p.typ == Nodos.nt:
          return p.sym.deletable
       elif p.typ == Nodos.alt:
          return Nodos.DelA( p.sub ) or p.down != None and Nodos.DelA(p.down)
       else:
          return p.typ in ( Nodos.eps, Nodos.iter, Nodos.opt, Nodos.sem, Nodos.sync, Nodos.rslv )

class Token( object ):
   def __init__( self ):
      self.tipo_token   = 0    
      self.posicion_token    = 0     
      self.columna_token    = 0    
      self.token_linea   = 0    
      self.token_valor    = u''   
      self.linked_list   = None 
      self.caracteres = []
      self.palabras_clave = {}
      self.tokens = []
      self.producciones = []
      self.tokens_excepto = []
   def crear_nodo(self):
        marcar_nodo = Nodos(0,0,0)
        return marcar_nodo

   def marcar_nodos(self, definir_lista):
      arreglo_contenido = []
      arreglo_nombre = []
      nombreend = []
      contenidoend = []
      excepcionesend = [] 
      if definir_lista != self.palabras_clave:
         for index_nodo in definir_lista:
            lindo = ("----------------------------")
            nombrefinal = (str(index_nodo.nombre))
            nombreend.append(nombrefinal)
            contenidofinal = (str(index_nodo.contenido) )
            contenidoend.append(contenidofinal)
            arreglo_contenido.append(contenidofinal)
            excepcionesfinal = (str(index_nodo.excepciones))
            excepcionesend.append(excepcionesfinal)
            lindo2 = ("----------------------------\n")
            #keypass_01.close()
      else:
         print(definir_lista)
      print("PROBAR ARREGLO")
      with open("Textos_Generados/analizador_lexico.txt", "a+") as txt_file:
         txt_file.write("NOMBRE\n")
         txt_file.write("__________________________________\n")
         for line in nombreend:
            txt_file.write("".join(line) + "\n")
         txt_file.write("----------------------------------\n")
         txt_file.write("CONTENIDO\n")
         txt_file.write("__________________________________\n")
         for line in contenidoend:
            txt_file.write("".join(line) + "\n") 
         txt_file.write("----------------------------------\n")
         txt_file.write("EXCEPCION\n")
         txt_file.write("__________________________________\n")
         for line in excepcionesend:
            txt_file.write("".join(line) + "\n") 
         txt_file.write("----------------------------------\n")
    

    
         
class Posicion( object ):    
   def __init__( self, buf, inicio, len, col ):
      assert isinstance( buf, Buffer )
      assert isinstance( inicio, int )
      assert isinstance( len, int )
      assert isinstance( col, int )

      self.buf = buf
      self.inicio = inicio   
      self.len = len  
      self.columna_token = col   

   def ObtenerSubcadena( self ):
      return self.buf.leer_posicion( self )

class Buffer( object ):
   EOF      = u'\u0100'   

   def __init__( self, s ):
      self.buf    = s
      self.largo_buffer = len(s)
      self.posicion_token    = 0
      self.token_lineas  = s.splitlines( True )

   def Read( self ):
      if self.posicion_token < self.largo_buffer:
         result = self.buf[self.posicion_token]
         self.posicion_token += 1
         return result
      else:
         return Buffer.EOF

   def LeerCaracteres( self, numero_bytes=1 ):
      result = self.buf[ self.posicion_token : self.posicion_token + numero_bytes ]
      self.posicion_token += numero_bytes
      return result

   def Peek( self ):
      if self.posicion_token < self.largo_buffer:
         return self.buf[self.posicion_token]
      else:
         return Escaner.buffer.EOF

   def ObtenerString( self, inicio, end ):
      s = ''
      oldPos = self.ObtenerPosicion( )
      self.setPos( inicio )
      while inicio < end:
         s += self.Read( )
         inicio += 1
      self.setPos( oldPos )
      return s

   def ObtenerPosicion( self ):
      return self.posicion_token

   def determinar_posicion( self, valor ):
      if valor < 0:
         self.posicion_token = 0
      elif valor >= self.largo_buffer:
         self.posicion_token = self.largo_buffer
      else:
         self.posicion_token = valor

   def leer_posicion( self, pos ):
      assert isinstance( pos, Posicion )
      self.determinar_posicion( pos.inicio )
      return self.LeerCaracteres( pos.len )

   def __iter__( self ):
      return iter(self.token_lineas)

class Escaner(object):
   EOL     = u'\n'
   eofSym  = 0
   H = "H"
   maxT=23
   noSym=   maxT=23

   letterLo="az"
   letterUp="AZ"
   letter="azAZ"
   vowels="aeiouAEIOU"
   consonants="letter-vowels"
   digit="0123456789"
   sign="-"
   hexdigit="0123456789ABCDEF"
   tab="CHR(9)"
   eol="CHR(10)"
   space="CHR(32)"
   whitespace="CHR(13)CHR(10)CHR(9)"
   zero=letterLo
   one=letterUp
   two=vowels
   three=consonants
   four=sign
   five=hexdigit
   six=tab
   seven=eol
   eight=whitespace
   nine=letter
   onezero=digit
   oneone=space
   transposicion=[[1, eight, 2], [1, five, 3], [1, nine, 4], [1, four, 5], [1, one, 6], [6, zero, 7], [7, one, 8], [7, zero, 9], [9, zero, 9], [8, zero, 10], [10, one, 11], [11, zero, 12], [12, one, 11], [5, one, 13], [13, zero, 14], [14, one, 15], [15, zero, 16], [16, one, 15], [4, nine, 17], [4, one, 18], [18, zero, 19], [19, nine, 20], [19, one, 18], [20, nine, 20], [20, one, 18], [17, nine, 17], [17, one, 18], [3, five, 21], [3, H, 22], [21, five, 21], [21, H, 22], [2, eight, 23], [23, eight, 23]]
   print(transposicion)
   string =[letter,letter]
   name =[letterUp,letterLo,letterLo]
   var =[letter,letter+digit,digit]
   signInt =[sign,digit,digit]
   int =[digit,digit]
   float =[digit,digit,digit,digit]
   hexnumber =[hexdigit,hexdigit,H,]
   space =[whitespace,whitespace]
   key_if="if"
   if key_if in lineas:
      print("KEYWORD:", key_if)
      lineas = lineas.replace(key_if, "")

   key_while="while"
   if key_while in lineas:
      print("KEYWORD:", key_while)
      lineas = lineas.replace(key_while, "")

   key_switch = "switch"
   if key_switch  in lineas:
      print("KEYWORD:", key_switch )
      lineas = lineas.replace(key_switch , "")

   key_do = "do"
   if key_do  in lineas:
      print("KEYWORD:", key_do )
      lineas = lineas.replace(key_do , "")

   key_for = "for"
   if key_for  in lineas:
      print("KEYWORD:", key_for )
      lineas = lineas.replace(key_for , "")

   key_exit = "exit"
   if key_exit  in lineas:
      print("KEYWORD:", key_exit )
      lineas = lineas.replace(key_exit , "")

   key_class = "class"
   if key_class  in lineas:
      print("KEYWORD:", key_class )
      lineas = lineas.replace(key_class , "")

   key_import = "import"
   if key_import  in lineas:
      print("KEYWORD:", key_import )
      lineas = lineas.replace(key_import , "")

   key_from = "from"
   if key_from  in lineas:
      print("KEYWORD:", key_from )
      lineas = lineas.replace(key_from , "")

   key_try = "try"
   if key_try  in lineas:
      print("KEYWORD:", key_try )
      lineas = lineas.replace(key_try , "")

   key_except = "except"
   if key_except  in lineas:
      print("KEYWORD:", key_except )
      lineas = lineas.replace(key_except , "")

   key_lambda = "lambda"
   if key_lambda  in lineas:
      print("KEYWORD:", key_lambda )
      lineas = lineas.replace(key_lambda , "")


   def __init__( self, s ):
      self.buffer = Buffer( unicode(s) ) 
      self.ch        = u'\0'       
      self.posicion_token       = -1         
      self.token_linea      = 1           
      self.linea_de_inicio = 0      
      self.antiguos_n   = 0           
      self.Siguiente_Caracter( )
      self.ignorar    = set( )      
      self.ignorar.add( ord(' ') )  
#!inicializacion
      self.corriente_de_tokens = Token( )       
      nodo   = self.corriente_de_tokens

      nodo.linked_list = self.Siguiente_Token( )
      nodo = nodo.linked_list
      while nodo.tipo_token != Escaner.eofSym:
         nodo.linked_list = self.Siguiente_Token( )
         nodo = nodo.linked_list

      nodo.linked_list = nodo
      nodo.val  = u'EOF'
      self.t  = self.corriente_de_tokens    
      self.PeekDeTokenActual = self.corriente_de_tokens     

   def Siguiente_Caracter( self ):
      self.ch = self.buffer.Read( )
      self.posicion_token += 1
      if (self.ch == u'\r') and (self.buffer.Peek() != u'\n'):
         self.ch = Escaner.EOL
      if self.ch == Escaner.EOL:
         self.token_linea += 1
         self.linea_de_inicio = self.posicion_token + 1
      #!nextcharcas


#!comentarios

   def CheckLiteral( self ):
      print("")
      #!inicio_literales

   def Siguiente_Token( self ):
      while ord(self.ch) in self.ignorar:
         self.Siguiente_Caracter( )
      #!scan01
      self.t = Token( )
      self.t.pos = self.posicion_token
      self.t.col = self.posicion_token - self.linea_de_inicio + 1
      self.t.line = self.token_linea
      if ord(self.ch) < len(self.transposicion):
         state = self.transposicion[ord(self.ch)]
      else:
         state = 0
      buf = u''
      buf += unicode(self.ch)
      self.Siguiente_Caracter()
      zero_array=[]
      zero_array+=zero
      one_array=[]
      one_array+=one
      two_array=[]
      two_array+=two
      three_array=[]
      three_array+=three
      four_array=[]
      four_array+=four
      five_array=[]
      five_array+=five
      six_array=[]
      six_array+=six
      seven_array=[]
      seven_array+=seven
      eight_array=[]
      eight_array+=eight
      nine_array=[]
      nine_array+=nine
      one_arrayzero_array=[]
      one_arrayzero_array+=onezero
      one_arrayone_array=[]
      one_arrayone_array+=oneone
      listo = False
      while not listo:
         if state == -1:
            self.t.tipo_token = Escaner.eofSym     
            listo = True
         elif state == 0:
            self.t.tipo_token = Escaner.noSym      
            listo = True
         elif state ==1:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=2
            elif self.ch in five_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=3
            elif self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=4
            elif self.ch in four_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=5
            elif self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=6
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==10:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=11
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==11:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=12
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==12:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=11
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==13:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=14
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==14:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=15
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==15:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=16
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==16:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=15
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==17:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=17
            elif self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=18
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==18:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=19
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==19:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=20
            elif self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=18
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==2:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=23
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==20:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=20
            elif self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=18
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==21:
            if self.ch in five_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=21
            elif self.ch in H:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=22
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==23:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=23
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==3:
            if self.ch in five_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=21
            elif self.ch in H:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=22
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==4:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=17
            elif self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=18
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==5:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==6:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=7
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==7:
            if self.ch in one_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=8
            elif self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=9
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==8:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=10
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==9:
            if self.ch in zero_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=9

      self.t.val = buf
      return self.t

   def Escanear( self ):
      self.t = self.t.linked_list
      self.PeekDeTokenActual = self.t.linked_list
      return self.t

   def Peek( self ):
      self.PeekDeTokenActual = self.PeekDeTokenActual.linked_list
      while self.PeekDeTokenActual.tipo_token > self.maxT:
         self.PeekDeTokenActual = self.PeekDeTokenActual.linked_list

      return self.PeekDeTokenActual

   def reiniciar( self ):
      self.PeekDeTokenActual = self.t
   
   def convert(lst):
      return ([i for item in lst for i in item.split()]) 
   

   def unique(list1):
      unique_list = [] 
      for x in list1:
         if x not in unique_list:
            unique_list.append(x)
      for x in unique_list:
         print (x)

   lineas = lineas.replace(" ", " # ")
   new_lineas = []
   new_lineas.append(lineas)
   new_lista_de_palabras = convert(new_lineas)
   lista_de_palabras = []
   for i in new_lista_de_palabras:
      if i == "#":
         i = i.replace("#", " ")
      lista_de_palabras.append(i)
   arreglo_con_todos_los_tokens = [] 

   for i in string :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in name :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in var :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in signInt :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in int :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in float :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in hexnumber :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)

   for i in space :
      lista_creada = list(i)
      arreglo_nuevo = []
      for j in lista_creada:
         for k in lista_de_palabras:
            arreglo_test = []
            lista_creada2 = list(k)
            for n in lista_creada2:
               if n in lista_creada:
                  arreglo_test.append(True)
               if n not in lista_creada:
                  arreglo_test.append(False)
            if all(arreglo_test) == True:
               salvar_valor = "Token:"+ k  
               arreglo_con_todos_los_tokens.append(salvar_valor)
   unique(arreglo_con_todos_los_tokens)
   transposicion_string =[[1, one, 2], [2, zero, 3], [3, zero, 4], [4, zero, 4]]
   transposicion_name =[[1, five, 2], [2, five, 3], [2, 'H', 4], [3, five, 3], [3, 'H', 4]]
   transposicion_var =[[1, eight, 2], [2, eight, 3], [3, eight, 3]]
   transposicion_signInt =[[1, nine, 2], [2, nine, 3], [3, nine, 3]]
   transposicion_int =[[1, nine, 2], [2, nine, 3], [2, one, 4], [4, zero, 5], [5, nine, 3], [5, one, 4], [3, nine, 3], [3, one, 4]]
   transposicion_float =[[1, four, 2], [2, one, 3], [3, zero, 4], [4, one, 5], [5, zero, 6], [6, one, 5]]
   transposicion_hexnumber =[[1, one, 2], [2, zero, 3], [3, one, 4], [4, zero, 5], [5, one, 4]]
   transposicion_space =[[1, one, 2], [2, zero, 3], [3, one, 4], [4, zero, 5], [5, one, 6], [6, zero, 7], [7, one, 6]]
   inicialfinal_string =[[1, 3]]
   inicialfinal_name =[[1, 4]]
   inicialfinal_var =[[1, 2]]
   inicialfinal_signInt =[[1, 2]]
   inicialfinal_int =[[1, 5]]
   inicialfinal_float =[[1, 4]]
   inicialfinal_hexnumber =[[1, 3]]
   inicialfinal_space =[[1, 5]]
   arreglo_con_todos_los_tokens2 = []
   for i in inicialfinal_string :
      for j in transposicion_string :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_name :
      for j in transposicion_name :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_var :
      for j in transposicion_var :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_signInt :
      for j in transposicion_signInt :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_int :
      for j in transposicion_int :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_float :
      for j in transposicion_float :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_hexnumber :
      for j in transposicion_hexnumber :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   for i in inicialfinal_space :
      for j in transposicion_space :
         if(i[0] == j[0] and i[1] == j[2]):
            lista_creada = []
            for i in j[1] :
               lista_creada.append(i)
            for j in lista_creada:
               for k in lista_de_palabras:
                  arreglo_test = []
                  lista_creada2 = list(k)
                  for n in lista_creada2:
                     if n in lista_creada:
                        arreglo_test.append(True)
                     if n not in lista_creada:
                        arreglo_test.append(False)
                  if all(arreglo_test) == True:
                     salvar_valor = 'Token_VS2:'+ k 
                     arreglo_con_todos_los_tokens2.append(salvar_valor)

   print("-------------------------VS2 ----------------------------------")
   unique(arreglo_con_todos_los_tokens2)

#!final
   error_validator =str(letterLo)+str(letterUp)+str(vowels)+str(consonants)+str(sign)+str(hexdigit)+str(tab)+str(eol)+str(whitespace)+str(letter)+str(digit)+str(space)
   lineas2 = lineas.replace(' ', '')
   lineas2 = lineas.replace('#', '')
   for i in lineas2:
      if i not in error_validator:
         if i != " ":
            print("ERROR!: Se ingreso un caracter no valido" , i)

tokenizar = Token()

def procesar_tokens(lista_de_tokens):
        for sbstring in lista_de_tokens:
            lista_de_tokens[lista_de_tokens.index(sbstring)] = sbstring.split('=')
        for sblista in lista_de_tokens:
                for sbstring in sblista:
                    if 'EXCEPT' in sbstring:
                        proceso_inmediato = deepcopy(sbstring)
                        proceso_inmediato = proceso_inmediato.split()
                        tokenizar.tokens_excepto.append([sblista[0], proceso_inmediato[proceso_inmediato.index('EXCEPT')+1].lower()])
                        destruir = deepcopy(proceso_inmediato)
                        destruir = destruir[:destruir.index('EXCEPT')]
                        lista_de_tokens[lista_de_tokens.index(sblista)] = [lista_de_tokens[lista_de_tokens.index(sblista)][0], destruir[0]]
        return lista_de_tokens

def quitar_caracteres_inecesarios(lista):
    lista = [str.rstrip(x, '\n') for x in lista]
    lista = [str.rstrip(x, '.') for x in lista]

    return lista

def process_palabras_clave(llave):
    for sbstring in llave:
        llave[llave.index(sbstring)] = sbstring.split('=')
    return llave

def cortar_lista(lista):
    lista = [i.split('=') for i in lista]
    for sblista in lista:
        for indx, texto in enumerate(sblista):
            if '+' in list(texto):
                cortar = list(texto)
                cortar = [cortar[:cortar.index('+')], cortar[cortar.index('+') + 1:]]
                arreglo1 = []
                for i in range(len(cortar)):
                    primer_string = ""
                    cortar[i] = [i for i in cortar[i] if i != ' ']
                    cortar[i] = primer_string.join(cortar[i])
                    arreglo1.append(cortar[i])
                arreglo1.insert(0, sblista[0])
                lista[lista.index(sblista)] = arreglo1
            if ' ' in list(texto):
                segundo_string = ""
                espacio_vacio = list(texto)
                espacio_vacio = [i for i in espacio_vacio if i != ' ']
                espacio_vacio = segundo_string.join(espacio_vacio)
                sblista[indx] = espacio_vacio
    return lista
