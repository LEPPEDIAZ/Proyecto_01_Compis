from OriginalScanner import *
import sys
import os
from expresion_regular import *
from generadorAFN import *
from AFD_por_AFN import *
import numpy as np
import string
import textwrap
os.system("python3 ManageProductions.py")
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
print("CORTE DE CARACTERES BUSCAR", corte_caracteres)
corte_caracteres = quitar_caracteres_inecesarios(corte_caracteres)
corte_de_palabras_clave = lineas[index_palabras_clave+1:index_tokens]
corte_de_palabras_clave = quitar_caracteres_inecesarios(corte_de_palabras_clave)
corte_de_tokens = lineas[index_tokens+1:index_producciones]
arreglo_tokens_limpios = corte_de_tokens 
print("ARREGLO LIMPIO DE TOKENS", arreglo_tokens_limpios)
corte_de_tokens = quitar_caracteres_inecesarios(corte_de_tokens)
arreglo_tokens_limpios2 = corte_de_tokens
print("ARREGLO LIMPIO DE TOKENS2", arreglo_tokens_limpios2)
corte_caracteres = cortar_lista(corte_caracteres)
print("CORTE DE CARACTERES BUSCAR2", corte_caracteres)
arreglo_tokens_limpios3 = corte_de_tokens
arreglo_con_key = str(arreglo_tokens_limpios3)
arreglo_test_key = []
arreglo_test_key.append(arreglo_con_key)
print("ARREGLO LIMPIO DE TOKENS3", str(arreglo_test_key))
corte_de_palabras_clave = process_palabras_clave(corte_de_palabras_clave)
corte_de_tokens = procesar_tokens(corte_de_tokens)
arreglo_tokens_limpios4 = corte_de_tokens
print("ARREGLO LIMPIO DE TOKENS4", arreglo_tokens_limpios4)
corte_caracteres = [x for x in corte_caracteres if x!= ['']]
corte_de_palabras_clave = [x for x in corte_de_palabras_clave if x!= ['']]
corte_de_tokens = [x for x in corte_de_tokens if x!= ['']]
arreglo_tokens_limpios5 = corte_de_tokens
print("ARREGLO LIMPIO DE TOKENS5", arreglo_tokens_limpios5)

for i, j in enumerate(corte_caracteres):
   for k, l in enumerate(j):
      if '+' in l:
         rehacer = deepcopy(l.split('+'))
         corte_caracteres[i][k] = rehacer[0]
         corte_caracteres[i].append(rehacer[1])
arreglo_de_tokens = []
with open("Textos_Generados/analizador_lexico.txt", "a+") as txt_file:
    corte_caracteres_finales = [] 
    txt_file.write("CORTE DE CARACTERES\n")
    txt_file.write("__________________________________\n")
    corte_caracteres_finales = corte_caracteres
    print("CORTE CARACTERES!!!!!!", corte_caracteres)
    sacar_inicio_caracteres = corte_caracteres
    print("CORTE CARACTERES2!!!!!!", sacar_inicio_caracteres)

    corte_caracteres_finales = np.array(corte_caracteres)
    primer_caracter_header = [i[0] for i in corte_caracteres]
    primer_caracter_valor = [i[1:] for i in corte_caracteres]
    print("CARACTER HEADER TEST",primer_caracter_header )
    print("CARACTER HEADER VALOR", primer_caracter_valor)
    def column(matrix, i):
       return [row[i] for row in matrix]
    corte_caracteres_finales2 = column(corte_caracteres, 1)
    print("CORTE CARACTERES VIEW", corte_caracteres_finales2)

    corte_caracteres_finales_header = column(corte_caracteres, 0)
    print("CORTE CARACTERES VIEW 2", corte_caracteres_finales_header)
    sacar_nombre_de_caracteres = corte_caracteres_finales_header
    print("CORTE DE CARACTERES FINALES", sacar_nombre_de_caracteres )
    
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
    arreglo_tokens_con_valor = [] 
    for line in corte_de_tokens:
        arreglo_de_tokens.append(line)
        txt_file.write("".join(line) + "\n") 
        final = "".join(line)
        print("TOKENS OBTENIDOS", final)
        arreglo_tokens_con_valor.append(final)
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

#print("ARREGLO DE TOKENS", arreglo_de_tokens)
solo_tokens = [] 
for i in (arreglo_de_tokens):
	#print(i[1])
    solo_tokens.append(i[1])
print("solo tokens", solo_tokens)
arregloA = solo_tokens

# TODO: hexdigit no aparece aun
print("CORTE DE CARACTERES CON TODO", corte_caracteres)
primero_01 = [i[0] for i in corte_caracteres]
print("primero_01", sacar_nombre_de_caracteres)
arregloB = sacar_nombre_de_caracteres
segundo_02 = [i[1:] for i in corte_caracteres]


