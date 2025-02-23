from bs4 import BeautifulSoup
import re




def extract(path,lan1):
    try:
        with open(path, 'r', encoding='utf-8') as archivoExtraer:
            contenido = archivoExtraer.read()  # Lee el contenido del archivo

        soup= BeautifulSoup(contenido, 'xml')   # Se guarda en la variable la información del xml
        resultado=""
        titulo = soup.find('dc:title',{'xml:lang':lan1})  #sacamos los campos a tokenizar
        descripcion = soup.find('dc:description', {'xml:lang': lan1})
        autores=soup.findAll('dc:creator')
        fecha=soup.find('dc:date')
        if titulo: #control de errores: hay veces que dependiendo del idioma falta el titulo
            resultado=titulo.string
        for autor in autores:
            resultado=resultado+" "+autor.string
        if fecha:
            resultado=resultado+" "+fecha.string+" "
        if descripcion:
            resultado+=descripcion.string
        return resultado #se devuelve un string con el contenido
    except FileNotFoundError:
        print(f"Error: El archivo '{path}' no existe.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None





def transform(content1,lan2):  #se utilizan expresiones regulares para eliminar los caracteres no deseados, en inglés no tiene sentido contemplar los acentos por eso la expresion regular es diferente
    content1 = content1.lower() #quitamos las mayusculas
    if lan2 == "es":
        return re.sub(r"[^a-záéíóú0-9 _\n-]", '', content1).split() #se devuelve en formato lista
    else:
        return re.sub(r"[^a-zA-Z0-9 _\n-]", '', content1).split()





def load(content2,nuevo_archivo): #para guardar la información en el formato esperado del token se va añadiendo palabra a palabra
    cambio_formato = "[" + ", ".join(f'"{palabra}"' for palabra in content2) + "]"
    with open(nuevo_archivo, 'w', encoding='utf-8') as f:
        f.write(cambio_formato)
    return




