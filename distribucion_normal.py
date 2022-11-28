import numpy


def estandarizar(lista):
    media = numpy.mean(lista)
    desviacion = numpy.std(lista)
    return [(x - media) / desviacion for x in lista]

def normalizar(lista):
    minimo = min(lista)
    maximo = max(lista)
    return [(x - minimo) / (maximo - minimo) for x in lista]

def main():
    lista = [1, 0.2, -3, 4, 15, 6, -7, 0.08, 9, -10]

    media = numpy.mean(lista)

    desviacion = numpy.std(lista)
    print(lista)
    print(f"Media: {media}, Desviación: {desviacion}\n")

    lista_normalizada = normalizar(lista)
    print(lista_normalizada)
    print(f"Media: {numpy.mean(lista_normalizada)}, Desviación: {numpy.std(lista_normalizada)}\n")


    


if __name__ == "__main__":
    main()