from OriginalScanner import *
import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *
import numpy as np
#tokenizar = Token()
class Tabla_de_Simbolos( object ):
   terminales     = [ ]    
   pragmas       = [ ]
   no_terminales  = [ ]
   original_token   = 0   # original a|b
   token_class   = 1   # digit{digit}
   token_operador      = 2   # operadores while if try
   clase_literales_tokens = 3   # letter {letter} 
   def __init__( self, typ, nombre, linea ):
      assert isinstance( typ, int )
      assert isinstance( nombre, (str,unicode) )
      assert isinstance( linea, int )
      self.n             = 0    
      self.typ           = 0      
      self.nombre          = 0     
      self.graph         = None    
      self.tipo_token     = 0       
      self.eliminar     = False   
      self.primero_listo    = False  
      self.primero         = None   
      self.follow        = None    
      self.nts           = None    
      self.linea          = 0      
      self.posicion_atributo       = None    
      self.posicion_semantica        = None                           
      self.tipo_output       = ''     
      self.tipo_atributo        = None   
      self.symnombre       = None   
      if len(nombre) == 2 and nombre[0] == '"':
         nombre = '???'
      self.typ = typ
      self.nombre = nombre
      self.linea = linea

      #if typ == Node.t:
      #   self.n = len(Symbol.terminales)
      #   Symbol.terminales.append( self )
      #elif typ == Node.pr:
      #   Symbol.pragmas.append( self )
      #elif typ == Node.nt:
      #   self.n = len(Symbol.no_terminales)
      #   Symbol.no_terminales.append( self )

   @staticmethod
   def Buscar( nombre ):
      assert isinstance( nombre, ( str, unicode ) )

      for s in Symbol.terminales:
         if s.nombre == nombre:
            return s

      for s in Symbol.no_terminales:
         if s.nombre == nombre:
            return s

      return None

   def comparar( self, x ):
      assert isinstance( x, Symbol )
      return self.nombre.__cmp__( x.nombre )
archivo_seleccionado = open("seleccionar_archivo.txt", "r+")
archivo_seleccionado = archivo_seleccionado.read()
archivo_para_scanner = open(archivo_seleccionado, 'r')
lineas = archivo_para_scanner.readlines()
archivo_para_scanner.close()
index_caracteres = lineas.index("CHARACTERS\n") + 1
index_palabras_clave = lineas.index("KEYWORDS\n")
index_tokens = lineas.index("TOKENS\n")
index_producciones = lineas.index("PRODUCTIONS\n")

corte_caracteres = lineas[index_caracteres:index_palabras_clave]
corte_caracteres = quitar_caracteres_inecesarios(corte_caracteres)
corte_de_palabras_clave = lineas[index_palabras_clave+1:index_tokens]
corte_de_palabras_clave = quitar_caracteres_inecesarios(corte_de_palabras_clave)
corte_de_tokens = lineas[index_tokens+1:index_producciones]
corte_de_tokens = quitar_caracteres_inecesarios(corte_de_tokens)
corte_caracteres = cortar_lista(corte_caracteres)
corte_de_palabras_clave = process_palabras_clave(corte_de_palabras_clave)
corte_de_tokens = procesar_tokens(corte_de_tokens)
corte_caracteres = [x for x in corte_caracteres if x!= ['']]
corte_de_palabras_clave = [x for x in corte_de_palabras_clave if x!= ['']]
corte_de_tokens = [x for x in corte_de_tokens if x!= ['']]

for i, j in enumerate(corte_caracteres):
   for k, l in enumerate(j):
      if '+' in l:
         rehacer = deepcopy(l.split('+'))
         corte_caracteres[i][k] = rehacer[0]
         corte_caracteres[i].append(rehacer[1])

