import random
import matplotlib.pyplot as grafics


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)


class Node:
    def __init__(self, name, conections=list([]), position=Position(0, 0)):
        self.name = name
        self.visited = False
        self.current_value = float('inf')
        self.connections = conections[:]
        self.position = position
        self.parent = None

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def set_position(self, x, y):
        self.position = Position(x, y)

    def __str__(self):
        string = "Nodo: " + self.name + " " + \
            str(self.current_value) + "\n" + "│\t└───Conexiones: \n"
        for i, connection in enumerate(self.connections):
            string += "│\t\t└───" if i == len(self.connections) - \
                1 else "│\t\t├───" + str(connection)+"\n"
        return string

    def __repr__(self):
        return str(self)


class Connection:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def __str__(self):
        return self.node1.name + " " + self.node2.name + " " + str(self.weight)

    def __repr__(self):
        return str(self)


class Route:
    def __init__(self, connections=list([])):
        self.connections = connections[:]
        self.weight = 0

    def __str__(self):
        return str(self.connections)

    def __repr__(self):
        return str(self)


class Graph:
    def __init__(self):
        list = []
        self.nodes = list[:]
        self.fastest_route = Route()
        self.start_node = None

    def add_node(self, node):
        self.nodes.append(node)

    def delete_node(self, node_name):
        del_node = self.get_node_by_name(node_name)
        for node in self.nodes:
            for connection in node.connections:
                if connection.node2 == del_node:
                    node.connections.remove(connection)

        self.nodes.remove(del_node)

    def add_connection(self, node_name1, node_name2, weight):
        node1 = self.get_node_by_name(node_name1)
        node2 = self.get_node_by_name(node_name2)
        node1.add_connection(Connection(node1, node2, weight))
        node2.add_connection(Connection(node2, node1, weight))

    def add_position(self, node_name, x, y):
        node = self.get_node_by_name(node_name)
        node.set_position(x, y)

    def create_example_graph(self):
        ''' 
            Example graph from: 
            https://www.codingame.com/playgrounds/7656/los-caminos-mas-cortos-con-el-algoritmo-de-dijkstra/el-algoritmo-de-dijkstra
        '''
        for i in range(6):
            self.add_node(Node(chr(65+i)))

        A = self.nodes[0]
        B = self.nodes[1]
        C = self.nodes[2]
        D = self.nodes[3]
        E = self.nodes[4]
        F = self.nodes[5]

        A.set_position(1, 3)
        A.add_connection(Connection(A, B, 3))
        A.add_connection(Connection(A, C, 1))

        B.set_position(3, 4)
        B.add_connection(Connection(B, A, 3))
        B.add_connection(Connection(B, C, 7))
        B.add_connection(Connection(B, D, 5))
        B.add_connection(Connection(B, E, 1))

        C.set_position(2, 1)
        C.add_connection(Connection(C, A, 1))
        C.add_connection(Connection(C, B, 7))
        C.add_connection(Connection(C, D, 2))

        D.set_position(4, 2)
        D.add_connection(Connection(D, B, 5))
        D.add_connection(Connection(D, C, 2))
        D.add_connection(Connection(D, E, 7))

        E.set_position(5, 5)
        E.add_connection(Connection(E, B, 1))
        E.add_connection(Connection(E, D, 7))
        E.add_connection(Connection(E, F, 3))

        F.set_position(6, 3)
        F.add_connection(Connection(F, E, 3))

        return self

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def create_graph_from_file(self, file, separator=";"):
        with open(file, 'r') as f:
            lines = f.readlines()

            # Create nodes
            for line in lines:
                line = line.replace("\n", "")
                line = line.split(separator)
                node_exists = False
                for node in self.nodes:
                    if node.name == line[0]:
                        node_exists = True
                        break
                if not node_exists:
                    node = Node(line[0])
                    self.add_node(node)

            # Create connections
            for line in lines:
                line = line.replace("\n", "")
                line = line.split(";")
                node = self.get_node_by_name(line[0])
                node.add_connection(
                    Connection(
                        node,
                        self.get_node_by_name(line[1]),
                        int(line[2])
                    )
                )

        return self

    def set_nodes_location_from_file(self, file, separator=";"):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n", "")
                line = line.split(separator)
                node = self.get_node_by_name(line[0])
                node.set_position(int(line[1]), int(line[2]))

    def create_random_graph(self, n):
        self.__restart()
        for i in range(n):
            self.add_node(Node(chr(65+i)))

        i = 0
        while i < len(self.nodes):
            random_int = random.randint(0, len(self.nodes) - 2)
            if (i == random_int):
                continue
            node = self.nodes[i]
            node.add_connection(Connection(
                self.nodes[i], self.nodes[random_int],random_int))
            node.add_connection(Connection(
                self.nodes[random_int], self.nodes[i], random_int))
            i += 1
        return self

    def __restart(self):
        self.fastest_route = Route()
        for node in self.nodes:
            node.visited = False
            node.current_value = float('inf')
            node.parent = None

    def calculate_nodes_value(self, start_node, final_node=None):
        self.__restart()
        my_start_node = self.get_node_by_name(start_node)
        if my_start_node == None:
            print(f"Start node '{start_node}' not found")
            print("Available nodes:")
            self.print_graph(True)
            return
        nodos_visitados = []
        current_node = my_start_node
        current_node.current_value = 0

        while (len(list(dict.fromkeys(nodos_visitados))) < len(self.nodes)):
            for node in self.nodes:
                if node.visited:
                    nodos_visitados.append(node)

            smaller_node = Node("Infinity")
            for connection in current_node.connections:
                if connection.node2.visited == True:
                    continue
                if connection.node2.current_value > current_node.current_value + connection.weight:
                    connection.node2.current_value = current_node.current_value + connection.weight
                    connection.node2.parent = current_node

                if smaller_node.current_value > connection.node2.current_value:
                    smaller_node = connection.node2

            current_node.visited = True

            smaller_node = Node("Infinity")
            for node in self.nodes:
                if node.visited:
                    continue
                if smaller_node.current_value > node.current_value:
                    smaller_node = node
            if smaller_node.name == "Infinity":
                break
            current_node = smaller_node

            # Cuando se llega a un nodo que no tiene mas conexiones y no se han visitado todos los nodos
            # Se vuelve al nodo inicial y se continua con el siguiente nodo

        if final_node != None:
            self.__set_fastest_route_to(start_node, final_node)

    def __set_fastest_route_to(self, initial, end_node):
        current_node = self.get_node_by_name(end_node)
        start_node = self.get_node_by_name(initial)
        while current_node != start_node:
            for connection in current_node.connections:
                if connection.node2 == current_node.parent:
                    self.fastest_route.connections.append(connection)
                    current_node = connection.node2
                    break

    def print_graph(self):
        print(self)

    def print_visual_graph(self):
        grafics.rcParams['axes.facecolor'] = 'black'
        grafics.figure(figsize=(20, 10))

        for node in self.nodes:
            for connection in node.connections:
                if connection in self.fastest_route.connections:
                    color = "white"
                    linewidth = 4
                    zorder = 10
                else:
                    color = "blue"
                    linewidth = 2
                    zorder = 5
                grafics.plot([node.position.x, connection.node2.position.x],
                             [node.position.y, connection.node2.position.y],
                             color=color, linewidth=linewidth, zorder=zorder)
                grafics.text((node.position.x + connection.node2.position.x)/2,
                             ((node.position.y + connection.node2.position.y)/2)+0.1, connection.weight, color="white")

            grafics.scatter(node.position.x, node.position.y,
                            color='Green', s=1500, zorder=11)
            grafics.text(node.position.x-0.02, node.position.y,
                         node.name, fontsize=12, zorder=15, color='White')
            grafics.text(node.position.x-0.02, node.position.y+0.2,
                         node.current_value, fontsize=12, zorder=15, color='RED')

        grafics.show()

    def __str__(self):
        '''
            TODO: Fix bad visualizations
        '''
        string = "Graph: \n"
        for i, node in enumerate(self.nodes):
            string += "└───" if i == len(self.nodes) - \
                1 else "├───" + str(node)+"\n"
        return string

    def __repr__(self):
        return str(self)


def main():
    # Create graph from file
    graph = Graph().create_graph_from_file("graph.csv")
    graph.set_nodes_location_from_file("graph_locations.csv")

    # Calculate nodes values from node A
    graph.calculate_nodes_value("C", "A")

    graph.print_visual_graph()
    graph.delete_node("A")
    node = Node("A'")
    graph.add_node(node)
    graph.add_connection("A'", "B", 1)
    graph.add_connection("A'", "C", 3)

    graph.add_position("A'", 1, 2)
    graph.calculate_nodes_value("C", "E")
    graph.print_visual_graph()

    pass


if __name__ == '__main__':
    main()
