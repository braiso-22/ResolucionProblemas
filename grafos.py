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

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def set_position(self, x, y):
        self.position = Position(x, y)

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


class Route:
    def __init__(self, connections, initial_node, final_node):
        self.connections = connections
        self.final_node = final_node

    def __str__(self):
        return str(self.connections)

    def __repr__(self):
        return str(self)


class Graph:
    def __init__(self, nodes=5, visual=False):
        list = []
        self.nodes = list[:]
        self.visual = visual
        self.fastest_route = Route([], 0, 0)

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

        A.set_position(1, 3)
        A.add_connection(Connection(A, B, 3))
        A.add_connection(Connection(A, C, 1))

        B.set_position(3, 4)
        B.add_connection(Connection(B, A, 3))
        B.add_connection(Connection(B, C, 7))
        B.add_connection(Connection(B, D, 5))
        B.add_connection(Connection(C, E, 1))

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
        current_node = self.nodes[start_node]
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

                if smaller_node.current_value > connection.node2.current_value:
                    smaller_node = connection.node2

            current_node.visited = True
            current_node = smaller_node

    def set_fastest_route(self, start_node, end_node):
        self.fastest_route.final_node = self.nodes[end_node]
        self.fastest_route.connections = []
        current_node = self.nodes[end_node]
        while current_node != self.nodes[start_node]:
            for connection in current_node.connections:
                if connection.node2.current_value == current_node.current_value - connection.weight:
                    self.fastest_route.connections.append(connection)
                    current_node = connection.node2
                    break
        self.fastest_route = Route(
            self.fastest_route.connections[::-1], start_node, end_node)
        return self.fastest_route

    def print_graph(self):
        grafics.rcParams['axes.facecolor'] = 'black'
        grafics.figure(figsize=(20, 10))

        if not self.visual:
            print("current graph is not visualizable")
            return

        for node in self.nodes:
            for connection in node.connections:
                if connection in self.fastest_route.connections:
                    color = "white"
                    linewidth=4
                    zorder=10
                else: 
                    color = "blue"
                    linewidth=2
                    zorder=5
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

        pass

    def __str__(self):
        return "Graph: " + str(self.nodes)

    def __repr__(self):
        return str(self)


def main():  # Create a graph with the nodes
    graph = Graph(visual=True).create_example_graph()

    print(graph)
    graph.print_graph()
    graph.calculate_nodes_value(4)

    print()
    print(graph)
    graph.set_fastest_route(4, 2)
    graph.print_graph()

    pass


if __name__ == '__main__':
    main()