with open("Textos_Generados/analizador_lexico.txt", "a+") as txt_file:
    corte_caracteres_finales = [] 
    txt_file.write("CORTE DE CARACTERES\n")
    txt_file.write("__________________________________\n")
    corte_caracteres_finales = corte_caracteres
    print("CORTE CARACTERES", corte_caracteres)
    corte_caracteres_finales = np.array(corte_caracteres)
    def column(matrix, i):
       return [row[i] for row in matrix]
    corte_caracteres_finales2 = column(corte_caracteres, 1)
    #print("CORTE CARACTERES FINALES 2", corte_caracteres_finales2)
    
    for line in corte_caracteres:
        txt_file.write("".join(line) + "\n")
    txt_file.write("----------------------------------\n")
    txt_file.write("CONDICIONALES\n")
    txt_file.write("__________________________________\n")
    
    for line in corte_de_palabras_clave:
        txt_file.write("".join(line) + "\n")
    
    txt_file.write("----------------------------------\n")
    txt_file.write("TOKENS\n")
    txt_file.write("__________________________________\n")
    for line in corte_de_tokens:
        txt_file.write("".join(line) + "\n") 
        final = "".join(line)
        print("token", final)
    txt_file.write("----------------------------------\n")



for elem in range(len(corte_caracteres)):
    if len(corte_caracteres[elem]) == 3:
        marcar_nodo = tokenizar.crear_nodo()
        marcar_nodo.nombre = corte_caracteres[elem][0]
        for elem2 in range(1, len(corte_caracteres[elem])-1):
            corte_caracteres[elem][elem2] = corte_caracteres[elem][elem2].replace('"', '')
            corte_caracteres[elem][elem2] = corte_caracteres[elem][elem2].replace('"', '')
            corte_caracteres[elem][elem2+1] = corte_caracteres[elem][elem2+1].replace('"', '')
            corte_caracteres[elem][elem2+1] = corte_caracteres[elem][elem2+1].replace('"', '')
            todas_las_listas = [primera_lista+segunda_lista for primera_lista in corte_caracteres[elem][elem2] for segunda_lista in corte_caracteres[elem][elem2+1]]
        marcar_nodo.contenido = deepcopy(todas_las_listas)
        tokenizar.caracteres.append(marcar_nodo)
    elif len(corte_caracteres[i]) >= 4:
       marcar_nodo = tokenizar.crear_nodo()
       marcar_nodo.data = corte_caracteres[i][0]
       marcar_nodo.contenido = [''.join(corte_caracteres[i][1:])]
       tokenizar.caracteres.append(marcar_nodo)

for i in range(len(corte_caracteres)):
    if len(corte_caracteres[i]) == 2:
        marcar_nodo = tokenizar.crear_nodo()
        marcar_nodo.nombre = corte_caracteres[i][0]
        marcar_nodo.contenido = [corte_caracteres[i][1]]
        tokenizar.caracteres.append(marcar_nodo)
    else:
        for j in range(len(corte_caracteres[i])):
            for index_nodo in tokenizar.caracteres:
                if index_nodo.nombre == corte_caracteres[i][j]:
                    corte_caracteres[i][j] = index_nodo.contenido[0]


for sblista in corte_de_palabras_clave:
    tokenizar.palabras_clave[corte_de_palabras_clave[corte_de_palabras_clave.index(sblista)][0]] = corte_de_palabras_clave[corte_de_palabras_clave.index(sblista)][1]
    
for index_nodo in tokenizar.caracteres:
    if len(index_nodo.contenido) ==1:
        dobles = list(index_nodo.contenido[0])
        for elemento in dobles:
            if elemento == '"' or elemento =='.':
                dobles.remove(elemento)
            if ord(elemento) == 34:
                dobles.remove(elemento)
        index_nodo.contenido = [''.join(dobles)]


for sblista in corte_de_palabras_clave:
    tokenizar.palabras_clave[corte_de_palabras_clave[corte_de_palabras_clave.index(sblista)][0]] = corte_de_palabras_clave[corte_de_palabras_clave.index(sblista)][1]
for llave in tokenizar.palabras_clave.keys():
    limpieza = tokenizar.palabras_clave.get(llave, '')
    if limpieza[0] == '"' and limpieza[-1] == '"' :
        limpieza = limpieza[1:-1]
        tokenizar.palabras_clave[llave] = limpieza

