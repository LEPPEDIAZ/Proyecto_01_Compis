import numpy as np
import re
import sys
from collections import OrderedDict
sys.setrecursionlimit(10000)
#Parser 
#producciones
#acciones semanticas
#atributos
#any
#ll1
mylines = []                          
with open ('archivos/AritmeticaMod.ATG', 'r') as myfile: 
    for myline in myfile:
        myline = myline.strip('\n')
        myline = myline.strip('\t\t')   
        mylines.append(myline)           
#print(mylines)  
get_index = (mylines.index('PRODUCTIONS'))
new_lista = mylines[:get_index + 1]
C = np.array(list(filter(lambda x: x not in new_lista, mylines)))
#print(C)  
print("----------------")
mylines = C[:-1]
print(mylines)
print("----------------")
guardar_todo_arreglo = mylines


def GetParametros(array):
    guardar_parametros = [] 
    for i in array:
        print("i", i)
        i = i.replace("]", "")
        i = i.replace("[", "")
        val = re.findall('\(([^)]+)', i)
        if "<" or ">" or "System.Console" not in val:
            print("val", val)
            guardar_parametros.append(val)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$", guardar_parametros)

unique_words = [] 
key_words_get = []
def Expression(array):
    arreglo_funciones = [] 
    get_special_value1 = []
    get_special_value2 = []
    for i in array:
        #clean variables
        i = i.replace("=", " = ")
        i = i.replace("}", "")
        i = i.replace("{", "")
        i = i.replace(";", "")
        i = i.replace('"."', "")
        i = i.replace('"', "")
        i = i.replace('[]', "")
        i = i.replace('..', ".")
        i = i.replace("<", " <")
        i = i.replace(">", "> ")
        i = i.replace("(.", " <")
        i = i.replace(".)", "> ")
        i = i.replace("]", "> ")
        i = i.replace("[", " <")
        i = re.sub('<[^>]+>', '', i)
        i = i.replace("[", "")
        i = i.replace("]", "")
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace("<", "")
        i = i.replace(">", "")
        i = i.replace("/", "")
        #temporales
        i = i.replace("-", "")
        i = i.replace("+", "")
        i = i.replace("*", "")
        i = i.replace("-", "")
        i = i.replace("=", "->")
        #print("######", i)
        ssplit = i.split()
        single_space = "."
        for j in ssplit:
            arreglo_funciones.append(j)
        #    if single_space in j:
        #        nuevo_arreglo = []
        #    nuevo_arreglo.append(j)
        #arreglo_funciones.append(j)
    print(arreglo_funciones)
    smallerlist = [l.split(',') for l in ','.join(arreglo_funciones).split('.')]
    print("*************")
    print(smallerlist)
    print("*************")
    clean_array = [] 
    for k in smallerlist:
        new_list = list(filter(None, k))
        clean_array.append(new_list)
    print("~~~~~~~~~~~~")
    print(clean_array)
    print("----------------------")
    for i in clean_array:
        for j in i:
            if j not in unique_words and j!= "->" and j!= "|":
                unique_words.append(j)
    print("U",unique_words)
    new_array_convert_vs2 = [] 
    for j in clean_array:
        print("arreglo sin pasar: ", j )
        new_array_convert = [] 
        i = 0
        for k in j:
            if k != "->" or k !='|':
                if k in unique_words:
                    get_index = (unique_words.index(k))
                    key_words_get.append(get_index)
                    new_array_convert.append(get_index)     
            if k == "->" or k =='|':
                new_array_convert.append(k)
        print("#####", new_array_convert)
        new_array_convert_vs2.append(new_array_convert)
    print(" - - -- - -- - - - -- - - -- - - ")
    print(new_array_convert_vs2)
    pass_to_text = []
    for i in new_array_convert_vs2:
        listToStr = ''.join([str(elem) for elem in i]) 
        print(listToStr)
        pass_to_text.append(listToStr)
    print("@", pass_to_text)
    with open('grammar.txt', 'w') as f:
        for item in pass_to_text:
            f.write("%s\n" % item)

print("--------------my lines---------------------------")
print(guardar_todo_arreglo)
print("--------------my lines---------------------------")
Expression(mylines)
GetParametros(mylines)


reglas = [] 
firsts = [] 
reglas_dict = OrderedDict()  
firsts_dict = OrderedDict() 
follow_dict = OrderedDict()  

#agrega los no terminales en la izquierda de los first_dict
def pone_los_no_terminales_en_izquierda(firsts, reglas):
    for regla in reglas:
        if regla[0][0] not in firsts:
            firsts.append(regla[0][0])
            firsts_dict[regla[0][0]] = []
            follow_dict[regla[0][0]] = []

