"""
 representar grafos en memoria
 para algoritmo dijkstra
 cada nodo del grafo es un diccionario de la forma nombre_nodo:lista_de_aristas
 cada arista de la lista tiene el nombre del nodo al que conecta y su coste

 Hay otro diccionario de posiciones x,y de cada nodo

 y hay otro diccionario que se crea al vuelo con nodo:valor
"""
import math
import matplotlib.pyplot as plt
#%matplotlib inline


class Grafo:
  grafo_pruebas = {"A":[["B", 3], ["C", 1]],
            "B":[["A", 3], ["C", 7], ["D", 5], ["E", 1]],
            "C":[["A", 1], ["B", 7], ["D", 2]],
            "D":[["B", 5], ["C", 2], ["E", 7]],
            "E":[["B", 1], ["D", 7]],
            
            }
  grafo_pruebas_posiciones = {"A": [1,4],
                        "B": [3,5],
                        "C": [2,3],
                        "D": [4,3],
                        "E": [5,6],
                        }
  
  def __init__(self):
    self.name = "Grafo"
    self.grafo = {}
    self.grafo_posiciones = None

  def __str__(self):
    for nodo in self.grafo:
      print(f"{nodo} -> {self.get_aristas()}")


  # opción1, definir el grafo a pelo y opcionalmente las posiciones de los nodos
  def carga_grafo_pruebas(self):
    self.grafo = self.grafo_pruebas
    self.grafo_posiciones = self.grafo_pruebas_posiciones


  # añade el nodo al grafo
  # no devuelve nada
  def add_nodo(self, nodo):
    if not nodo in self.grafo:
      self.grafo[nodo] = []

  # añade la arista al grafo
  # si no existen los nodos los crea
  def add_arista(self, nodo_desde, nodo_hasta, coste):
    self.add_nodo(self, nodo_desde)
    self.add_nodo(self, nodo_hasta)
    self.grafo[nodo_desde].append([nodo_hasta, coste])
    self.grafo[nodo_hasta].append([nodo_desde, coste])


  # quita el nodo al grafo
  # no devuelve nada
  def del_nodo(self, nodo):
    aristas = self.get_aristas(self.grafo, nodo)
    nodos = [arista[0] for arista in aristas]
    for n in nodos:
      self.del_arista(self.grafo, nodo, n) 
    self.grafo.pop(nodo)


  # añade la arista al grafo
  # crea los nodos si no existen
  def del_arista(self, nodo_desde, nodo_hasta, coste=None):
    hijos_nodo_desde = self.get_aristas(self.grafo, nodo_desde)
    # grafo[nodo_desde] = [arista for arista in hijos_nodo_desde if arista[0] != nodo_hasta]
    hijos = []
    for arista in hijos_nodo_desde:
      if arista[0] != nodo_hasta: hijos.append(arista)
    self.grafo[nodo_desde] = hijos

    hijos_nodo_hasta = self.get_aristas(self, nodo_hasta)
    hijos = []
    for arista in hijos_nodo_hasta:
      if arista[0] != nodo_desde: hijos.append(arista)
    self.grafo[nodo_hasta] = hijos


  # retorna una lista de las aristas que conectan el nodo
  # cada arista es una lista con el nodo a que conecta y su coste
  def get_aristas(self, nodo):
    return self.grafo[nodo]

  # retorna un grafo cargado desde el fichero
  # el fichero está formado por líneas con el formato nodo;nodo;coste
  # devuelve el grafo reconstruido
  def carga_grafo(self, fichero):
    self.grafo = {}
    f = open(fichero, "r")
    lineas = f.readlines()
    f.close()
    for linea in lineas:
      if linea[0] == "#": continue
      partes = linea.split(sep=";")
  #    print(partes)
      if len(partes) != 3: continue
      nodo1 = partes[0]
      nodo2 = partes[1]
      costo = float(partes[2])
      self.add_arista(nodo1, nodo2, costo)
    return self

  # guarda un grafo en el fichero ....
  def guarda_grafo(self, fichero):
    lista_de_aristas = []
    # lista_de_aristas es una lista como [[nodo1, nodo2, coste1], [nodo1, nodo2, coste2],...]
    for nodo, aristas in self.grafo.items():
      for arista in aristas:
        ar = [nodo, arista[0], arista[1]]
        if ar in lista_de_aristas: continue
        ar = [arista[0], nodo, arista[1]]
        if ar in lista_de_aristas: continue

        lista_de_aristas.append(ar)

    f = open(fichero, "wt")
    # escribir todo lo de la lista_de_aristas al fichero 
    # y separado por ;
    for elemento in lista_de_aristas:
      f.write(f"{elemento[0]};{elemento[1]};{elemento[2]}\n")
    f.close()