#print("segundo_02", segundo_02)
#concat_matrix = "\n".join([str("   " + a.replace("'","")) + "="+ '"' + str(b) + '"' for a,b in zip(primero_01,segundo_02)])
#print("DEFINICIONES", concat_matrix)

contained = []
for key in arregloB:
    for value in arregloB:
        if (key in value) and (key != value):
            str_contained = key
            contained.append(str_contained)

contained = list(dict.fromkeys(contained))

for i in range(len(contained)):
    for values in arregloB:
        if contained[i] == values:
            arregloB.pop(arregloB.index(values))
            arregloB.append(contained[i])

print(arregloB)

todos = []
todos_index = 0
for i in arregloB:
    for j in arregloA:
        if i in j:
            j_before = j
            cambiar = arregloB.index(i)
            j = j.replace(str(i), str(cambiar))
            j = j.replace("{", "(")
            j = j.replace("}", ")*")
            j = j.replace("|", "|")
            j = j.replace("[", "")
            j = j.replace("]", "")
            j = j.replace(".", "")
            j = j.replace('"', "")
            #print("ESTADOS FINALES",j)
            #print("index", i )
            todos.append(j)
            #print(j)
            arr_pos = arregloA.index(j_before)
            arregloA.pop(arr_pos)
            arregloA.insert(arr_pos, todos[todos_index])
            todos_index = todos_index + 1

print("ALL_FOR_IT", todos)

for poss_keys in arregloB:
    for poss_token in todos:
        if poss_keys in poss_token:
            todos.pop(todos.index(poss_token))

for poss_keys in arregloB:
    for poss_token in todos:
        if poss_keys in poss_token:
            todos.pop(todos.index(poss_token))

print("ALL_FOR_IT_2", todos)

arreglo_todos_los_tokens_transposicion = []
arreglo_todos_los_tokens_final_inicial = []
i_variable = 0 
for n in todos:
    i_variable = i_variable + 1
    print("N!$", n)
    n = n.replace(" ","")
    expresion_regular = n
    print("QUE ENTRO AUTOMATITOS", expresion_regular)
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
    #!graficar_AFDFinal(sacar_variable,sacar_variable2,str(i_variable))
    #!generacion_de_archivo_afd_test(sacar_variable,sacar_variable2)
    arreglo_de_inicio_finales.append(sacar_variable2)
    arreglo_todos_los_tokens_transposicion.append(sacar_variable)
    arreglo_todos_los_tokens_final_inicial.append(sacar_variable2)
print("todos los tokens transposicion",arreglo_todos_los_tokens_transposicion)
print("todos los tokens inicial y final",arreglo_todos_los_tokens_final_inicial)   

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
          #alfabeto2 = d[int(i)]
          #sacar_integer = "(" + alfabeto + "|" + alfabeto2 + ")"
          sacar_integer = "(" + alfabeto + "|" + alfabeto + ")"
          print("ALFABETO", sacar_integer)
          print("TEST FALSE", elemento_array)
          elemento_array = elemento_array.replace('.', "")
          valor = valor.replace(elemento_array, sacar_integer)
          print("CAMBIO VALOR", valor )
          valor_guardado = elemento_array + "=" + alfabeto
          guardar_estados_transformados.append(valor_guardado)
          guardar_estados_en_DFA.append(alfabeto)
          #valor_guardado2 = elemento_array + "=" + alfabeto2
          #guardar_estados_transformados.append(valor_guardado2)
          #guardar_estados_en_DFA.append(alfabeto2)
          valor_guardado2_2 = alfabeto + "=" + sacar_token_name
          guardar_estados_transformados_2.append(valor_guardado2_2)
          #valor_guardado2_3 = alfabeto2 + "=" + sacar_token_name
          #guardar_estados_transformados_2.append(valor_guardado2_3)
           
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
    #graficar_AFDFinal(sacar_variable,sacar_variable2,str(i))
    #generacion_de_archivo_afd_test(sacar_variable,sacar_variable2)
    #arreglo_de_inicio_finales.append(sacar_variable2)
    
    

print("LISTA DE TODOS LOS AUTOMATAS", todos )
fullStr = '|'.join('("' + item + '")' for item in todos)
print("LISTA DE TODOS LOS AUTOMATAS2", fullStr )
fullStr = fullStr.replace('"',"")
fullStr = fullStr.replace(" ","")
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
   


