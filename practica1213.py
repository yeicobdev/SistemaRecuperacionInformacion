from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer






class StopperNStemmer:
    def __init__(self, lan):
        self.stop_words=set(stopwords.words(lan))
        self.stemmer=SnowballStemmer(lan)

    def stopper(self, content,palabras_repetidas_ini, palabras_repetidas_stopper):
        lista_return=[]
        for palabra in content:

            palabras_repetidas_ini.update(palabra.split())
            if palabra not in self.stop_words:
                lista_return.append(palabra)
                palabras_repetidas_stopper.update(palabra.split())
        return lista_return


    def stemmerfunc(self, content, palabras_repetidas_stemmer):
        lista_return=[]
        for palabra in content:
            word=self.stemmer.stem(palabra)
            lista_return.append(word)
            palabras_repetidas_stemmer.update(lista_return[-1].split())
        return lista_return



    def print_stop_words(self):
        print("StopWords:")
        for elemento in self.stop_words: print(elemento,end=" ")
        print("\n")