# fichero_posiciones en un fichero de posciones con la estructura:
# A;valor;valor\n     B;valor;valor\n      .......
  def carga_grafo_posiciones(self, fichero_posiciones):
    self.grafo_posiciones = {}
    with open(fichero_posiciones) as f:
      lineas = f.readlines()
      # print(lineas)
      for linea in lineas:
          elementos = linea.split(sep=";")
          if len(elementos) != 3: continue
          self.grafo_posiciones[elementos[0]] = [float(elementos[1]), float(elementos[2])]

  # genera un diccionario de posiciones para colocar los nodos
  # es para el caso de que no se proporcionen
  def genera_posiciones(self):
    self.grafo_posiciones = {}
    y_inicial = (len(self.grafo) * 4)/2
    x_inicial = 2
    inc = 1
    for orden, n in enumerate(self.grafo):
      self.grafo_posiciones[n] = [x_inicial + orden, y_inicial + (orden*inc)*(1 if orden%2 else -1)]
      inc += 0.5


  # de un diccionario de posiciones devuelve los límites de (x, y) mímimos y máximo
  def limites_posiciones(self):
    xmin = 100000
    xmax = -100000
    ymin = 100000
    ymax = -100000
    for vertice, posicion in self.grafo_posiciones.items():
      if posicion[0] < xmin: xmin = posicion[0]
      if posicion[0] > xmax: xmax = posicion[0]
      if posicion[1] < ymin: ymin = posicion[1]
      if posicion[1] > ymax: ymax = posicion[1]
    return xmin, xmax, ymin, ymax

  # valores es un diccionario nodo:valor
  # ruta es una lista de nodos en la  que se quiere resaltar la ruta que los une
  def dibuja_grafo(self, posiciones=None, valores=None, ruta=None):
    fig = plt.figure(figsize=(20,10))

    # si no nos indican donde, intentamos colocar los vértices donde podamos
    if posiciones == None: 
      self.genera_posiciones()
      posiciones = self.grafo_posiciones
  
    # dibujamos los vértices
    for vertice, posicion in posiciones.items():
      plt.scatter(posicion[0], posicion[1], s=1000, color='b')
      plt.text(posicion[0], posicion[1], vertice)
    
    # dibujamos las aristas y las distancias
    for vertice, aristas in self.grafo.items():
      posicion_org = posiciones[vertice]
      x_org, y_org = posicion_org[0], posicion_org[1]
      for arista in aristas:
        vertice_destino = arista[0]
        distancia = arista[1]
        posicion_dst = posiciones[vertice_destino]
        x_dst, y_dst = posicion_dst[0], posicion_dst[1]
        # si estos dos vértices son consecutivos en ruta, se dibujan en rojo, sino en verde
        color_p = "g"
        if ruta and vertice in ruta and vertice_destino in ruta and abs(ruta.index(vertice_destino)-ruta.index(vertice)) == 1: color_p = "r"
        plt.plot([x_org, x_dst], [y_org, y_dst], color=color_p)
        plt.text((x_org + x_dst)/2, (y_org + y_dst)/2, str(distancia))
    
    # dibujamos el valor que tiene cada vértice
    if valores:
      for vertice, valor in valores.items():
        posicion = posiciones[vertice]
        plt.text(posicion[0], posicion[1]+0.4, str(valor))

    # ponemos los límites y a dibujar...
    xmin, xmax, ymin, ymax = self.limites_posiciones()
    plt.xlim(xmin-2, xmax+2), plt.ylim(ymin-2, ymax+2)
    plt.show()