def declarar_variables_de_inicializacion ():
   print("sacar caracteres header inicializacion", primer_caracter_header)
   print("SACAR CARACTERES PARA INICIALIZACION", sacar_inicio_caracteres)
   buscar_ultimo_estado = max(variable_transposicion)	
   values1 = '\n'.join(str(v) for v in buscar_ultimo_estado)
   values1 = values1[0] + values1[1]
   values1 = "   "+"maxT" + "=" + values1 + "\n"
   values2 = "   "+"noSym" + "=" + values1 + "\n"
   print("TERMINALES FINALES", arreglo_de_inicio_finales)
   archivo_seleccionado = open("OriginalScanner.py", "r+")
   archivo_seleccionado = archivo_seleccionado.read()
   print("Inicio de Modificacion del Scanner")
   print("CORTE", corte_caracteres)
   primero_01 = [i[0] for i in corte_caracteres]
   segundo_02 = [i[1:] for i in corte_caracteres]
   print("produccciones", segundo_02)
   arreglo_value_char = []
   for i in segundo_02:
       arrayprod = []
       test = ("".join(i))
       test = test.replace('"',"")
       test = test.replace("'","")
       test = '"' + test + '"'
       arrayprod.append(test)
       arreglo_value_char.append(arrayprod)
   concat_matrix = "\n".join([str("   " + a.replace("'","")) + "="+ '"' + str(b) + '"' for a,b in zip(primer_caracter_header,arreglo_value_char)])
   print("concat_matrix_declare", concat_matrix)
   values = concat_matrix
   values = values.replace("[", "")
   values = values.replace("]", "")
   values = values.replace("',", " ")
   values = values.replace("'", "")
   #falta debuggear
   values = values.replace('""', '"')
   values = values.replace('" ', '')
   values = values.replace('.', '')
   print("RESULTADO", values)
   guardar_estados_transformados_2_nuevos = []
   for i in guardar_estados_transformados_2:
       print("PINTAR ELEMENTO",i)
       manage_tab = "   " + i
       guardar_estados_transformados_2_nuevos.append(manage_tab)
    
   declaracion_string = ("\n".join(guardar_estados_transformados_2_nuevos))
   declaracion_string = declaracion_string.replace("0", "zero")
   declaracion_string = declaracion_string.replace("1", "one")
   declaracion_string = declaracion_string.replace("2", "two")
   declaracion_string = declaracion_string.replace("3", "three")
   declaracion_string = declaracion_string.replace("4", "four")
   declaracion_string = declaracion_string.replace("5", "five")
   declaracion_string = declaracion_string.replace("6", "six")
   declaracion_string = declaracion_string.replace("7", "seven")
   declaracion_string = declaracion_string.replace("8", "eight")
   declaracion_string = declaracion_string.replace("9", "nine")

   print("PRIMER SACAR DECLARACIONES", sacar_nombre_de_caracteres)
   nueva_declaracion = []
   for i in sacar_nombre_de_caracteres:
       buscar_posicion = sacar_nombre_de_caracteres.index(i)
       buscar_posicion = str(buscar_posicion)
       buscar_posicion = buscar_posicion.replace('0',"zero")
       buscar_posicion = buscar_posicion.replace('1', "one")
       buscar_posicion = buscar_posicion.replace('2', "two")
       buscar_posicion = buscar_posicion.replace('3', "three")
       buscar_posicion = buscar_posicion.replace('4', "four")
       buscar_posicion = buscar_posicion.replace('5', "five")
       buscar_posicion = buscar_posicion.replace('6', "six")
       buscar_posicion = buscar_posicion.replace('7', "seven")
       buscar_posicion = buscar_posicion.replace('8', "eight")
       buscar_posicion = buscar_posicion.replace('9', "nine")
       nuevo_string = "   " + buscar_posicion + "=" + i
       print(nuevo_string)
       nueva_declaracion.append(nuevo_string)


   print("TRANSPOSICION",variable_transposicion )
   nueva_declaracion_string = ("\n".join(nueva_declaracion))
   print("ESTADOS ACTUALES", guardar_estados_en_DFA)
   transposicion_show = str(variable_transposicion)
   transposicion_show = transposicion_show.replace("'0'", "zero")
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
   start_declaration = "transposicion=" + transposicion_show + "\n" + "   "+  "print(" + "transposicion" + ")"
   todo_limpio = values1 + values2 + values + "\n" + nueva_declaracion_string +  "\n" + "   "+  start_declaration
   archivo_seleccionado = archivo_seleccionado.replace("#!declaraciones", todo_limpio)
   keypass_01 = open("NewScanner.py", "w")
   keypass_01.write(archivo_seleccionado)
   keypass_01.close()

