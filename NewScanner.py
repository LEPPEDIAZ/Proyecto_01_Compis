#!inicio
import sys
from copy import deepcopy
with open("Textos_Generados/analizador_lexico.txt", "w") as txt_file:
         txt_file.write("ANALIZADOR LEXICO\n")
         txt_file.write("_____________________________________________\n")
         txt_file.write("_____________________________________________\n")
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
   maxT=18
   noSym=   maxT=18

   digit="0123456789"
   tab="\\t"
   eol="\\n"
   blanco="\\n  \\r  \\t"
   one=digit
   a=tab
   b=eol
   c=blanco
   two=digit
   b=tab
   c=eol
   d=blanco
   three=digit
   c=tab
   d=eol
   e=blanco
   transposicion=[[1, b, 2], [1, two, 3], [1, one, 4], [4, one, 5], [5, one, 5], [3, two, 6], [6, two, 7], [7, two, 7], [2, l, 8], [8, a, 9], [9, n, 10], [10, c, 11], [11, o, 12], [12, b, 13], [13, l, 14], [14, a, 15], [15, n, 16], [16, c, 17], [17, o, 18], [18, b, 13]]
   print(transposicion)

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
            if self.ch ==b:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=2
            elif self.ch =='two':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=3
            elif self.ch =='one':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=4
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==10:
            if self.ch ==c:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=11
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==11:
            if self.ch ==o:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=12
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==12:
            if self.ch ==b:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==13:
            if self.ch ==l:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=14
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==14:
            if self.ch ==a:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=15
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==15:
            if self.ch ==n:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=16
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==16:
            if self.ch ==c:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=17
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==17:
            if self.ch ==o:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=18
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==18:
            if self.ch ==b:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=13
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==2:
            if self.ch ==l:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=8
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==3:
            if self.ch =='two':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=6
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==4:
            if self.ch =='one':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=5
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==5:
            if self.ch =='one':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=5
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==6:
            if self.ch =='two':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=7
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==7:
            if self.ch =='two':
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=7
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==8:
            if self.ch ==a:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=9
            else:
               self.t.tipo_token= Escaner.noSym 
               done = True
         elif state ==9:
            if self.ch ==n:
               buf += unicode(self.ch)
               self.Siguiente_Caracter()
               state=10

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
