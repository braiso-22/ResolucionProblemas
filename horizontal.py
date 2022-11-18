# Vamos a buscar los la solucion de una lista de valores
from juego_damas_simple import comprobar_solucion


def generar_sucesores(padre, largo_solucion=4):
    sucesores = []
    if (len(padre) < largo_solucion):
        for i in range(0, largo_solucion):
            sucesores.append(padre + str(i))
    return sucesores


def busqueda_horizontal(tablero=4):
    estado_inicial = ""
    abiertos = []

    abiertos.append(estado_inicial)
    actual = abiertos[0]

    while not (len(actual) == tablero and comprobar_solucion(actual)) and len(abiertos) > 0:
        abiertos.pop()
        sucesores = generar_sucesores(actual,tablero)
        abiertos.extend(sucesores)
        if (len(abiertos) > 0):
            actual = abiertos[-1]
        
    if comprobar_solucion(actual):
        print(actual)
    else:
        print("No hay solucion")


def main():
    busqueda_horizontal(4)


if __name__ == "__main__":
    main()