def declarar_siguiente_caracter():
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    
    #transposicion_show = transposicion_show.replace("'", "")
    x = np.array(variable_transposicion)
    print("Ordenado",x)
    arreglo_estado_inicio = []
    arreglo_estado_inicio_limpio = [] 
    arreglo_estado_medio_final = []
    for i, j in enumerate(x):
        #print ("elif state ==" + j[0] + ":" + "\n")
        primer_elemento = ("elif state ==" + j[0] + ":" + "\n")
        arreglo_estado_inicio.append(":" + j[0] + ":")
        arreglo_estado_inicio_limpio.append(j[0])
        segundo_elemento = j[1]
        segundo_elemento = segundo_elemento.replace("0", "zero_array")
        segundo_elemento = segundo_elemento.replace("1", "one_array")
        segundo_elemento = segundo_elemento.replace("2", "two_array")
        segundo_elemento = segundo_elemento.replace("3", "three_array")
        segundo_elemento = segundo_elemento.replace("4", "four_array")
        segundo_elemento = segundo_elemento.replace("5", "five_array")
        segundo_elemento = segundo_elemento.replace("6", "six_array")
        segundo_elemento = segundo_elemento.replace("7", "seven_array")
        segundo_elemento = segundo_elemento.replace("8", "eight_array")
        segundo_elemento = segundo_elemento.replace("9", "nine_array")
        segundo_elemento = ":" + j[0] + ":" + "self.ch in " + segundo_elemento + ":" + "\n" + "               "+ "buf += unicode(self.ch)" + "\n" + "               " + "self.Siguiente_Caracter()"+ "\n" +"               "+ "state=" + j[2] + "\n"
        arreglo_estado_medio_final.append(segundo_elemento)
        #print(segundo_elemento)

    unicos_primer_elemento = np.unique(arreglo_estado_inicio)
    unicos_primer_elemento = np.array(unicos_primer_elemento)
    ordenar_unicos = np.sort(unicos_primer_elemento)

    unicos_primer_elemento1 = np.unique(arreglo_estado_inicio_limpio)
    unicos_primer_elemento1 = np.array(unicos_primer_elemento1)
    ordenar_unicos_limpios = np.sort(unicos_primer_elemento1)
    print("Valor unico primer_elemento", unicos_primer_elemento)
    print("ordenar valor unico primer_elemento", ordenar_unicos)
    print("test ordenar valor unico primer_elemento", ordenar_unicos_limpios)
    print("arreglo_estado_medio_final",arreglo_estado_medio_final)
    todo_scan3 = []
    test_change = 0
    for i in ordenar_unicos_limpios:
        #print( i + "!!!")
        inicio = i 
        i = ":" + i + ":"
        #inicio = inicio.replace(":", "")
        revisar = inicio
        inicio = "         "+"elif state ==" + inicio + ":" + "\n"
        print("i:" ,revisar )
        if (revisar == "1"):
            todo_scan3.append(inicio)
            print(inicio)
        if (revisar != "1"):
            add_else = "            "+ "else:" + "\n" + "               " + "self.t.tipo_token= Escaner.noSym " +  "\n" + "               " +"done = True" + "\n"
            inicio_2 = add_else + inicio
            todo_scan3.append(inicio_2)
            print(inicio_2)
        anterior = i
        for j in arreglo_estado_medio_final:
            if i in j:
                if (test_change) == inicio:
                    segundo_valor = j
                    segundo_valor = segundo_valor.replace(i, "")
                    segundo_valor = "            "+ "elif" + " " + segundo_valor
                    print(segundo_valor)
                    todo_scan3.append(segundo_valor)
                if (test_change) != inicio:
                    test_change = inicio
                    segundo_valor = j
                    segundo_valor = segundo_valor.replace(i, "")
                    segundo_valor = "            "+ "if" + " " + segundo_valor
                    print(segundo_valor)
                    todo_scan3.append(segundo_valor)
                test_change = inicio
                
                #print(j)
    print("------------------------------------")
    print(todo_scan3)
    new_text = "".join(todo_scan3)
    print(new_text) 
    archivo_seleccionado = archivo_seleccionado.replace("#!scan03", new_text)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()       
def input_de_archivo():
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    new_text = 'ver_archivo = input("Ingrese el archivo del cual desea ver tokens:  ")' + "\n" + "archivo_para_scanner = open(ver_archivo, 'r')" + "\n" + "lineas = archivo_para_scanner.readlines()" + "\n" + 'lineas = ", ".join(lineas)' + "\n"  + "archivo_para_scanner.close()"
    archivo_seleccionado = archivo_seleccionado.replace("#!leer_archivo!", new_text)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()       

