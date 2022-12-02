import random

def genera_random(numero):
    return random.randint(0, numero-1)

class Estado:
    def __init__(self, posiciones):
        self.posiciones = posiciones
        self.mal_colocadas = self.__evalua_estado()

    def reproducir_con(self, otro):
        '''
        Recibe otro individuo y devuelve un nuevo individuo
        '''
        # creamos una lista de posiciones vacía
        posiciones = []
        # bucle para ir cogiendo posiciones de los padres
        
        num = genera_random(len(self.posiciones))

        better = self if self.mal_colocadas < otro.mal_colocadas else otro

        worse = self if self.mal_colocadas > otro.mal_colocadas else otro

        for i in range(len(self.posiciones)):
            if i == num:
                posiciones.append(
                    worse.posiciones[i]
                )
                continue
            posiciones.append(better.posiciones[i])

        posiciones[genera_random(len(self.posiciones))] = Posicion().get_random_posicion(len(self.posiciones))
        # devolvemos el nuevo individuo
        return Estado(posiciones)

    def __evalua_estado(self):
        '''
        se le pasa individuo y devuelve la calidad
        devuelve el número de damas mal colocadas
        0 es lo mejor, y ndamas lo peor
        '''
        mal_colocadas = 0
        # Están en la misma casilla
        for i, dama in enumerate(self.posiciones):
            for j, dama2 in enumerate(self.posiciones):
                if i == j:
                    continue
                if dama.fila == dama2.fila and dama.columna == dama2.columna:
                    mal_colocadas += 1

        # bucle para contar las que están en la misma fila,
        # incrementando mal_colocadas por cada una que esté mal
        for i, dama in enumerate(self.posiciones):
            for j, dama2 in enumerate(self.posiciones):
                if i == j:
                    continue
                if dama.fila == dama2.fila and dama.columna != dama2.columna:
                    mal_colocadas += 1

        # bucle para contar las que están en la misma columna,
        # incrementando mal_colocadas por cada una que esté mal
        for i, dama in enumerate(self.posiciones):
            for j, dama2 in enumerate(self.posiciones):
                if i == j:
                    continue
                if dama.columna == dama2.columna and dama.fila != dama2.fila:
                    mal_colocadas += 1
        # bucle para contar las que están en la misma diagonal,
        # incrementando mal_colocadas por cada una que esté mal
        for i, dama in enumerate(self.posiciones):
            for j, dama2 in enumerate(self.posiciones):
                if i == j:
                    continue
                if abs(dama.fila - dama2.fila) == abs(dama.columna - dama2.columna) and dama.fila != dama2.fila:
                    mal_colocadas += 1

        return mal_colocadas

    def __str__(self):
        string = ''
        for dama in self.posiciones:
            string += str(dama)+"\n"
        string += "Mal colocadas: "+str(self.mal_colocadas)
        return string

    def __lt__(self, other):
        return self.mal_colocadas < other.mal_colocadas

    def print(self):
        estado = []
        for i in range(len(self.posiciones)):
            estado.append([])
            for j in range(len(self.posiciones)):
                estado[i].append("0")
        for dama in self.posiciones:
            estado[dama.fila][dama.columna] = "X"
        for fila in estado:
            string = ""
            for columna in fila:
                string += columna + " "
            print(string)
        print("\n")


class Posicion:
    def __init__(self, fila=0, columna=0):
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return "Fila: "+str(self.fila)+" Columna: "+str(self.columna)

    def __repr__(self):
        return self.__str__()

    def get_random_posicion(self, n):
        return Posicion(random.randint(0, n-1), random.randint(0, n-1))


class GestorEstados:
    def __genera_estado(self, tamaño):
        # genera un estado al azar y lo devuelve
        posiciones = []
        for i in range(tamaño):
            posiciones.append(Posicion(random.randint(
                0, tamaño-1), random.randint(0, tamaño-1)))
        estado = Estado(posiciones)
        return estado

    def genera_estados(self, tamaño, numero_estados):
        # genera nindividuos al azar y devuévelos en una lista que sea
        # [[indiv, calidad], [indiv, calidad], .....]
        poblacion = []
        for i in range(numero_estados):
            estado = self.__genera_estado(tamaño)
            poblacion.append(estado)
        return poblacion

    def ordena_estados(self, estados):
        # ordena los estados por su calidad
        estados.sort()
        return estados

    def eliminar_peores(self, estados, estados_mantenidos):
        # elimina los peores estados
        return estados[:estados_mantenidos]

    def cruza_estados(self, estados):
        # cruza los estados para generar nuevos estados
        # devuelve una lista con los nuevos estados
        nuevos_estados = []
        for i in range(0, int(len(estados)/ 2)):
            # cruzamos los estados i e i+1
            reproductor = len(estados)-i-1
            nuevo_estado = estados[i].reproducir_con(estados[reproductor])
            nuevos_estados.append(nuevo_estado)
        return nuevos_estados


def evolucionar(poblacion, generaciones=0):
    gestorEstados = GestorEstados()
    generaciones_actuales=0
    if generaciones == 0:
        # bucle para las generaciones
        while (True):
            poblacion = gestorEstados.ordena_estados(poblacion)
            # eliminamos los peores
            poblacion = gestorEstados.eliminar_peores(poblacion, 100)
            # cruzamos los estados
            poblacion_de_hijos = gestorEstados.cruza_estados(poblacion)
            # añadimos los hijos a la población
            poblacion = poblacion+poblacion_de_hijos
            generaciones_actuales+=1
            poblacion = gestorEstados.ordena_estados(poblacion)
            if generaciones_actuales%100==0:
                print("Generación: "+str(generaciones_actuales))
            if poblacion[0].mal_colocadas == 0:
                break
    else:
        # bucle para las generaciones
        for i in range(generaciones):
            # evaluamos la población
            poblacion = gestorEstados.ordena_estados(poblacion)
            # eliminamos los peores
            poblacion = gestorEstados.eliminar_peores(poblacion, 100)
            # cruzamos los estados
            poblacion_de_hijos = gestorEstados.cruza_estados(poblacion)
            # añadimos los hijos a la población
            poblacion = poblacion+poblacion_de_hijos
            poblacion = gestorEstados.ordena_estados(poblacion)
    print("Generaciones: "+str(generaciones_actuales))
    return poblacion


def main():

    gestorEstados = GestorEstados()
    poblacion = evolucionar(
        gestorEstados.genera_estados(12, 100)
    )

    # evaluamos la población
    for i, estado in enumerate(poblacion):
        estado.print()
        print(estado, "\n")
        
        if (i == 1):
            break
    pass


if __name__ == '__main__':
    main()
