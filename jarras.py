from clases.clases_profesor import GrafoR


class Jarras(GrafoR):
    def __init__(self,final="5-5-0", capacidad_grande=10, capacidad_medio=7, capacidad_peque=3):
        GrafoR.__init__(self)
        self.final = final
        self.capacidad_grande = capacidad_grande
        self.capacidad_medio = capacidad_medio
        self.capacidad_peque = capacidad_peque
        # set capacidades to array of final values
        self.capacidades = [int(x) for x in self.final.split("-")]

    def es_final(self, nodo):
        return nodo == self.final

    def generar_sucesores(self, nodo):
        """
        Genera los sucesores de un nodo\n
        - el nodo es una cadena de 3 caracteres separados por guión\n
        - El primer caracter es la jarra de mayor capacidad\n
        - El segundo caracter es la jarra de capacidad media\n
        - El tercer caracter es la jarra de menor capacidad\n

        """
        hijos = []
        distancias_origen = []

        nodo = nodo.split("-")
        copia = nodo[:]
        posibles_hijos = []
        posibles_hijos.append(self.__llenar(copia, "grande", "medio"))
        copia = nodo[:]
        posibles_hijos.append(self.__llenar(copia, "grande", "peque"))
        copia = nodo[:]
        posibles_hijos.append(self.__llenar(copia, "medio", "grande"))
        copia = nodo[:]
        posibles_hijos.append(self.__llenar(copia, "medio", "peque"))
        copia = nodo[:]
        posibles_hijos.append(self.__llenar(copia, "peque", "grande"))
        copia = nodo[:]
        posibles_hijos.append(self.__llenar(copia, "peque", "medio"))
        # Remove None values
        posibles_hijos = [x for x in posibles_hijos if x is not None]
        
        for hijo in posibles_hijos:
            
            if self.__is_valid_son(hijo, nodo):
                nodo ="-".join(nodo)
                hijo = "-".join(hijo)
                hijos.append(hijo)
                distancias_origen.append(
                    1 + self.distancias_origen.get(nodo, 0))
                nodo = nodo.split("-")
        return hijos, distancias_origen

    def __llenar(self, nodo, jarra, jarra2):
        nodoInicial = nodo[:]
        grande = int(nodo[0])
        medio = int(nodo[1])
        peque = int(nodo[2])
        if jarra == "grande":
            if jarra2 == "medio":
                grande, medio = self.__vaciar(
                    grande, medio, self.capacidad_medio)
            elif jarra2 == "peque":
                grande, peque = self.__vaciar(
                    grande, peque, self.capacidad_peque)
        elif jarra == "medio":
            if jarra2 == "grande":
                medio, grande = self.__vaciar(
                    medio, grande, self.capacidad_grande)
            elif jarra2 == "peque":
                medio, peque = self.__vaciar(
                    medio, peque, self.capacidad_peque)
        elif jarra == "peque":
            if jarra2 == "grande":
                peque, grande = self.__vaciar(
                    peque, grande, self.capacidad_grande)
            elif jarra2 == "medio":
                peque, medio = self.__vaciar(
                    peque, medio, self.capacidad_medio)
        
        nodo = [str(grande), str(medio), str(peque)]
        if nodo == nodoInicial:
            return None
        return nodo

    def __vaciar(self, jarra, jarra2, capacidad):
        if jarra + jarra2 > capacidad:
            jarra = jarra - (capacidad - jarra2)
            jarra2 = capacidad
        else:
            jarra2 += jarra
            jarra = 0
        return jarra, jarra2

    def __is_valid_son(self, hijo, padre):
        if hijo == padre:
            return False
        if self.__count_changes(hijo, padre) != 2:
            return False
        if int(hijo[0]) > self.capacidad_grande:
            return False
        if int(hijo[1]) > self.capacidad_medio:
            return False
        if int(hijo[2]) > self.capacidad_peque:
            return False
        if int(hijo[0]) < 0 or int(hijo[1]) < 0 or int(hijo[2]) < 0:
            return False
        # Sumar el total de las jarras
        if sum([int(x) for x in hijo]) != self.capacidad_grande:
            return False

        return True

    def __count_changes(self, str1, str2):
        count = 0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                count += 1
        return count

    def evalua_individuo(self, estado):
        estado = estado.split("-")
        numero_jarras = len(estado)
        litros_mal_situados = 0
        jarra = 0
        while jarra < (numero_jarras):
            contenido_esperado = self.capacidades[jarra]
            contenido_real = estado[jarra]
            litros_mal_situados += abs(int(contenido_esperado) - int(contenido_real))

            jarra += 1

        return litros_mal_situados


def main():
    solucion = "5-5-0"
    inicial = "10-0-0"
    jarra_grande = 10
    jarra_medio = 7
    jarra_peque = 3
    jarras = Jarras(solucion,jarra_grande,jarra_medio,jarra_peque)
    jarras.recorre_grafo(inicial, modo="dijkstra", evita_repetidos=False)
    ruta = jarras.genera_ruta(solucion, inicial)
    print(ruta)


if __name__ == "__main__":
    main()
