import random


class Node:
    def __init__(self, name, conections=list([])):
        self.name = name
        self.visited = False
        self.current_value = float('inf')
        self.connections = conections[:]

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def __str__(self):
        return "Nodo: " + self.name + " " + str(self.current_value) + " " + str(self.connections)

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


class Graph:
    def __init__(self, nodes=5):
        list = []
        self.nodes = list[:]

    def add_node(self, node):
        self.nodes.append(node)

    def create_example_graph(self):
        ''' 
            Example graph from: 
            https://www.codingame.com/playgrounds/7656/los-caminos-mas-cortos-con-el-algoritmo-de-dijkstra/el-algoritmo-de-dijkstra
        '''
        for i in range(5):
            self.add_node(Node(chr(65+i)))

        A = self.nodes[0]
        B = self.nodes[1]
        C = self.nodes[2]
        D = self.nodes[3]
        E = self.nodes[4]

        A.add_connection(Connection(A, B, 3))
        A.add_connection(Connection(A, C, 1))

        B.add_connection(Connection(B, A, 3))
        B.add_connection(Connection(B, C, 7))
        B.add_connection(Connection(B, D, 5))
        B.add_connection(Connection(C, E, 1))

        C.add_connection(Connection(C, A, 1))
        C.add_connection(Connection(C, B, 7))
        C.add_connection(Connection(C, D, 2))

        D.add_connection(Connection(D, B, 5))
        D.add_connection(Connection(D, C, 2))
        D.add_connection(Connection(D, E, 7))

        E.add_connection(Connection(E, B, 1))
        E.add_connection(Connection(E, D, 7))
        return self

    def create_random_graph(self, n):
        for i in range(n):
            self.add_node(chr(65+i))

        i = 0
        while i < len(self.nodes):
            random_int = random.randint(0, len(self.nodes) - 2)
            if (i == random_int):
                continue
            node = self.nodes[i]
            node.add_connection(Connection(
                self.nodes[i], self.nodes[random_int], random.randint(1, 10)))
            i += 1
        return self

    def calculate_nodes_value(self, start_node):
        '''
        for i, node in enumerate(self.nodes):
            if node.visited:
                continue
            node.visited = True
            if (i == 0):
                node.current_value = 0

            for connection in node.connections:
                if connection.node2.current_value > node.current_value + connection.weight:
                    connection.node2.current_value = node.current_value + connection.weight
        '''
        nodos_visitados = []
        i = 0
        while (len(list(dict.fromkeys(nodos_visitados))) < len(self.nodes)):
            for node in self.nodes:
                if node.visited:
                    nodos_visitados.append(node)

            if (i == 0):
                current_node = self.nodes[start_node]
                current_node.current_value = 0
                i += 1

            smaller_node = Node("Infinity")
            for connection in current_node.connections:
                if connection.node2.visited == True:
                    continue
                if connection.node2.current_value > current_node.current_value + connection.weight:
                    connection.node2.current_value = current_node.current_value + connection.weight

                if smaller_node.current_value > connection.node2.current_value:
                    smaller_node = connection.node2
            current_node.visited = True
            current_node = smaller_node

    def __str__(self):
        return "Graph: " + str(self.nodes)

    def __repr__(self):
        return str(self)


def main():  # Create a graph with the nodes
    graph = Graph().create_example_graph()

    print(graph)
    graph.calculate_nodes_value(2)

    print()
    print(graph)
    pass


if __name__ == '__main__':
    main()
