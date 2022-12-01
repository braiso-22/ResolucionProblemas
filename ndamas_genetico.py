import random


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
        for i in range(len(self.posiciones)):
            total = self.mal_colocadas + otro.mal_colocadas
            # ejemplo 5 y 1
            if random.randint(0, total) < self.mal_colocadas:
                posiciones.append(self.posiciones[i])
            else:
                posiciones.append(otro.posiciones[i])
        # devolvemos el nuevo individuo
        return Estado(posiciones)

    def __evalua_estado(self):
        '''
        se le pasa individuo y devuelve la calidad
        devuelve el número de damas mal colocadas
        0 es lo mejor, y ndamas lo peor
        '''
        mal_colocadas = 0
        # bucle para contar las que están en la misma fila,
        # incrementando mal_colocadas por cada una que esté mal
        for dama in self.posiciones:
            for dama2 in self.posiciones:
                if dama.fila == dama2.fila and dama.columna != dama2.columna:
                    mal_colocadas += 1

        # bucle para contar las que están en la misma columna,
        # incrementando mal_colocadas por cada una que esté mal
        for dama in self.posiciones:
            for dama2 in self.posiciones:
                if dama.columna == dama2.columna and dama.fila != dama2.fila:
                    mal_colocadas += 1
        # bucle para contar las que están en la misma diagonal,
        # incrementando mal_colocadas por cada una que esté mal
        for dama in self.posiciones:
            for dama2 in self.posiciones:
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


class Posicion:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return "Fila: "+str(self.fila)+" Columna: "+str(self.columna)


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
        for i in range(0, len(estados), 2):
            # cruzamos los estados i e i+1
            nuevo_estado = estados[i].reproducir_con(estados[i+1])
            nuevos_estados.append(nuevo_estado)
        return nuevos_estados

def evolucionar(poblacion, numero_generaciones):
    gestorEstados = GestorEstados()
    # bucle para las generaciones
    for i in range(numero_generaciones):
        # evaluamos la población
        poblacion = gestorEstados.ordena_estados(poblacion)
        # eliminamos los peores
        poblacion = gestorEstados.eliminar_peores(poblacion, 100)
        # cruzamos los estados
        poblacion_de_hijos = gestorEstados.cruza_estados(poblacion)
        # añadimos los hijos a la población
        poblacion = poblacion+poblacion_de_hijos
        poblacion = gestorEstados.ordena_estados(poblacion)

    return poblacion

def main():
    
    gestorEstados = GestorEstados()

    poblacion = evolucionar(gestorEstados.genera_estados(8, 100), 7)

    # evaluamos la población
    for i,estado in enumerate(poblacion):
        print(estado, "\n")
        if(i==3):
            break
    pass


if __name__ == '__main__':
    main()
