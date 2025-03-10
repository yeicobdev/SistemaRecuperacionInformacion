import heapq

from math import sqrt
from collections import defaultdict

from bs4 import BeautifulSoup

from Practica11 import transform
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer





def show_file(path, lan):
    try:
        with open(path, 'r', encoding='utf-8') as archivoExtraer:
            contenido = archivoExtraer.read()  # Lee el contenido del archivo

        soup= BeautifulSoup(contenido, 'xml')   # Se guarda en la variable la información del xml
        titulo = soup.find('dc:title',{'xml:lang':lan})  #sacamos los campos a tokenizar
        descripcion = soup.find('dc:description', {'xml:lang': lan})
        autores=soup.findAll('dc:creator')
        fecha=soup.find('dc:date')
        print("Titulo: ")
        if titulo:
            print(titulo)

        print("Autores: ")
        for autor in autores:
            print(autor)
        print("Fecha: ")
        if fecha:
            print(fecha)

        print("Descripcion: ")
        if descripcion:
            print(descripcion)


    except FileNotFoundError:
        print(f"Error: El archivo '{path}' no existe.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None








class Word:
    def __init__(self,idx, word,weight):
        self.word = word
        self.weight=weight
        self.idx = idx

class Query:
    def __init__(self):
        self.words=[]


class Task:
    def __init__(self):
        self.querys=[]
        self.answer=[]
    def add_query(self,query):
        self.querys.append(query)





class Buscador:
    def __init__(self,lan,dicc,num_doc):
        self.query_list = []
        self.diccionario=dicc
        self.lan=lan
        self.tasks=[]
        self.num_doc=num_doc
        if lan == 'es':
            self.stop_words = set(stopwords.words('spanish'))
            self.stemmer = SnowballStemmer('spanish')
        else:
            self.stop_words = set(stopwords.words('english'))
            self.stemmer = SnowballStemmer('english')




    def add_querys(self, path):
        try:
            with open(path, "r", encoding="utf-8") as archivo:
                self.query_list = [line.strip() for line in archivo if line.strip()]
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta '{path}'.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")


    def nss_query(self):
        normalized_list=[]
        for query in self.query_list:
            normalized_list.append(transform(query,self.lan))

        final_list= []
        for lista in normalized_list:
            lista_add = []
            for word in lista:
                if word not in self.stop_words:
                    word=self.stemmer.stem(word)
                    lista_add.append(word)

            final_list.append(lista_add)

        self.query_list = final_list

    def create_task(self):
        self.tasks.append(Task())
        norms=[]
        for query in self.query_list:
            norm=0
            self.tasks[-1].add_query(Query())
            for word in query:
                iden=self.diccionario.term2id.get(word,"key_error")

                if iden!= "key_error":
                    value = self.diccionario.idf_list[iden]
                    palabra = Word(iden,word,value if iden != -1 else -1)
                    norm+=pow(value,2)
                    self.tasks[-1].querys[-1].words.append(palabra)

            norms.append(sqrt(norm))

        i=0
        for query in self.tasks[-1].querys:
            for word in query.words:
                word.weight=word.weight/norms[i]

            i+=1


    def search_documents(self):

        for task in self.tasks:
            for query in task.querys:
                documents=defaultdict(float)
                for word in query.words:
                    for doc in self.diccionario.indice_invertido[word.idx].frec_doc.values():
                        documents[doc.documento]+=word.weight*doc.nw


                lista_prov=list(documents.items())
                more_relevant=heapq.nlargest(self.num_doc,lista_prov,key=lambda x:x[1])
                task.answer.append(more_relevant)



