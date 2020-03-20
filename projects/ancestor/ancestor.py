from util import Queue, Stack


def get_neighbors(ancestors, node):
    # create empty list to hold neighbors
    neighbors = list()
    # loop over ancestors:
    for el in ancestors:
        # if first item of tuple matches our node
        if el[1] == node:
            # add second item to the neighbors list
            neighbors.append(el[0])
    # return neighbor list
    return neighbors


def earliest_ancestor(ancestors, starting_node):
    # create a stack
    s = Stack()
    # create visited
    visited = set()
    # create a path list
    all_paths = list()
    # add starting node to the queue
    s.push([starting_node])
    # while queue is not empty
    while s.size() > 0:
        # pop the path
        path = s.pop()
        # take the last vert
        vertex = path[-1]
        # if the vert is not in visited
        if vertex not in visited:
            # add vert to the visited set
            visited.add(vertex)
            # loop over neighbors
            for neighbor in get_neighbors(ancestors, vertex):
                # set a new path equal to the copy of the current path
                new_path = list(path)
                # append next vert in the new path
                new_path.append(neighbor)
                # append the path to the list with all paths
                all_paths.append(new_path)
                # push the path to the stack
                s.push(new_path)

    # list containing the length of the path and the last item. we start it as [0,0] - [len, last item]
    verdict = [0, 0]  # [len(path), last item]
    # loop over all paths
    for path in all_paths:
        # if len of path i is longer that initial list, we set it as the new longest path and we store the last vertex
        if len(path) > verdict[0]:
            verdict = [len(path), path[-1]]

    # we return the last vertex
    if verdict[1] == 0:
        return -1
    else:
        return verdict[1]
