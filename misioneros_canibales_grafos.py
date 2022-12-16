from clases.clases_profesor import GrafoR

class Misioneros(GrafoR):
    def __init__(self):
        GrafoR.__init__(self)
        self.numero_elementos = 7

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
        return nodo == "1"*self.numero_elementos

    def generar_sucesores(self, nodo):
        """
        Genera los sucesores de un nodo\n
        - el nodo es una cadena de 7 caracteres\n
        - el primer caracter es el estado del barco\n
        - el segundo, tercer y cuarto caracteres son el estado del los misioneros\n
        - el quinto caracter es el estado del canibal que rema\n
        - el sexto y septimo caracter es el estado de los otros canibales\n

        - 0 es izquierda\n
        - 1 es derecha
        """
        hijos = []
        distancias_origen = []
        for i in range(0, 2**self.numero_elementos):
            nodo_nuevo = format(i, f'0{self.numero_elementos}b')
            if not self.__is_valid_son(nodo_nuevo, nodo):
                continue
            hijos.append(nodo_nuevo)

            distancias_origen.append(
                1 + self.distancias_origen.get(nodo, 0))

        

        return hijos, distancias_origen

    def __is_valid_son(self, hijo, padre):
        barco = hijo[0]
        barco_padre = padre[0]
        numero_misioneros =hijo[1:4]
        numero_misioneros_derecha= numero_misioneros.count("1")
        numero_misioneros_izquierda= numero_misioneros.count("0")

        numero_canibales = hijo[4:]
        numero_canibales_derecha = numero_canibales.count("1")
        numero_canibales_izquierda = numero_canibales.count("0")

        canibales_que_no_reman = hijo[5:]
        canibales_que_no_reman_padre = padre[5:]

        personas = hijo[1:]
        personas_padre = padre[1:]
        
        # No cambia el barco
        if barco == barco_padre:
            return False
        # Se mueven más de dos en la barca
        if self.__count_changes(hijo, padre) > 3:
            return False
        # Se mueve la barca sola
        # ejemplo: 0000011 1000011
        if self.__count_changes(personas, personas_padre) == 0:
            return False
        # Más canibales que misioneros en la izquierda si hay misioneros
        if numero_misioneros_izquierda < numero_canibales_izquierda and numero_misioneros_izquierda!=0:
            return False
        # Más canibales que misioneros en la izquierda si hay misioneros
        if numero_misioneros_derecha < numero_canibales_derecha and numero_misioneros_derecha!=0:
            return False
        # Se mueven los 2 canibales que no reman
        if self.__count_changes(canibales_que_no_reman, canibales_que_no_reman_padre) == 2:
            return False
        # Se mueve solo uno de los 2 canibales que no reman
        if self.__count_changes(canibales_que_no_reman, canibales_que_no_reman_padre) == 1 and self.__count_changes(hijo, padre)==2:
            return False
        # Los que se mueven no están en la misma orilla que el barco
        if self.__change_not_in_same_side(hijo, padre, barco):
            return False
        
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
    misioneros = Misioneros()
    misioneros.recorre_grafo("0000000",modo="dijkstra",evita_repetidos = False)
    ruta = misioneros.genera_ruta("1111111", "0000000")
    print(ruta)

if __name__ == "__main__":
    main()

