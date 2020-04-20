from OriginalScanner import *

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

with open("Textos_Generados/analizador_lexico.txt", "a+") as txt_file:
    txt_file.write("CORTE DE CARACTERES\n")
    txt_file.write("__________________________________\n")
    for line in corte_caracteres:
        txt_file.write("".join(line) + "\n")
    txt_file.write("----------------------------------\n")
    txt_file.write("CONDICIONALES\n")
    txt_file.write("__________________________________\n")
    for line in corte_de_palabras_clave:
        txt_file.write("".join(line) + "\n")
    txt_file.write("----------------------------------\n")
    txt_file.write("TIPOS\n")
    txt_file.write("__________________________________\n")
    for line in corte_de_tokens:
        txt_file.write("".join(line) + "\n") 
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
            if elemento == '"':
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
            again = sbstring[sbstring.index('{')+1:sbstring.index('}')]
            sbstring = again + ' ' + again + '* '  + sbstring[sbstring.index('}')+1:]
    marcar_nodo.contenido = sbstring
    tokenizar.tokens.append(marcar_nodo)


for primer_token in tokenizar.tokens:
    for segundo_token in tokenizar.caracteres:
        primer_contenido = primer_token.contenido.split()
        for por_cada_palabra in primer_contenido:
            if segundo_token.nombre == por_cada_palabra:
                if len(segundo_token.contenido) == 1:
                    primer_token.contenido = primer_token.contenido.replace(segundo_token.nombre, segundo_token.contenido[0])
                else:
                    crear = ' '.join([str(elem) for elem in segundo_token.contenido])
                    crear = crear.replace(' ', '')
                    primer_token.contenido = primer_token.contenido.replace(segundo_token.nombre, crear)
                    primer_token.contenido = primer_token.contenido.replace('"', '')
tokenizar.marcar_nodos(tokenizar.tokens)

for indice, sblista in enumerate(tokenizar.tokens_excepto):
    for indice2, nod in enumerate(tokenizar.tokens):
        if nod.nombre == sblista[0]:
            nod.excepciones = sblista[1:]

print("+ analizador lexico generado")