with open("grammar.txt", 'r') as inp, open('grammar_clean.txt', 'w') as out:
    for linea in inp:
        if linea.strip():
            out.write(linea)

with open("grammar_clean.txt", "r") as filetxt:
    for linea in filetxt:
        reglas.append(linea.strip().split('\n'))


numero_de_reglas= len(reglas)
contador_de_reglas = first_count = 0
pone_los_no_terminales_en_izquierda(firsts, reglas)
for first in firsts:
    reglas_dict[first] = reglas[contador_de_reglas][0][3:]
    contador_de_reglas += 1

for regla in reglas:
    if regla[0][3].islower():
        firsts_dict[regla[0][0]].extend(regla[0][3])
# implementa un pass 
for regla in reglas:
    if regla[0][3].isupper():
        firsts_dict[regla[0][0]].extend(firsts_dict[regla[0][3]])

with open("firsts.txt", "w+") as wp:
    for k in firsts_dict:
        wp.write("first(%s): \t " % k)
        wp.write("%s\n" % firsts_dict[k])

#se inicia a ver follows

llave_de_reglas = list(reglas_dict.keys())
key_count = len(llave_de_reglas)

for j in reglas_dict:
    tmp_regla_str = reglas_dict[j]
    if j == llave_de_reglas[0]:
        follow_dict[j].append('$')
    for i in range(key_count):
        if llave_de_reglas[i] in tmp_regla_str:
            tmp_regla_list = list(tmp_regla_str)
            current_non_term_index = tmp_regla_list.index(llave_de_reglas[i])

            if current_non_term_index == (len(tmp_regla_list) - 1):
                follow_dict[llave_de_reglas[i]].extend(follow_dict[llave_de_reglas[0]])
            else:
                follow_dict[llave_de_reglas[i]].extend(
                    firsts_dict[llave_de_reglas[(i + 1) % key_count]])

with open("follows.txt", "w+") as wp:
    for k in follow_dict:
        wp.write("follow(%s): \t" % k)
        wp.write("%s\n" % follow_dict[k])
print("Firsts:" + " " + str(follow_dict))
print("Follow:" + " " + str(firsts_dict))
print("Reglas:" + " " + str(reglas_dict))
print("------------------------------------")
print("unique words",unique_words)
index_elements_unique = set(key_words_get)
print("unicos en keywords", index_elements_unique)
print("------------------------------------")
def WriteNewFunctions(array_index, array_with_values, functions_for_variables):
    print("escribir nuevas funciones")

def CreateNewFunctions(all_array, array_with_values):
    for i in all_array:
        write_body_function = " "
        write_function_name = " "
        print("@", i )
        j = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", i)
        k = j
        j = re.sub('<[^>]+>', '', j)
        if "=" in j:
            def_name = j.split('=')[0]
            parameters = re.findall('<[^>]+>', k)
            next_values = i.split('=')[1:]
            next_values = "=".join(next_values)
            print("next values 2 ", next_values)
            # = i.split('=')[2]
            if "=" not in next_values:
                next_values = next_values.replace(".int", "")
                next_values = next_values.replace(";.", "=0")
                next_values = next_values.replace(",", "=0 \n")
                next_values = next_values.replace("(", "")
                next_values = next_values.replace(")", "")
                next_values = next_values.replace(" ", "")
            if "=" in next_values:
                next_values = next_values.replace(".int", "")
                next_values = next_values.replace("int.Parse(lastToken.Value).", "=0")
                next_values = next_values.replace(",", "=0 \n")
                next_values = next_values.replace(";.", "")
                next_values = next_values.replace("= =", "=")
                #next_values = next_values.replace("(", "")
                #next_values = next_values.replace(")", "")
                next_values = next_values.replace(".", "")
                next_values = next_values.replace(" ", "")

            #next_values = re.findall('\(([^)]+)', next_values)
            print("next values", next_values)
            if len(parameters)==0:
                write_function_name = "def " + str(def_name) + "():" + "\n" + "    "+ next_values
            if len(parameters)!=0:
                for p in parameters:
                    print("parametros", p)
                    p = p.replace("<", "")
                    p = p.replace(">", "")
                    p = p.replace("double", "")
                    p = p.replace("int", "")
                    p = p.replace("ref", "")
                    p = p.replace(" ", "")
                    write_function_name = "def " + str(def_name) + "(" + str(p) + "):" + "\n" + "    "+ next_values
            print("*************************")
            print("FUNCION", write_function_name)
            print("*************************")
        else:
            print("test")



CreateNewFunctions(guardar_todo_arreglo, unique_words)