def definiciones_de_tokens():
    print("tokens para pasar a definicon", arreglo_tokens_limpios5)
    print("sacar caracteres", sacar_nombre_de_caracteres)
    arreglo_limpio = [] 
    arreglo_limpio2 = [] 
    arreglo_headers = [] 
    for i in arreglo_tokens_limpios5:
        arreglo_por_valor = []
        arreglo_por_valor_2 = [] 
        valor_entrada = i[0]
        valor_entrada2 = i[1]
        valor_entrada2 = valor_entrada2.replace(" ", "")
        valor_entrada2 = valor_entrada2.replace('"', "")
        valor_entrada2 = valor_entrada2.replace('.', ",")
        valor_entrada2 = valor_entrada2.replace("{", ",")
        valor_entrada2 = valor_entrada2.replace("|", "+")
        valor_entrada2 = valor_entrada2.replace("}a", ",a")
        valor_entrada2 = valor_entrada2.replace("}b", ",b")
        valor_entrada2 = valor_entrada2.replace("}c", ",c")
        valor_entrada2 = valor_entrada2.replace("}d", ",d")
        valor_entrada2 = valor_entrada2.replace("}e", ",e")
        valor_entrada2 = valor_entrada2.replace("}f", ",f")
        valor_entrada2 = valor_entrada2.replace("}g", ",g")
        valor_entrada2 = valor_entrada2.replace("}h", ",h")
        valor_entrada2 = valor_entrada2.replace("}i", ",i")
        valor_entrada2 = valor_entrada2.replace("}j", ",j")
        valor_entrada2 = valor_entrada2.replace("}k", ",k")
        valor_entrada2 = valor_entrada2.replace("}l", ",l")
        valor_entrada2 = valor_entrada2.replace("}m", ",m")
        valor_entrada2 = valor_entrada2.replace("}n", ",n")
        valor_entrada2 = valor_entrada2.replace("}o", ",o")
        valor_entrada2 = valor_entrada2.replace("}p", ",p")
        valor_entrada2 = valor_entrada2.replace("}q", ",q")
        valor_entrada2 = valor_entrada2.replace("}r", ",r")
        valor_entrada2 = valor_entrada2.replace("}s", ",s")
        valor_entrada2 = valor_entrada2.replace("}t", ",t")
        valor_entrada2 = valor_entrada2.replace("}u", ",u")
        valor_entrada2 = valor_entrada2.replace("}v", ",v")
        valor_entrada2 = valor_entrada2.replace("}w", ",w")
        valor_entrada2 = valor_entrada2.replace("}x", ",x")
        valor_entrada2 = valor_entrada2.replace("}y", ",y")
        valor_entrada2 = valor_entrada2.replace("}z", ",z")
        valor_entrada2 = valor_entrada2.replace("}", "")
        valor_entrada2 = valor_entrada2.replace("a(", "a,")
        valor_entrada2 = valor_entrada2.replace("b(", "b,")
        valor_entrada2 = valor_entrada2.replace("c(", "c,")
        valor_entrada2 = valor_entrada2.replace("d(", "d,")
        valor_entrada2 = valor_entrada2.replace("e(", "e,")
        valor_entrada2 = valor_entrada2.replace("f(", "f,")
        valor_entrada2 = valor_entrada2.replace("g(", "g,")
        valor_entrada2 = valor_entrada2.replace("h(", "h,")
        valor_entrada2 = valor_entrada2.replace("i(", "i,")
        valor_entrada2 = valor_entrada2.replace("j(", "j,")
        valor_entrada2 = valor_entrada2.replace("k(", "k,")
        valor_entrada2 = valor_entrada2.replace("l(", "l,")
        valor_entrada2 = valor_entrada2.replace("m(", "m,")
        valor_entrada2 = valor_entrada2.replace("n(", "n,")
        valor_entrada2 = valor_entrada2.replace("o(", "o,")
        valor_entrada2 = valor_entrada2.replace("p(", "p,")
        valor_entrada2 = valor_entrada2.replace("q(", "q,")
        valor_entrada2 = valor_entrada2.replace("r(", "r,")
        valor_entrada2 = valor_entrada2.replace("s(", "s,")
        valor_entrada2 = valor_entrada2.replace("t(", "t,")
        valor_entrada2 = valor_entrada2.replace("u(", "u,")
        valor_entrada2 = valor_entrada2.replace("v(", "v,")
        valor_entrada2 = valor_entrada2.replace("w(", "w,")
        valor_entrada2 = valor_entrada2.replace("x(", "x,")
        valor_entrada2 = valor_entrada2.replace("y(", "y,")
        valor_entrada2 = valor_entrada2.replace("z(", "z,")
        valor_entrada2 = valor_entrada2.replace("(", "")
        valor_entrada2 = valor_entrada2.replace(")", ",")
        valor_entrada2 = valor_entrada2.replace("[", "")
        valor_entrada2 = valor_entrada2.replace("]", ",")
        valor_entrada2 = valor_entrada2.replace(", ", "")
        valor_entrada2 = valor_entrada2.replace(",,", ",")
        arreglo_headers.append(valor_entrada)
        arreglo_por_valor_2.append(valor_entrada2)
        print("for1-----------", valor_entrada2 )
        valor_total = i[1]
        for j in sacar_nombre_de_caracteres:
            print("for2", j )
            if j in i[1]:
                arreglo_por_valor.append(j)
        arreglo_limpio.append(arreglo_por_valor)
        arreglo_limpio2.append(arreglo_por_valor_2)
    print("ARREGLO LIMPIO", arreglo_limpio)
    print("ARREGLO LIMPIO2", arreglo_limpio2)
    print("ARREGLO HEADERS", arreglo_headers)
    concat_matrix = "\n".join([str("   " + a.replace("'","")) + "="+ '"' + str(b) + '"' for a,b in zip(arreglo_headers,arreglo_limpio2)])
    print("CONCATENACION", concat_matrix)
    concat_matrix = concat_matrix.replace('"', "")
    concat_matrix = concat_matrix.replace("'", "")
    print("CONCATENACION", concat_matrix)
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    new_text = concat_matrix
    archivo_seleccionado = archivo_seleccionado.replace("#!tokens", new_text)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()   
    
