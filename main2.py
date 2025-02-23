import json
import time

from Practica14 import Diccionario

if __name__ == '__main__':
    start_time = time.time()  # control del tiempo
    with open('config2.json', 'r', encoding='utf-8') as archivo:
        datosConfig = json.load(archivo)

    token_dir=datosConfig['tokenDir']
    coleccion_vacia=datosConfig['coleccion_vacia']
    pkl_path=datosConfig['pkl_path']
    diccionario=Diccionario()
    if coleccion_vacia=='TRUE':
        diccionario.leer(token_dir)
        diccionario.guarda_info(pkl_path)
    else:
        diccionario.carga_info(pkl_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo: {elapsed_time} segundos ")
    diccionario.mostrar_memoria()

