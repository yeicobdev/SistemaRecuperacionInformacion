import json
import time
from Practica14 import Diccionario
from Practica16 import Buscador, show_file

if __name__ == '__main__':
    start_time = time.time()
    with open('config4.json', 'r', encoding='utf-8') as archivo:
        datosConfig = json.load(archivo)

    pkl_path = datosConfig['pkl_path']
    diccionario = Diccionario()
    diccionario.carga_info(pkl_path)

    query_path=datosConfig['query_path']
    num_doc=datosConfig['num_doc']
    lan=datosConfig['lan']

    buscador=Buscador(lan,diccionario,num_doc)
    buscador.add_querys(query_path)
    buscador.nss_query()
    buscador.create_task()
    buscador.search_documents()




    end_time = time.time()
    elapsed_time = end_time - start_time
    print(diccionario.indice_invertido[diccionario.term2id['bienest']].idf)
    print(f"Tiempo: {elapsed_time} segundos ")
    diccionario.mostrar_memoria()
    print("CPU: Intel(R) Core(TM) i5-1035G1 CPU @ 1.00GHz   1.19 GHz")
    print("RAM: 8,00 GB (7,81 GB usable)")
    cont=1
    for task in buscador.tasks:
        for ans in task.answer:
            print(f"Query {cont}")
            for fich in ans:
                show_file("C://Users//jacob//OneDrive//Escritorio//SRI//scielo_collection//scielo_collection//"+diccionario.id2doc[fich[0]],"es")
                print("\n")
            print("\n")
            print("\n")
            cont+=1