def validaciones():
    print("tokens para pasar a definicon", arreglo_tokens_limpios5)
    arreglo_headers = [] 
    for i in arreglo_tokens_limpios5:
        valor_entrada = i[0] 
        arreglo_headers.append(valor_entrada)
    print("Encabezados", arreglo_headers)
    todas_las_validaciones = [] 
    for j in arreglo_headers:
        #nuevo_texto_validar = "   " + "new_lineas = []" + "\n" + "   "+  "new_lineas.append(lineas)" +  "\n" + "   " + "lista_de_palabras = convert(new_lineas)" +  "\n" + "   " + "arreglo_con_todos_los_tokens = [] "
        nuevo_texto_validar = "\n" + "   " + "for i in " + j + ":" 
        nuevo_texto_validar = nuevo_texto_validar + "\n" + "      " + "lista_creada = list(i)" + "\n" + "      " + "arreglo_nuevo = []" + "\n" + "      " + "for j in lista_creada:"
        nuevo_texto_validar = nuevo_texto_validar + "\n" + "         " + "for k in lista_de_palabras:" + "\n" + "            " + "arreglo_test = []" + "\n" + "            "+ "lista_creada2 = list(k)"  + "\n" + "            "+"for n in lista_creada2:"
        nuevo_texto_validar = nuevo_texto_validar + "\n" + "               if n in lista_creada:" + "\n" + "                  arreglo_test.append(True)" + "\n" + "               if n not in lista_creada:" + "\n" + "                  arreglo_test.append(False)"
        nuevo_texto_validar = nuevo_texto_validar + "\n" + "            if all(arreglo_test) == True:" + "\n" + '               salvar_valor = "Token:"+ k +' + '" ' + j + '"'  + "\n" + "               arreglo_con_todos_los_tokens.append(salvar_valor)"
        print("------------------------")
        print(nuevo_texto_validar )
        print("------------------------")
        todas_las_validaciones.append(nuevo_texto_validar)
    
    declaracion_string = ("\n".join(todas_las_validaciones))
    inicializar_limpieza = '   lineas = lineas.replace(" ", " # ")' + "\n"
    inicializar_limpieza = inicializar_limpieza + "   new_lineas = []"+ "\n"
    inicializar_limpieza = inicializar_limpieza + "   new_lineas.append(lineas)"+ "\n"
    inicializar_limpieza = inicializar_limpieza + "   new_lista_de_palabras = convert(new_lineas)"+ "\n"
    inicializar_limpieza = inicializar_limpieza + "   lista_de_palabras = []"+ "\n"
    inicializar_limpieza = inicializar_limpieza + "   for i in new_lista_de_palabras:"+ "\n"
    inicializar_limpieza = inicializar_limpieza + '      if i == "#":'+ "\n"
    inicializar_limpieza = inicializar_limpieza + '         i = i.replace("#", " ")'+ "\n"
    inicializar_limpieza = inicializar_limpieza + '      lista_de_palabras.append(i)'+ "\n"
    inicializar_limpieza = inicializar_limpieza + '   arreglo_con_todos_los_tokens = [] '+ "\n"
    declaracion_string = inicializar_limpieza + declaracion_string
    #declaracion_string = "   " + "new_lineas = []" + "\n" + "   "+  "new_lineas.append(lineas)" +  "\n" + "   " + "lista_de_palabras = convert(new_lineas)" +  "\n" + "   " + "arreglo_con_todos_los_tokens = [] " + declaracion_string
    declaracion_string = declaracion_string + "\n" + "   unique(arreglo_con_todos_los_tokens)"
    print("-----------------------------------------")
    print("DECLARACION STRING", declaracion_string)
    print("-----------------------------------------")
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    archivo_seleccionado = archivo_seleccionado.replace("#validar!$", declaracion_string)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()   