for indice, sblista in enumerate(corte_de_tokens):
    marcar_nodo = tokenizar.crear_nodo()
    marcar_nodo.nombre = sblista[0]
    for indice2, sbstring in enumerate(sblista):
        if '}' in sbstring:
            print("sbstring",sbstring)
            again = deepcopy(sbstring[sbstring.index('{')+1:sbstring.index('}')])
            print("again", again)
            sbstring = sbstring[:sbstring.index('{')] + ' ' + again + '* '  + sbstring[sbstring.index('}')+1:]
            sbstring = sbstring.replace('{', '(')
            sbstring = sbstring.replace('}', ')*')
            sbstring = sbstring.replace('"', '')
            sbstring = sbstring.replace('.', '')
            #sbstring = sbstring[:sbstring.index('{')] + '' + again + '*' + sbstring[sbstring.index('}')+1]
            #sbstring = again + ' ' + again + '* '  + sbstring[sbstring.index('}')+1:]
    marcar_nodo.contenido = sbstring
    tokenizar.tokens.append(marcar_nodo)


for primer_token in tokenizar.tokens:
    for segundo_token in tokenizar.caracteres:
        primer_contenido = primer_token.contenido.split()
        for por_cada_palabra in primer_contenido:
            if segundo_token.nombre == por_cada_palabra:
                if len(segundo_token.contenido) == 1:
                    primer_token.contenido = primer_token.contenido.replace(segundo_token.nombre, segundo_token.contenido[0])
                #elif segundo_token.data in por_cada_palabra:
                #   if por_cada_palabra[por_cada_palabra.index(segundo_token.data)-1] == '|':
                #      primer_token.contenido = primer_token.contenido.replace(segundo_token.data, segundo_token.contenido[0])
                else:
                    crear = ' '.join([str(elem) for elem in segundo_token.contenido])
                    crear = crear.replace(' ', '')
                    primer_token.contenido = primer_token.contenido.replace(segundo_token.nombre, crear)
                    primer_token.contenido = primer_token.contenido.replace('"', '')
            elif segundo_token.nombre in por_cada_palabra:
               if por_cada_palabra[por_cada_palabra.index(segundo_token.nombre)-1] == '|':
                  primer_token.contenido = primer_token.contenido.replace(segundo_token.nombre, segundo_token.contenido[0])


for indice, sblista in enumerate(tokenizar.tokens_excepto):
    for indice2, nod in enumerate(tokenizar.tokens):
        if nod.nombre == sblista[0]:
            nod.excepciones = sblista[1:]
      
cantidad = len(tokenizar.tokens)
print("Cantidad de Tokens:", cantidad)
cantidad = cantidad
tokenizar.marcar_nodos(tokenizar.tokens)
arreglo_todos_los_automatas = []
for i in range(cantidad):
    print("i", i )
    valor = tokenizar.tokens[i].contenido.strip()
    valor2 = valor 
    print("VALORINICIAL", valor)
    i = i +1
    print("CORTE CARACTERES FINALES 2!!!", corte_caracteres_finales2)
    valor = valor.replace(' ', '(')
    valor = valor.replace("*", ")*")
    for elemento_array in corte_caracteres_finales2:
       elemento_array = elemento_array.replace("'", "")
       elemento_array = elemento_array.replace('"', "")
       print("PALABRA_SACADA", elemento_array )
       if elemento_array.isdigit() == True:
          print("TEST TRUE",elemento_array)
          sacar_integer = "(" + str(i) + "|" + str(i) + ")"
          print("TEST INTEGER", sacar_integer)
          valor = valor.replace(elemento_array, sacar_integer)
          print("CAMBIO VALOR", valor)
       if elemento_array.isdigit() == False:
          print("TEST FALSE", elemento_array)
          elemento_array = elemento_array.replace('.', "")
          valor = valor.replace(elemento_array, '(a|b)')
          print("CAMBIO VALOR", valor )
           
    print("VALOR", valor)
    valortest = valor 
    valortest = valortest.replace("("," ")
    valortest = valortest.replace(")","")
    valortest = valortest.replace("|","")
    print("VALOR CORTADITO", valortest[0])
    if len(valortest[1]) > 2:
       print("VALOR QUE LE FALTA", valortest[1]) 
    print("VALORTEST", valortest)
    expresion_regular = valor
    print("QUE ENTRO", expresion_regular)
    arreglo_todos_los_automatas.append(expresion_regular)
    
    if "?" in expresion_regular:
       expresion_regular.replace("?", "|e")
    if "ε" in expresion_regular:
       expresion_regular.replace("ε", "@")
    a = Thmp(expresion_regular)
    sacar_variable =a.FunctionsNFA()
    sacar_variable2 = a.InEnd()
    #graficar_AFNVS2(sacar_variable,sacar_variable2)
    generacion_de_archivo_AFN(sacar_variable,sacar_variable2)
    print("|------------Subconjuntos--------------|")
    b = Subconjunto(a.afn)
    sacar_variable =b.TransposicionFinalAFD()
    sacar_variable2 = b.InEndAFD()
    graficar_AFDFinal(sacar_variable,sacar_variable2,str(i))
    generacion_de_archivo_afd_test(sacar_variable,sacar_variable2)
    print("|------------MINIMIZACION--------------|")
    b.minimizador()
    sacar_variable =b.TransposicionFinalMIN()
    sacar_variable2 = b.InEndMIN()
    graficar_MINVS2(sacar_variable,sacar_variable2,str(i))
    generacion_de_archivo_min(sacar_variable,sacar_variable2)
    keypass = open("expresion_regular.txt", "w")
    keypass.write(expresion_regular)
    keypass.close()
    

