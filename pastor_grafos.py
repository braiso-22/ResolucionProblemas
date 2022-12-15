from clases.clases_profesor import GrafoR

class Pastor(GrafoR):
    def __init__(self):
        GrafoR.__init__(self)
        self.numero_elementos = 4

    def es_final(self, nodo):
        """
        Comprueba si el nodo es el final\n
        El nodo final es 1111\n
        - el nodo es una cadena de 4 caracteres\n
        - el primer caracter es el estado del pastor\n
        - el segundo caracter es el estado del lobo\n
        - el tercer caracter es el estado de la oveja\n
        - el cuarto caracter es el estado de la col\n
        - 0 es izquierda\n
        - 1 es derecha
        """
        return nodo == "1111"

    def generar_sucesores(self, nodo):
        """
        Genera los sucesores de un nodo\n
        - el nodo es una cadena de 4 caracteres\n
        - el primer caracter es el estado del pastor\n
        - el segundo caracter es el estado del lobo\n
        - el tercer caracter es el estado de la oveja\n
        - el cuarto caracter es el estado de la col\n

        - 0 es izquierda\n
        - 1 es derecha
        """
        hijos = []
        distancias_origen = []
        for i in range(0, 2**self.numero_elementos):
            nodo_nuevo = format(i, f'0{self.numero_elementos}b')
            hijos.append(nodo_nuevo)

            distancias_origen.append(
                1 + self.distancias_origen.get(nodo, 0))

        hijos = self.__delete_not_valids(hijos, nodo)

        return hijos, distancias_origen

    def __delete_not_valids(self, hijos, padre):
        hijos_finales = hijos[:]
        for hijo in hijos:
            if not self.__is_valid_son(hijo, padre):
                hijos_finales.remove(hijo)
        return hijos_finales

    def __is_valid_son(self, hijo, padre):
        pastor = hijo[0]
        pastor_padre = padre[0]
        lobo = hijo[1]
        oveja = hijo[2]
        col = hijo[3]

        # No cambia el pastor
        if pastor == pastor_padre:
            return False
        # Se mueven más de dos en la barca
        if self.__count_changes(hijo, padre) > 2:
            return False
        # Se come a la oveja
        if lobo == oveja and pastor != lobo:
            return False
        # Se come a la col
        if oveja == col and pastor != oveja:
            return False

        return True

    def __count_changes(self, str1, str2):
        count = 0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                count += 1
        return count

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
    pastor = Pastor()
    pastor.recorre_grafo("0000",modo="anchura",evita_repetidos = False)
    r = pastor.genera_ruta("1111", "0000")
    print(r)

if __name__ == "__main__":
    main()
