from clases.clases_profesor import GrafoR

class EightPuzzle(GrafoR):
    def __init__(self):
        GrafoR.__init__(self)
        self.numero_elementos = 7

    def es_final(self, nodo):
        """
        """
        return False

    def generar_sucesores(self, nodo):
        """
        """
        hijos = []
        distancias_origen = []
        
        return hijos, distancias_origen

    def __is_valid_son(self, hijo, padre): 
        return True

    def __count_changes(self, str1, str2):
        count = 0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                count += 1
        return count
    def __change_not_in_same_side(self, str1, str2, side):
        for i in range(len(str1)):
            if str1[i] != str2[i] and str1[i] != side:
                return True
        return False

    def evalua_individuo(self, tentativa):
        lg = len(tentativa)
        mal_colocadas = self.ndamas - lg
        columna = 0
        while columna < (lg-1):
            fila = int(tentativa[columna])
            # print(f"estoy investigando columna {columna} fila {fila}")
            columna2 = columna + 1
            while columna2 <= (lg-1):
                fila2 = int(tentativa[columna2])
                if fila == fila2:
                    mal_colocadas += 10
                if abs(columna - columna2) == abs(fila - fila2):
                    mal_colocadas += 10
                # print(f"comparo contra columna {columna2} fila {fila2}")
                columna2 = columna2 + 1
            columna = columna + 1
        return mal_colocadas

def main ():
    puzzle = EightPuzzle()
    puzzle.recorre_grafo("",modo="dijkstra",evita_repetidos = False)
    ruta = puzzle.genera_ruta("", "")
    print(ruta)

if __name__ == "__main__":
    main()