print("LISTA DE TODOS LOS AUTOMATAS", arreglo_todos_los_automatas )
fullStr = '|'.join('("' + item + '")' for item in arreglo_todos_los_automatas)
print("LISTA DE TODOS LOS AUTOMATAS2", fullStr )
fullStr = fullStr.replace('"',"")
print("LISTA DE TODOS LOS AUTOMATAS3", fullStr )
expresion_regular = fullStr
expresion_regular = expresion_regular.replace('ε', 'e')
print("-------------------------------------------------------")
first_char = expresion_regular[0]
print('First character : ', first_char)
if first_char in "()":
   print("|------------Thompson--------------|")
   if "?" in expresion_regular:
      expresion_regular.replace("?", "|e")
   if "ε" in expresion_regular:
      expresion_regular.replace("ε", "@")
   a = Thmp(expresion_regular)
   sacar_variable =a.FunctionsNFA()
   sacar_variable2 = a.InEnd()
   print("|------------Subconjuntos--------------|")
   b = Subconjunto(a.afn)
   sacar_variable =b.TransposicionFinalAFD()
   sacar_variable2 = b.InEndAFD()
   graficar_Automaton(sacar_variable,sacar_variable2)
   generacion_de_archivo_Automaton(sacar_variable,sacar_variable2)
   print("|------------MINIMIZACION--------------|")
   b.minimizador()
   sacar_variable =b.TransposicionFinalMIN()
   sacar_variable2 = b.InEndMIN()
   graficar_Automaton_MIN(sacar_variable,sacar_variable2)
   generacion_de_archivo_Automaton_MIN(sacar_variable,sacar_variable2)
    #keypass = open("expresion_regular.txt", "w")
    #keypass.write(expresion_regular)
    #keypass.close()
	