def segunda_validacion():
    print("tokens para pasar a definicon", arreglo_tokens_limpios5)
    arreglo_headers = [] 
    for i in arreglo_tokens_limpios5:
        valor_entrada = i[0] 
        arreglo_headers.append(valor_entrada)
    print("Encabezados de Tokens", arreglo_headers)
    print("transposiciones", arreglo_todos_los_tokens_transposicion )
    print("final e inicial", arreglo_todos_los_tokens_final_inicial)
    concat_matrix = "\n".join([str("   transposicion_" + a.replace("'","")) + "="+ str(b) for a,b in zip(arreglo_headers,arreglo_todos_los_tokens_transposicion)])
    print("TRANS",concat_matrix)
    concat_matrix = concat_matrix.replace("'0'", "zero")
    concat_matrix = concat_matrix.replace("'1'", "one")
    concat_matrix = concat_matrix.replace("'2'", "two")
    concat_matrix = concat_matrix.replace("'3'", "three")
    concat_matrix = concat_matrix.replace("'4'", "four")
    concat_matrix = concat_matrix.replace("'5'", "five")
    concat_matrix = concat_matrix.replace("'6'", "six")
    concat_matrix = concat_matrix.replace("'7'", "seven")
    concat_matrix = concat_matrix.replace("'8'", "eight")
    concat_matrix = concat_matrix.replace("'9'", "nine")
    concat_matrix2 = "\n".join([str("   inicialfinal_" + a.replace("'","")) + "="+ str(b) for a,b in zip(arreglo_headers,arreglo_todos_los_tokens_final_inicial)])
    print(concat_matrix2)
    pasar_variable = concat_matrix + "\n" + concat_matrix2 + "\n" + "   arreglo_con_todos_los_tokens2 = []" + "\n"
    print("PASAR VARIABLE", concat_matrix)
    arreglo_verificar_afd = []
    for i in arreglo_headers:
        print("********************************")
        #arreglo_verificar_afd.append(variable_analizar2)
        nuevo_texto = "   for i in " + "inicialfinal_" + i + ":" + "\n"
        nuevo_texto= nuevo_texto + "      for j in transposicion_" + i + ":" + "\n"
        nuevo_texto= nuevo_texto + "         if(i[0] == j[0] and i[1] == j[2]):" + "\n"
        nuevo_texto= nuevo_texto + "            lista_creada = []" + "\n"
        nuevo_texto= nuevo_texto + "            for i in j[1] :" + "\n"
        nuevo_texto= nuevo_texto + "               lista_creada.append(i)"+ "\n"
        nuevo_texto= nuevo_texto + "            for j in lista_creada:"+ "\n"
        nuevo_texto= nuevo_texto + "               for k in lista_de_palabras:"+ "\n"
        nuevo_texto= nuevo_texto + "                  arreglo_test = []"+ "\n"
        nuevo_texto= nuevo_texto + "                  lista_creada2 = list(k)"+ "\n"
        nuevo_texto= nuevo_texto + "                  for n in lista_creada2:"+ "\n"
        nuevo_texto= nuevo_texto + "                     if n in lista_creada:"+ "\n"
        nuevo_texto= nuevo_texto + "                        arreglo_test.append(True)"+ "\n"
        nuevo_texto= nuevo_texto + "                     if n not in lista_creada:"+ "\n"
        nuevo_texto= nuevo_texto + "                        arreglo_test.append(False)"+ "\n"
        nuevo_texto= nuevo_texto + "                  if all(arreglo_test) == True:"+ "\n"
        nuevo_texto= nuevo_texto + "                     salvar_valor = 'Token_VS2:'+ k "+ "\n"
        nuevo_texto= nuevo_texto + "                     arreglo_con_todos_los_tokens2.append(salvar_valor)"+ "\n"
        print(nuevo_texto)
        arreglo_verificar_afd.append(nuevo_texto)
        print("********************************")
    print("PROBAR", arreglo_verificar_afd)
    verificar_afd = "\n".join(arreglo_verificar_afd)
    pasar_variable = pasar_variable + verificar_afd + "\n" + '   print("-------------------------VS2 ----------------------------------")'+ "\n"
    pasar_variable = pasar_variable + "   unique(arreglo_con_todos_los_tokens2)" + "\n" 
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    archivo_seleccionado = archivo_seleccionado.replace("#validar2!@", pasar_variable)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()  

