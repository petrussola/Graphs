class Stack:
    def __init__(self):
        self.stack = []

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edges(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise KeyError("Vertex does not exist")


def earliest_ancestor(ancestors, starting_node):
    # 1. we build the graph
    # create graph
    g = Graph()

    # iterate over ancestors
    for el in ancestors:
        # create vertices
        g.add_vertex(el[0])
        g.add_vertex(el[1])
        # create edges
        g.add_edges(el[1], el[0])
    # 2. for the starting node, we do a BFS
    # create a queue
    s = Stack()
    # add starting node as a list
    s.push([starting_node])
    max_length_path = 1
    earliest_ancestor = -1

    # while stack is not empty
    while s.size() > 0:
        # pop path
        path = s.pop()
        # get last vertex
        vertex = path[-1]
        #
        if (len(path) >= max_length_path and vertex < earliest_ancestor) or (len(path) > max_length_path):
            # set earliest ancestor
            earliest_ancestor = vertex
            # set the max path
            max_length_path = len(path)
        # get neighbors and iterate
        for neighbor in g.vertices[vertex]:
            # copy the path
            new_path = path
            # add vertex to the path
            new_path.append(neighbor)
            # add to the queue
            s.push(new_path)
    return earliest_ancestor

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 9))