#!inicio
import sys

class Token( object ):
   def __init__( self ):
      self.tipo_token   = 0    
      self.posicion_token    = 0     
      self.columna_token    = 0    
      self.token_linea   = 0    
      self.token_valor    = u''   
      self.linked_list   = None  


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

   def Revision( self ):
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

#!declaraciones

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
      self.RevisionDeTokenActual = self.corriente_de_tokens     

   def Siguiente_Caracter( self ):
      if self.AntiguoEols > 0:
         self.ch = Escaner.EOL
         self.AntiguoEols -= 1
      else:
         self.ch = self.buffer.Read( )
         self.posicion_token += 1
      
         if (self.ch == u'\r') and (self.buffer.Revision() != u'\n'):
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
            self.t.kind = Escaner.eofSym     
            listo = True
         elif state == 0:
            self.t.kind = Escaner.noSym      
            listo = True
#!scan03
      self.t.val = buf
      return self.t

   def Escanear( self ):
      self.t = self.t.next
      self.RevisionDeTokenActual = self.t.next
      return self.t

   def Revision( self ):
      self.RevisionDeTokenActual = self.RevisionDeTokenActual.next
      while self.RevisionDeTokenActual.kind > self.maxT:
         self.RevisionDeTokenActual = self.RevisionDeTokenActual.next

      return self.RevisionDeTokenActual

   def reiniciar( self ):
      self.RevisionDeTokenActual = self.t

#!final
