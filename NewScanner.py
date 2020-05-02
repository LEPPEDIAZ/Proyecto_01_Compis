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

   def Peak( self ):
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
   maxT=6

   noSym=   maxT=6


   digit="0123456789"
   tab="\\t"
   eol="\\n"
   blanco="\\n  \\r  \\t"
   zero=digit
   one=tab
   two=eol
   three=blanco
   transposicion=[[1, zero, 2], [1, three, 3], [3, three, 4], [4, three, 4], [2, zero, 5], [5, zero, 6], [6, zero, 6]]
   print(transposicion)
   number =[digit]
   decnumber =[digit]
   white =[blanco]
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
      self.PeakDeTokenActual = self.corriente_de_tokens     

   def Siguiente_Caracter( self ):
      if self.AntiguoEols > 0:
         self.ch = Escaner.EOL
         self.AntiguoEols -= 1
      else:
         self.ch = self.buffer.Read( )
         self.posicion_token += 1
      
         if (self.ch == u'\r') and (self.buffer.Peak() != u'\n'):
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
      #!scan02
      listo = False
      while not listo:
         if state == -1:
            self.t.tipo_token = Escaner.eofSym     
            listo = True
         elif state == 0:
            self.t.tipo_token = Escaner.noSym      
            listo = True
         elif state ==1:
            if self.ch =='zero':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=2
            elif self.ch =='three':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=3
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==2:
            if self.ch =='zero':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=5
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==3:
            if self.ch =='three':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=4
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==4:
            if self.ch =='three':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=4
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==5:
            if self.ch =='zero':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=6
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==6:
            if self.ch =='zero':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=6

      self.t.val = buf
      return self.t

   def Escanear( self ):
      self.t = self.t.next
      self.PeakDeTokenActual = self.t.next
      return self.t

   def Peak( self ):
      self.PeakDeTokenActual = self.PeakDeTokenActual.next
      while self.PeakDeTokenActual.kind > self.maxT:
         self.PeakDeTokenActual = self.PeakDeTokenActual.next

      return self.PeakDeTokenActual

   def reiniciar( self ):
      self.PeakDeTokenActual = self.t
   
   def convert(lst):
      return ([i for item in lst for i in item.split()]) 
   

   def unique(list1):
      unique_list = [] 
      for x in list1:
         if x not in unique_list:
            unique_list.append(x)
      for x in unique_list:
         print (x)
   new_lineas = []
   new_lineas.append(lineas)
   lista_de_palabras = convert(new_lineas)
   arreglo_con_todos_los_tokens = [] 
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

   for i in decnumber :
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

   for i in white :
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
   transposicion_number =[[1, '0', 2], [2, '0', 3], [3, '0', 3]]
   transposicion_decnumber =[[1, '0', 2], [2, '0', 3], [3, '0', 4], [4, '0', 4]]
   transposicion_white =[[1, '3', 2], [2, '3', 3], [3, '3', 3]]
   inicialfinal_number =[[1, 2]]
   inicialfinal_decnumber =[[1, 3]]
   inicialfinal_white =[[1, 2]]
#!final
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
