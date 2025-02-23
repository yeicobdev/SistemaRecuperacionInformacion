from Practica11 import *
import time
import os
import json
from practica1213 import  StopperNStemmer
from collections import Counter

if __name__ == '__main__':
    start_time = time.time() #control del tiempo
    num_tokens_inicio=0
    max_tokens_inicio=-999999
    min_tokens_inicio=999999

    num_tokens_stopper=0
    max_tokens_stopper = -999999
    min_tokens_stopper = 999999

    num_tokens_stemmer=0
    max_tokens_stemmer = -999999
    min_tokens_stemmer = 999999

    palabras_repetidas_inicio= Counter()
    palabras_repetidas_stopper= Counter()
    palabras_repetidas_stemmer= Counter()



    num_archivos=0 #numero de archivos procesados
    # Abrir y leer el archivo JSON
    with open('config.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)




    directorio=datos['path'] #directorio con el conjunto de datos
    directorio_resultado=datos['resultPath'] #directorio donde se guardarán los resultados
    lan=datos['lan'] #idioma de los datos español 'es' inglés 'en'
    if lan=='es':
        stopperstemmer= StopperNStemmer('spanish')
    else:
        stopperstemmer = StopperNStemmer('english')


    os.mkdir(directorio_resultado+"//resultado") # se crea un directorio con el resultado
    for nombre_archivo in os.listdir(directorio): #se listan todos los archivos del directorio del conjunto de datos
        ruta_completa = os.path.join(directorio, nombre_archivo)
        if ruta_completa.endswith(".xml"): #solo procesamos archivos .xml
            content = extract(ruta_completa,lan) #se extrae la información
            content = transform(content,lan) #se transforma al formato adecuado

            num_tokens_inicio+=len(content)
            if len(content) > max_tokens_inicio:
                max_tokens_inicio=len(content)
            if len(content) < min_tokens_inicio:
                min_tokens_inicio=len(content)


            content=stopperstemmer.stopper(content,palabras_repetidas_inicio,palabras_repetidas_stopper) #se quitan las palabras sin significado
            num_tokens_stopper+=len(content)
            if len(content) > max_tokens_stopper:
                max_tokens_stopper=len(content)
            if len(content) < min_tokens_inicio:
                min_tokens_stopper=len(content)

            content=stopperstemmer.stemmerfunc(content,palabras_repetidas_stemmer) # se sacan las raices
            num_tokens_stemmer+=len(content)
            unique=set(content)
            if len(unique) > max_tokens_stemmer:
                max_tokens_stemmer=len(unique)
            if len(unique) < min_tokens_stemmer:
                min_tokens_stemmer=len(unique)


            load(content,directorio_resultado+"//resultado//"+nombre_archivo[:-4]+"-tokens.json") #creamos un fichero con los tokens
            num_archivos+=1 #contar archivos


        else:
            print("El archivo NO es XML.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"El bloque de código tardó {elapsed_time:.6f} segundos en ejecutarse")
    print(f"Se han procesado: { num_archivos} archivos ")
    print(f"Se han obtenido: {num_tokens_inicio} tokens al inicio")
    print(f"Media de tokens al inicio: {num_tokens_inicio/num_archivos}")
    print(f"Maximo de tokens al inicio: {max_tokens_inicio} tokens")
    print(f"Minimo de tokens al inicio: {min_tokens_inicio} tokens")
    top_10_ini=palabras_repetidas_inicio.most_common(10)
    print(f"10 palabras mas repetidas en el inicio: {top_10_ini} ")
    print("\n")

    print(f"Se han obtenido: {num_tokens_stopper} tokens despues del stopper")
    print(f"Media de tokens despues del stopper: {num_tokens_stopper/num_archivos} tokens")
    print(f"Maximo de tokens despues del stopper: {max_tokens_stopper} tokens")
    print(f"Minimo de tokens despues del stopper: {min_tokens_stopper} tokens")
    top_10_stop = palabras_repetidas_stopper.most_common(10)
    print(f"10 palabras mas repetidas despues del stopper: {top_10_stop} ")
    print("\n")
    stopperstemmer.print_stop_words()

    print(f"Se han obtenido: {len(palabras_repetidas_stemmer)} tokens unicos despues del stemmer")
    print(f"Media de tokens unicos despues del stemmer en toda la coleccion: {len(palabras_repetidas_stemmer) / num_archivos} tokens")
    print(f"Maximo de tokens unicos despues del stemmer en un fichero: {max_tokens_stemmer} tokens")
    print(f"Minimo de tokens unicos despues  del stemmer en un fichero: {min_tokens_stemmer} tokens")
    top_10_stemmer = palabras_repetidas_stemmer.most_common(10)
    print(f"10 palabras mas repetidas despues del stemmer: {top_10_stemmer} ")
    print(f"Se ha utilizado el Stemmer Snowball de nltk")