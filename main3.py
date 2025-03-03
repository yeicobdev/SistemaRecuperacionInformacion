import json
import time
from Practica14 import Diccionario

if __name__ == '__main__':
    start_time = time.time()  # control del tiempo
    with open('config2.json', 'r', encoding='utf-8') as archivo:
        datosConfig = json.load(archivo)
    pkl_path = datosConfig['pkl_path']
    diccionario = Diccionario()
    diccionario.carga_info(pkl_path)
    diccionario.calcula_pesos_y_frecuencias()
    diccionario.guarda_info(pkl_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo: {elapsed_time} segundos ")
    diccionario.mostrar_memoria()
    print("CPU: Intel(R) Core(TM) i5-1035G1 CPU @ 1.00GHz   1.19 GHz")
    print("RAM: 8,00 GB (7,81 GB usable)")