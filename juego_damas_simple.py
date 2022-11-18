import math


def generar_soluciones():
    numeros = [0, 1, 2, 3]
    soluciones = []
    for i in numeros:
        for j in numeros:
            for k in numeros:
                for l in numeros:
                    solucion = "{}{}{}{}".format(i, j, k, l)
                    if solucion not in soluciones:
                        soluciones.append(solucion)
    return soluciones


def generar_soluciones2():
    numeros = []
    for i in range(1111111, 7777778):
        if ("8" in str(i) or "9" in str(i) or "0" in str(i)):
            continue
        numeros.append(str(i))

    return numeros


def fichas_en_linea1(solucion):
    return (solucion[0] == solucion[1] or solucion[1] == solucion[2] or
            solucion[2] == solucion[3] or solucion[3] == solucion[0]
            or solucion[0] == solucion[2] or solucion[1] == solucion[3])


def fichas_en_diagonal1(solucion):
    '''
            0 1 2 3
         0  X X 0 X Blancas par   X 0 X X
         1  0 X X X Negras impar  X X X 0
         2  X X X 0               0 X X X
         3  X 0 X X               X X 0 X
    '''
    # 2. Comprobar que no hayan dos fichas en la misma diagonal descendente
    for i in range(0, 4):
        primera_ficha_casilla_color = int(solucion[i])-i
        for j in range(i+1, 4):
            segunda_ficha_casilla_color = int(solucion[j])-j
            if primera_ficha_casilla_color == segunda_ficha_casilla_color:
                return True

    # 3. Comprobar que no hayan dos fichas en la misma diagonal ascendente
    for i in range(0, 4):
        primera_ficha_casilla_color = int(solucion[i])+i
        for j in range(i+1, 4):
            segunda_ficha_casilla_color = int(solucion[j])+j
            if primera_ficha_casilla_color == segunda_ficha_casilla_color:
                return True
    return False


def fichas_en_linea2(solucion):
    numero_fichas = len(solucion)
    for i in range(0, numero_fichas):
        for j in range(i+1, numero_fichas):
            if solucion[i] == solucion[j]:
                return True
    return False


def fichas_en_diagonal2(solucion):
    '''
        0 1 2 3
    0   X X X X     La diagonal es la igualdad de la resta de fila de a y la fila de b
    1   0 X X X     y la columna de a y la columna de b 
    2   X X X X
    3   X X 0 X
    '''
    numero_fichas = len(solucion)
    for i in range(0, numero_fichas):
        for j in range(i+1, numero_fichas):
            if abs(int(solucion[i])-int(solucion[j])) == abs(i-j):
                return True
    return False


def comprobar_solucion(solucion):

    if (fichas_en_linea2(solucion)):
        return False

    if (fichas_en_diagonal2(solucion)):
        return False

    return True


def main():
    soluciones = generar_soluciones2()
    for solucion in soluciones:
        if comprobar_solucion(solucion):
            print(solucion)


if __name__ == '__main__':
    main()
pass
