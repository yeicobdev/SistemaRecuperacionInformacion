import json
import os
import sys
import pickle

class Documento:
    def __init__(self, documento):
        self.documento = documento
        self.apariciones=1
    def inc(self):
        self.apariciones=self.apariciones+1





class Elemento:
    def __init__(self,id_palabra):
        self.id_palabra = id_palabra
        self.frec_doc=[]

    def nueva_aparicion(self, doc):
        self.frec_doc.append(Documento(doc))

    def incrementa_doc(self):
        self.frec_doc[-1].inc()


    def string_form(self):
        return f"Elemento: {self.id_palabra}, Frecuencia por Documento: {dict(self.frec_doc)}"

class Diccionario:
    def __init__(self):
        self.term2id={}
        self.doc2id={}
        self.id2term=[]
        self.id2doc=[]
        self.indice_invertido={}
        self.cont_term=0
        self.cont_doc=0


    def __leer_json(self,nombre_archivo,indice_fichero):
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)  # Cargar el contenido del JSON
                if isinstance(datos, list):  # Verificar que sea una lista
                    for palabra in datos:

                        if palabra not in self.term2id:
                            self.term2id[palabra]=self.cont_term
                            self.id2term.append(palabra)
                            self.indice_invertido[self.cont_term]= Elemento(self.cont_term)
                            self.indice_invertido.get(self.cont_term).nueva_aparicion(indice_fichero)
                            self.cont_term += 1

                        else:
                            termino=self.indice_invertido.get(self.term2id.get(palabra))
                            if termino.frec_doc[-1].documento == indice_fichero:
                                termino.incrementa_doc()
                            else:
                                termino.nueva_aparicion(indice_fichero)





                else:
                    print("El JSON no contiene una lista de palabras.")
        except FileNotFoundError:
            print("El archivo no se encontró.")
        except json.JSONDecodeError:
            print("Error al decodificar el JSON. Verifique el formato del archivo.")



    def leer(self, data_path):


        os.listdir(data_path)

        for file in os.listdir(data_path):


            file_name=data_path+"\\"+file

            if file_name not in self.doc2id:
                self.id2doc.append(file_name)
                self.doc2id[file_name] = self.cont_doc
                self.__leer_json(file_name,self.cont_doc)
                self.cont_doc += 1
            else:
                print(f"No se ha procesado el documento {file_name} porque ya existe")




    def muestra_indice_invertido(self):
        for clave,valor in self.indice_invertido.items():
            print(clave)
            print(valor.string_form())





    def guarda_info(self, path):
        with open(path,"wb") as archivo:
            pickle.dump(self.term2id,archivo)
            pickle.dump(self.doc2id,archivo)
            pickle.dump(self.id2term,archivo)
            pickle.dump(self.id2doc,archivo)
            pickle.dump(self.indice_invertido,archivo)
            pickle.dump(self.cont_term,archivo)
            pickle.dump(self.cont_doc,archivo)




    def carga_info(self,path):
        with open(path,"rb") as archivo:
            self.term2id=pickle.load(archivo)
            self.doc2id=pickle.load(archivo)
            self.id2term=pickle.load(archivo)
            self.id2doc=pickle.load(archivo)
            self.indice_invertido=pickle.load(archivo)
            self.cont_term=pickle.load(archivo)
            self.cont_doc=pickle.load(archivo)

    @staticmethod
    def __calcular_memoria(estructura):
        """Calcula el tamaño en memoria de una estructura incluyendo su contenido."""
        size = sys.getsizeof(estructura)
        if isinstance(estructura, dict):
            size += sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in estructura.items())
        elif isinstance(estructura, list):
            size += sum(sys.getsizeof(item) for item in estructura)
        return size

    def mostrar_memoria(self):
        print(f"Memoria utilizada por term2id: {self.__calcular_memoria(self.term2id)} bytes")
        print(f"Memoria utilizada por doc2id: {self.__calcular_memoria(self.doc2id)} bytes")
        print(f"Memoria utilizada por id2term: {self.__calcular_memoria(self.id2term)} bytes")
        print(f"Memoria utilizada por id2doc: {self.__calcular_memoria(self.id2doc)} bytes")
        print(f"Memoria utilizada por indice_invertido: {self.__calcular_memoria(self.indice_invertido)} bytes")