class GrafoR(Grafo):
    def __init__(self):
        Grafo.__init__(self)
        self.name = "GrafoR"
        self.nodos_abiertos = []
        self.nodos_cerrados = []
        self.distancias_origen = {}
        self.distancias_destino = {}
        self.padres = {}
        self.evita_repetidos = True

    def pop_primero(self, lista):
        n = lista.pop(0)
        #n = lista.pop()
        return n

    def pop_ultimo(self, lista):
        n = lista.pop()
        return n

    def pop_menor_distancia(self, lista, d_org=None, d_dst=None):
        d = math.inf
        nodo = None
        for n in lista:
            d1 = 0
            if d_org:
                d1 += d_org.get(n, math.inf)
            if d_dst:
                d1 += d_dst.get(n, math.inf)
            if d1 <= d:
                d = d1
                nodo = n
        if nodo is not None:
            lista.remove(nodo)
        return nodo

    def es_final(self, nodo):
        print(nodo)
        return False

    def generar_heuristicas(self, nodos, nodo_destino):
        d_dest = []
        for nodo in nodos:
            d_dest.append(math.inf)
        return d_dest

    # devuelve una lista de nodos hijo y otra lista con sus distancias al origen (la del nodo + la arista)

    def generar_sucesores(self, nodo):
        hijos = []
        d_org = []
        aristas = self.get_aristas(nodo)
        for arista in aristas:
            hijos.append(arista[0])
            d_org.append(arista[1] + self.distancias_origen.get(nodo, 0))
        return hijos, d_org

    # recibe una lista de hijos   [[nodo_hijo, d_org, d_dest], ....]
    # añade el nodo a abiertos
    # si el nodo está en cerrados pero tiene menor distancia al origen lo reabre
    # si el nodo está en abiertos pero tiene menor distancia al origen lo sustituye
    def tratar_repetidos(self, padre, lhijos):
        for lhijo in lhijos:
            hijo, d_org, d_dst = lhijo
            if d_org > self.max_profundidad:
                continue

            if hijo in self.nodos_cerrados:
                if self.evita_repetidos:
                    continue
                if self.distancias_origen.get(hijo, 0) <= d_org:
                    continue
                self.nodos_cerrados.remove(hijo)  # reabrir el nodo

            if hijo in self.nodos_abiertos:
                if self.evita_repetidos:
                    continue
                if self.distancias_origen.get(hijo, 0) <= d_org:
                    continue
            else:
                self.nodos_abiertos.append(hijo)

            self.distancias_origen[hijo] = d_org
            self.distancias_destino[hijo] = d_dst
            self.padres[hijo] = padre

    def recorre_grafo(self, ini, end=None, modo="anchura", evita_repetidos="True"):
        self.nodos_abiertos = []
        self.nodos_cerrados = []
        self.padres = {}
        self.distancias_origen = {}
        self.distancias_destino = {}
        self.max_profundidad = math.inf
        self.evita_repetidos = evita_repetidos
        self.end = end
        self.ini = ini
        self.modo = modo
        g = GrafoR()
        for n in g.grafo:
            self.distancias_origen[n] = math.inf
        self.distancias_origen[ini] = 0

        self.nodos_abiertos.append(ini)
        while True:
            if len(self.nodos_abiertos) == 0:
                #        print("Llegué al final sin encontrar solución")
                break

            if modo == "anchura":
                Actual = self.pop_primero(self.nodos_abiertos)
            elif modo == "profundidad":
                Actual = self.pop_ultimo(self.nodos_abiertos)
            elif modo == "dijkstra":
                Actual = self.pop_menor_distancia(
                    self.nodos_abiertos, d_org=self.distancias_origen)
            elif modo == "avaricioso":
                Actual = self.pop_menor_distancia(
                    self.nodos_abiertos, d_dst=self.distancias_destino)
            elif modo == "A*":
                Actual = self.pop_menor_distancia(
                    self.nodos_abiertos, d_org=self.distancias_origen, d_dst=self.distancias_destino)

    #    print(f"Procesando {Actual}")
            if self.es_final(Actual):
                print(f"hallada solución: {Actual}")
                return 1
            self.nodos_cerrados.append(Actual)
            hijos, d_org = self.generar_sucesores(Actual)
            d_dest = self.generar_heuristicas(hijos, end)
            self.tratar_repetidos(Actual, list(zip(hijos, d_org, d_dest)))

        return 0

    def recorrido_recursivo(self, nodo_inicio=None):
        self.nodos_cerrados = []
        if nodo_inicio is None:
            nodo_inicio = list(self.grafo.keys())[0]
        self.distancias_origen[nodo_inicio] = 0
        return self.recorrido_recursivo_aux(nodo_inicio)

    def recorrido_recursivo_aux(self, Actual):
        if self.es_final(Actual) == True:
            print(f"hallada solución: {Actual}")
        self.nodos_cerrados.append(Actual)
        hijos, _ = self.generar_sucesores(Actual)
        for hijo in hijos:
            if hijo in self.nodos_cerrados:
                continue
            self.recorrido_recursivo2(hijo)

    def genera_ruta(self, nodo_end, nodo_ini=None):
        ruta = []
        nodo = nodo_end
        while (nodo != None):
            ruta.append(nodo)
            if nodo_ini and nodo == nodo_ini:
                break
            nodo = self.padres.get(nodo, None)
        ruta = ruta[::-1]
        return ruta