archivo_seleccionado = open("OriginalScanner.py", "r+")
archivo_seleccionado = archivo_seleccionado.read()
print("Inicio de Modificacion del Scanner")
#print(archivo_seleccionado)
keypass_01 = open("NewScanner.py", "w")
keypass_01.write(archivo_seleccionado)
keypass_01.close()
'''
    def AbrirGenerador(backUp):
      assert isinstance(backUp,bool)
      try:
         fn = FILE.srcDir + "Scanner.py"   # String
         if backUp and os.path.exists(fn):
            if os.path.exists(fn + '.old'):
               os.remove( fn + '.old' )
            os.rename( fn, fn + '.old' )
         FILE.gen = file( fn, 'w' )
      except:
         raise RuntimeError("-- Compiler Error: Cannot generate scanner file.")

   @staticmethod
   def EscribirScanner( AllNombres):
      assert isinstance(AllNombres,bool)
      startTab = [ 0 for i in xrange(CharClass.charSetSize) ]
      fr = FILE.srcDir + "OriginalScanner.py"   # String
      if not os.path.exists( fr ):
         if Tab.frameDir is not None:
            fr = os.path.join( Tab.frameDir.strip(), "OriginalScanner.py" )
         if not os.path.exists(fr):
            raise RuntimeError("-- Compiler Error: Cannot find OriginalScanner.py")
      try:
         FILE.fram = file( fr, 'r' )
      except:
         raise RuntimeError("-- Compiler Error: Cannot open OriginalScanner.py.")
      FILE.AbrirGenerador(True)
      if FILE.dirtyFILE:
         FILE.MakeDeterministic( )
      FILE.FillStartTab(startTab)
      FILE.CopyFramePart( "#!inicio" )
      if not FILE.srcName.lower( ).endswith( 'coco.atg' ):
         FILE.gen.close()
         FILE.AbrirGenerador(False)

      FILE.CopyFramePart("#!declaraciones")
      FILE.gen.write("   charSetSize = " + str(CharClass.charSetSize) + '\n')
      FILE.gen.write("   maxT = "        + str(len(Symbol.terminals) - 1) + '\n')
      FILE.gen.write("   noSym = "       + str(Tab.noSym.n) + '\n')
      if AllNombres:
         FILE.gen.write("   # terminals\n")
         for sym in Symbol.terminals:
            FILE.gen.write("   " + sym.symName + " = " + str(sym.n) + '\n')
         FILE.gen.write("   # pragmas\n")
         for sym in Symbol.pragmas:
            FILE.gen.write("   " + sym.symName + " = " + str(sym.n) + '\n')
         FILE.gen.write( '\n' )
      FILE.gen.write("   start = [\n")
      for i in xrange(0,CharClass.charSetSize / 16):
         FILE.gen.write("   ")
         for j in xrange(0,16):
            FILE.gen.write(Trace.formatString(str(startTab[16*i+j]), 3))
            FILE.gen.write(",")
         FILE.gen.write( '\n' )
      FILE.gen.write("     -1]\n")

      if FILE.ignoreCase:
         FILE.gen.write("   valCh = u''       # current input character (for token.val)")

      FILE.CopyFramePart("#!inicializacion")
      j = 0
      for i in Tab.ignored:
         FILE.gen.write("      self.ignore.add(" + str(i) + ") \n")

      FILE.CopyFramePart("#!nextcharcas")
      if FILE.ignoreCase:
         FILE.gen.write("      valCh = self.ch\n")
         FILE.gen.write("      if self.ch != Buffer.EOF:\n")
         FILE.gen.write("         self.ch = self.ch.lower()\n");

      FILE.CopyFramePart("#!comentarios")
      com = Comment.first   # Comment
      i = 0
      while com is not None:
         FILE.GenComment(com, i)
         com = com.next
         i += 1

      FILE.CopyFramePart("#!inicio_literales")
      FILE.GenLiterals()

      FILE.CopyFramePart("#!scan01")
      if Comment.first!=None:
         FILE.gen.write("if (")
         com = Comment.first
         i = 0
         while com is not None:
            FILE.gen.write(FILE.ChCond(com.start[0]))
            FILE.gen.write(" and self.Comment" + str(i) + "()")
            if com.next is not None:
               FILE.gen.write(" or ")
            com = com.next
            i += 1
         FILE.gen.write("):\n")
         FILE.gen.write("         return self.NextToken()\n")
      if FILE.hasCtxMoves:
         FILE.gen.write('\n')
         FILE.gen.write("      apx = 0")

      FILE.CopyFramePart("#!scan02")
      if FILE.ignoreCase:
         FILE.gen.write("buf += unicode(self.ch)\n")
         FILE.gen.write("      self.NextCh()\n")
      else:
         FILE.gen.write("buf += unicode(self.ch)\n")
         FILE.gen.write("      self.NextCh()\n")

      FILE.CopyFramePart("#!scan03")
      state = FILE.firstState.next
      while state is not None:
         FILE.gen.write("         elif state == ")
         FILE.WriteState(state)
         state = state.next
      FILE.CopyFramePart("#!final")
      FILE.gen.close()
'''
print("+ analizador lexico generado")





