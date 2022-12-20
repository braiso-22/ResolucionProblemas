from clases.clases_profesor import GrafoR
import sys

class EightPuzzle(GrafoR):
    def __init__(self,solucion="1-2-3-4-5-6-7-8-0"):
        GrafoR.__init__(self, )
        self.borde_superior = [0, 1, 2]
        self.borde_inferior = [6, 7, 8]
        self.borde_izquierdo = [0, 3, 6]
        self.borde_derecho = [2, 5, 8]
        self.solucion = solucion

    def es_final(self, nodo):
        """
        Comprueba si el nodo es el final\n
        El nodo final es 1-2-3-4-5-6-7-8-0\n
        - el nodo es una cadena de 9 caracteres separados por guión\n
        - el primer caracter es el estado del 1 y así sucesivamente\n
        - 0 es vacío\n
        """
        return nodo == self.solucion

    def generar_sucesores(self, nodo):
        """
        Genera los sucesores de un nodo\n
        - el nodo es una cadena de 9 caracteres separados por guión\n
        - el primer caracter es el estado del 1 y así sucesivamente\n
        - 0 es vacío\n
        """
        hijos = []
        distancias_origen = []
        copia = nodo[:]
        arriba = self.__mover_abajo(copia)
        copia = nodo[:]
        abajo = self.__mover_arriba(copia)
        copia = nodo[:]
        izquierda = self.__mover_izquierda(copia)
        copia = nodo[:]
        derecha = self.__mover_derecha(copia)
        if arriba:
            hijos.append(arriba)
            distancias_origen.append(1 + self.distancias_origen.get(nodo, 0))
        if abajo:
            hijos.append(abajo)
            distancias_origen.append(1 + self.distancias_origen.get(nodo, 0))
        if izquierda:
            hijos.append(izquierda)
            distancias_origen.append(1 + self.distancias_origen.get(nodo, 0))
        if derecha:
            hijos.append(derecha)
            distancias_origen.append(1 + self.distancias_origen.get(nodo, 0))
        
        return hijos, distancias_origen

    def __mover_derecha(self, nodo):
        nodo = nodo.split("-")
        pos = nodo.index("0")
        if pos not in self.borde_derecho:
            nodo[pos], nodo[pos+1] = nodo[pos+1], nodo[pos]
            return "-".join(nodo)
        return None
    def __mover_izquierda(self, nodo):
        nodo = nodo.split("-")
        pos = nodo.index("0")
        if pos not in self.borde_izquierdo:
            nodo[pos], nodo[pos-1] = nodo[pos-1], nodo[pos]
            return "-".join(nodo)
        return None
    def __mover_arriba(self, nodo):
        nodo = nodo.split("-")
        pos = nodo.index("0")
        if pos not in self.borde_superior:
            nodo[pos], nodo[pos-3] = nodo[pos-3], nodo[pos]
            return "-".join(nodo)
        return None
    def __mover_abajo(self, nodo):
        nodo = nodo.split("-")
        pos = nodo.index("0")
        if pos not in self.borde_inferior:
            nodo[pos], nodo[pos+3] = nodo[pos+3], nodo[pos]
            return "-".join(nodo)
        return None

    def evalua_individuo(self, estado):
        estado = estado.split("-")
        numero_piezas = len(estado)
        mal_colocadas = 0
        casilla = 0
        while casilla < (numero_piezas-1):
            pieza_esperada = str(casilla+1)
            pieza_real = estado[casilla]
            pieza_mal_colocada = pieza_esperada != pieza_real
            
            casilla += 1
            if pieza_mal_colocada:
                mal_colocadas += 1
            
        return mal_colocadas

def menu():
    return input("Introduce el estado inicial del puzzle Ejemplo: 3-4-5-2-7-6-1-8-0: \n")

def main (param = None):
    solucion = "1-2-3-4-5-6-7-8-0"
    puzzle = EightPuzzle(solucion)
    if param:
        inicial = param
    else:
        inicial = menu()
    
    puzzle.recorre_grafo(inicial, modo="A*",evita_repetidos = True)
    ruta = puzzle.genera_ruta(solucion, inicial)
    print_ruta(ruta)

def print_ruta(ruta):
    for paso in ruta:
        paso = paso.split("-")
        print("-------")
        for i in range(3):
            string = "|"
            for j in paso[i*3:i*3+3]:
                string += j + "|"
            print(string)
        print("-------")
        print()

if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) == 0:
        main()
    else:
        main(params[0])