def error_validator():
    print("sacar caracteres", sacar_nombre_de_caracteres)
    error_value = '+'.join(["str(" + str(elem)+ ")" for elem in sacar_nombre_de_caracteres])
    error_value = "   " + "error_validator =" + error_value + "\n" + "   lineas2 = lineas.replace(' ', '')" + "\n"+ "   lineas2 = lineas.replace('#', '')"
    error_value = error_value + "\n" + "   for i in lineas2:" + "\n" + "      if i not in error_validator:" + "\n"
    error_value = error_value + '         if i != " ":' + "\n"
    error_value = error_value + '            print("ERROR!: Se ingreso un caracter no valido" , i)'+ "\n"
    print("error value", error_value)
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    archivo_seleccionado = archivo_seleccionado.replace("#!error_validator", error_value)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()

def keywords_manager():
    print("condicionales", corte_de_palabras_clave)
    print("arreglo_tokens_limpios3", arreglo_test_key)
    condicionales_init = []
    for i in corte_de_palabras_clave:
        nueva_variable = "   " + "key_" + i[0] + "=" + i[1] + "\n"
        nueva_variable = nueva_variable + "   if key_"+ i[0]+ " in lineas:" +  "\n"
        nueva_variable = nueva_variable + '      print("KEYWORD:", key_' + i[0] + ")"+  "\n"
        nueva_variable = nueva_variable + "      lineas = lineas.replace(key_" + i[0] + ', "")' +  "\n"
        print("condicionales iniciales", nueva_variable)
        condicionales_init.append(nueva_variable)
    inicializar_keywords = "\n".join(condicionales_init)
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    archivo_seleccionado = archivo_seleccionado.replace("#!keywords", inicializar_keywords)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()
def por_caracter():
    print("PRIMER SACAR DECLARACIONES", sacar_nombre_de_caracteres)
    nueva_declaracion = []
    for i in sacar_nombre_de_caracteres:
        buscar_posicion = sacar_nombre_de_caracteres.index(i)
        buscar_posicion = str(buscar_posicion)
        buscar_posicion = buscar_posicion.replace('0',"zero_array")
        buscar_posicion = buscar_posicion.replace('1', "one_array")
        buscar_posicion = buscar_posicion.replace('2', "two_array")
        buscar_posicion = buscar_posicion.replace('3', "three_array")
        buscar_posicion = buscar_posicion.replace('4', "four_array")
        buscar_posicion = buscar_posicion.replace('5', "five_array")
        buscar_posicion = buscar_posicion.replace('6', "six_array")
        buscar_posicion = buscar_posicion.replace('7', "seven_array")
        buscar_posicion = buscar_posicion.replace('8', "eight_array")
        buscar_posicion = buscar_posicion.replace('9', "nine_array")
        buscar_posicion_2 = sacar_nombre_de_caracteres.index(i)
        buscar_posicion_2 = str(buscar_posicion_2)
        buscar_posicion_2 = buscar_posicion_2.replace('0',"zero")
        buscar_posicion_2 = buscar_posicion_2.replace('1', "one")
        buscar_posicion_2 = buscar_posicion_2.replace('2', "two")
        buscar_posicion_2 = buscar_posicion_2.replace('3', "three")
        buscar_posicion_2 = buscar_posicion_2.replace('4', "four")
        buscar_posicion_2 = buscar_posicion_2.replace('5', "five")
        buscar_posicion_2 = buscar_posicion_2.replace('6', "six")
        buscar_posicion_2 = buscar_posicion_2.replace('7', "seven")
        buscar_posicion_2 = buscar_posicion_2.replace('8', "eight")
        buscar_posicion_2 = buscar_posicion_2.replace('9', "nine")
        nuevo_string = "      " + buscar_posicion + "=" + "[]" + "\n"
        nuevo_string = nuevo_string + "      " + buscar_posicion + "+=" + buscar_posicion_2
        #print("PROBAR NUEVO SCAN", nuevo_string)
        nueva_declaracion.append(nuevo_string)
    values1 = '\n'.join(nueva_declaracion)
    print("PROBAR INICIALIZACION", values1)
    archivo_seleccionado = open("NewScanner.py", "r+")
    archivo_seleccionado = archivo_seleccionado.read()
    archivo_seleccionado = archivo_seleccionado.replace("#!scan02", values1)
    keypass_01 = open("NewScanner.py", "w")
    keypass_01.write(archivo_seleccionado)
    keypass_01.close()

    

declarar_variables_de_inicializacion()
declarar_siguiente_caracter()
input_de_archivo()
definiciones_de_tokens()
validaciones()
segunda_validacion()
error_validator()
keywords_manager()
por_caracter()
print()
print("+ analizador lexico generado")







