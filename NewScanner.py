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
       return (p is None) or Nodos.DelNodos(p) and Nodos.DelGrafico(p.next)

    @staticmethod
    def DelSbGrafo( p ):
       return p is None or Nodos.DelNodos(p) and (p.up or Nodos.DelSbGrafo(p.next))

    @staticmethod
    def DelA( p ):
       return p is None or Nodos.DelNodos(p) and (p.up or Nodos.DelA(p.next))

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
   maxT=14
   noSym=   maxT=14

   upletter="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   downletter="abcdefghijklmnopqrstuvwxyz"
   letter="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZdownletter"
   digit="0123456789"
   hexdigit="0123456789ABCDEF"
   hexterm="H"
   tab="CHR(9)"
   eol="CHR(10)"
   whitespace="CHR(13)CHR(10)CHR(9)"
   sign="-"
   zero=upletter
   one=downletter
   two=hexdigit
   three=hexterm
   four=tab
   five=eol
   six=whitespace
   seven=sign
   eight=letter
   nine=digit
   transposicion=[[1, eight, 2], [1, two, 3], [1, six, 4], [1, nine, 5], [1, seven, 6], [6, nine, 7], [7, nine, 8], [8, nine, 8], [5, nine, 9], [9, nine, 9], [4, six, 10], [10, six, 10], [3, three, 11], [3, two, 12], [12, three, 11], [12, two, 12], [2, eight, 13], [2, nine, 14], [14, eight, 13], [14, nine, 14], [13, eight, 13], [13, nine, 14]]
   print(transposicion)
   ident =[letter,letter+digit]
   hexnumber =[hexdigit,hexdigit,hexterm]
   number =[digit,digit]
   signnumber =[sign,digit,digit]
   whitetoken =[whitespace,whitespace]
   key_while = "while"
   if key_while  in lineas:
      print("KEYWORD:", key_while )
      lineas = lineas.replace(key_while , "")

   key_do = "do"
   if key_do  in lineas:
      print("KEYWORD:", key_do )
      lineas = lineas.replace(key_do , "")


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

      nodo.next = self.Siguiente_Token( )
      nodo = nodo.next
      while nodo.kind != Escaner.eofSym:
         nodo.next = self.Siguiente_Token( )
         nodo = nodo.next

      nodo.next = nodo
      nodo.val  = u'EOF'
      self.t  = self.corriente_de_tokens    
      self.PeekDeTokenActual = self.corriente_de_tokens     

   def Siguiente_Caracter( self ):
      if self.AntiguoEols > 0:
         self.ch = Escaner.EOL
         self.AntiguoEols -= 1
      else:
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
      if ord(self.ch) < len(self.start):
         state = self.start[ord(self.ch)]
      else:
         state = 0
      buf = u''
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
            elif self.ch in two_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=3
            elif self.ch in six_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=4
            elif self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=5
            elif self.ch in seven_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=6
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==10:
            if self.ch in six_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=10
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==12:
            if self.ch in three_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=11
            elif self.ch in two_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=12
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==13:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            elif self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=14
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==14:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            elif self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=14
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==2:
            if self.ch in eight_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            elif self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=14
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==3:
            if self.ch in three_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=11
            elif self.ch in two_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=12
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==4:
            if self.ch in six_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=10
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==5:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=9
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==6:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=7
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==7:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=8
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==8:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=8
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==9:
            if self.ch in nine_array:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=9

      self.t.val = buf
      return self.t

   def Escanear( self ):
      self.t = self.t.next
      self.PeekDeTokenActual = self.t.next
      return self.t

   def Peek( self ):
      self.PeekDeTokenActual = self.PeekDeTokenActual.next
      while self.PeekDeTokenActual.kind > self.maxT:
         self.PeekDeTokenActual = self.PeekDeTokenActual.next

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

   for i in ident :
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

   for i in number :
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

   for i in signnumber :
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

   for i in whitetoken :
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
   transposicion_ident =[[1, two, 2], [2, two, 3], [2, three, 4], [3, two, 3], [3, three, 4]]
   transposicion_hexnumber =[[1, six, 2], [2, six, 3], [3, six, 3]]
   transposicion_number =[[1, eight, 2], [2, nine, 3], [2, eight, 4], [4, nine, 3], [4, eight, 4], [3, nine, 3], [3, eight, 4]]
   transposicion_signnumber =[[1, nine, 2], [2, nine, 3], [3, nine, 3]]
   transposicion_whitetoken =[[1, seven, 2], [2, nine, 3], [3, nine, 4], [4, nine, 4]]
   inicialfinal_ident =[[1, 4]]
   inicialfinal_hexnumber =[[1, 2]]
   inicialfinal_number =[[1, 2]]
   inicialfinal_signnumber =[[1, 2]]
   inicialfinal_whitetoken =[[1, 3]]
   arreglo_con_todos_los_tokens2 = []
   for i in inicialfinal_ident :
      for j in transposicion_ident :
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

   for i in inicialfinal_number :
      for j in transposicion_number :
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

   for i in inicialfinal_signnumber :
      for j in transposicion_signnumber :
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

   for i in inicialfinal_whitetoken :
      for j in transposicion_whitetoken :
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
   error_validator =str(upletter)+str(downletter)+str(hexdigit)+str(hexterm)+str(tab)+str(eol)+str(whitespace)+str(sign)+str(letter)+str(digit)
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
