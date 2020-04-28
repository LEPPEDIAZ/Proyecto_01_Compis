from OriginalScanner import *
import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *
import numpy as np
import string
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
    print("CORTE CARACTERES VIEW", corte_caracteres_finales2)
    corte_caracteres_finales_header = column(corte_caracteres, 0)
    print("CORTE CARACTERES VIEW 2", corte_caracteres_finales_header)
    
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
terminales_finales = []
guardar_estados_transformados = []
guardar_estados_transformados_2 = [] 
guardar_estados_en_DFA = []
arreglo_de_inicio_finales = [] 
d = dict(enumerate(string.ascii_lowercase, 1))
for i in range(cantidad):
    print("i", i )
    valor = tokenizar.tokens[i].contenido.strip()
    valor2 = valor 
    print("VALORINICIAL", valor)
    i = i +1
    print("CORTE CARACTERES FINALES 2!!!", corte_caracteres_finales2)
    valor = valor.replace(' ', '(')
    valor = valor.replace("*", ")*")
    posicion_actual = -1
    for elemento_array in corte_caracteres_finales2:
       posicion_actual = posicion_actual + 1
       print("VER QUE POSICION ESTA", posicion_actual)
       sacar_token_name = corte_caracteres_finales_header[posicion_actual]
       print("ARRAY OBTENIDO", sacar_token_name)
       elemento_array = elemento_array.replace("'", "")
       elemento_array = elemento_array.replace('"', "")
       print("PALABRA_SACADA", elemento_array )
       if elemento_array.isdigit() == True:
          print("TEST TRUE",elemento_array)
          sacar_integer = "(" + str(i) + "|" + str(i) + ")"
          print("TEST INTEGER", sacar_integer)
          valor = valor.replace(elemento_array, sacar_integer)
          print("CAMBIO VALOR", valor)
          valor_guardado = elemento_array + "=" + str(i)
          guardar_estados_transformados.append(valor_guardado)
          guardar_estados_en_DFA.append(i)
          valor_guardado_2 = str(i) + "=" + sacar_token_name
          guardar_estados_transformados_2.append(valor_guardado_2)
       if elemento_array.isdigit() == False:
          alfabeto = d[int(i)]
          i = i+1
          alfabeto2 = d[int(i)]
          sacar_integer = "(" + alfabeto + "|" + alfabeto2 + ")"
          print("ALFABETO", sacar_integer)
          print("TEST FALSE", elemento_array)
          elemento_array = elemento_array.replace('.', "")
          valor = valor.replace(elemento_array, sacar_integer)
          print("CAMBIO VALOR", valor )
          valor_guardado = elemento_array + "=" + alfabeto
          guardar_estados_transformados.append(valor_guardado)
          guardar_estados_en_DFA.append(alfabeto)
          valor_guardado2 = elemento_array + "=" + alfabeto2
          guardar_estados_transformados.append(valor_guardado2)
          guardar_estados_en_DFA.append(alfabeto2)
          valor_guardado2_2 = alfabeto + "=" + sacar_token_name
          guardar_estados_transformados_2.append(valor_guardado2_2)
          valor_guardado2_3 = alfabeto2 + "=" + sacar_token_name
          guardar_estados_transformados_2.append(valor_guardado2_3)
           
    print("VALOR", valor)
    print("Relacion de valor de token con valor de automatas", guardar_estados_transformados)
    print("relacion de nombre de token con valor de automatas", guardar_estados_transformados_2)
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
    arreglo_de_inicio_finales.append(sacar_variable2)
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
   variable_transposicion = b.TransposicionFinalAFD()
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
   print("Sacar terminales finales", sacar_variable2)
    #keypass = open("expresion_regular.txt", "w")
    #keypass.write(expresion_regular)
    #keypass.close()

def declarar_variables_de_inicializacion ():
   buscar_ultimo_estado = max(variable_transposicion)	
   values1 = '\n'.join(str(v) for v in buscar_ultimo_estado)
   values1 = values1[0] + values1[1]
   values1 = "maxT" + "=" + values1 + "\n"
   values2 = "noSym" + "=" + values1 + "\n"
   print("TERMINALES FINALES", arreglo_de_inicio_finales)
   archivo_seleccionado = open("OriginalScanner.py", "r+")
   archivo_seleccionado = archivo_seleccionado.read()
   print("Inicio de Modificacion del Scanner")
   print("CORTE", corte_caracteres)
   primero_01 = [i[0] for i in corte_caracteres]
   segundo_02 = [i[1:] for i in corte_caracteres]
   concat_matrix = "\n".join([str(a.replace("'","")) + "="+ '"' + str(b) + '"' for a,b in zip(primero_01,segundo_02)])
   print("concat_matrix", concat_matrix)
   values = concat_matrix
   values = values.replace("[", "")
   values = values.replace("]", "")
   values = values.replace("',", " ")
   values = values.replace("'", "")
   values = values.replace('""', '"')
   values = values.replace('" ', '')
   values = values.replace('.', '')
   print("RESULTADO", values)
   declaracion_string = ("\n".join(guardar_estados_transformados_2))
   declaracion_string = declaracion_string.replace("1", "one")
   declaracion_string = declaracion_string.replace("2", "two")
   declaracion_string = declaracion_string.replace("3", "three")
   declaracion_string = declaracion_string.replace("4", "four")
   declaracion_string = declaracion_string.replace("5", "five")
   declaracion_string = declaracion_string.replace("6", "six")
   declaracion_string = declaracion_string.replace("7", "seven")
   declaracion_string = declaracion_string.replace("8", "eight")
   declaracion_string = declaracion_string.replace("9", "nine")

   print("TRANSPOSICION",variable_transposicion )
   print("ESTADOS ACTUALES", guardar_estados_en_DFA)
   transposicion_show = str(variable_transposicion)
   transposicion_show = transposicion_show.replace("'1'", "one")
   transposicion_show = transposicion_show.replace("'2'", "two")
   transposicion_show = transposicion_show.replace("'3'", "three")
   transposicion_show = transposicion_show.replace("'4'", "four")
   transposicion_show = transposicion_show.replace("'5'", "five")
   transposicion_show = transposicion_show.replace("'6'", "six")
   transposicion_show = transposicion_show.replace("'7'", "seven")
   transposicion_show = transposicion_show.replace("'8'", "eight")
   transposicion_show = transposicion_show.replace("'9'", "nine")
   transposicion_show = transposicion_show.replace("'", "")
   start_declaration = "transposicion=" + transposicion_show + "\n" + "print(" + "transposicion" + ")"
   todo_limpio = values1 + values2 + values + "\n" + declaracion_string +  "\n" + start_declaration
   archivo_seleccionado = archivo_seleccionado.replace("#!declaraciones", todo_limpio)
   keypass_01 = open("NewScanner.py", "w")
   keypass_01.write(archivo_seleccionado)
   keypass_01.close()

declarar_variables_de_inicializacion()
print("+ analizador lexico generado")





