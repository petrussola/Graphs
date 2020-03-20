from room import Room
from player import Player
from world import World
from util import Stack
from graph import Graph

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
# print(room_graph, "<<<<<<<")
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def get_random_direction(available_directions, current_room, mess, length, graph):
    if len(available_directions) > 0:
        numb = random.randrange(0, len(available_directions))
    # print(mess, "<<<< type of call")
    # print(current_room, "<<<< current room <<<")
    # print(available_directions, "<<< available directions")
    # print(available_directions[numb], "<<< next direction")
    # print(length, "<<< len(graph.vertices)")
    # print(graph, "<<< len(room_graph)")
    # print("---------------------------------------")
        return available_directions[numb]
    else:
        dir = []
        directions = current_room.get_exits()
        for d in directions:
            dir.append(dir)
        numb = random.randrange(0, len(dir))
        return dir[numb]


graph = Graph()
used_directions = {}

options = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}
s = Stack()  # [(direction, prev room), current_room]
s.push([[[None, None], player.current_room]])
while s.size() > 0:
    if len(graph.vertices) != len(room_graph):
        path = s.pop()
        room = path[-1][1]
        incoming_direction = path[-1][0][0]
        prev_room = path[-1][0][1]
        # print(path[-1][0][0], "<<<<< rooom")
        directions = room.get_exits()
        if room.id not in graph.vertices:
            graph.add_vertex(room.id)
            for d in directions:
                graph.vertices[room.id][d] = "?"
        if incoming_direction != None:
            opposite_direction = options[incoming_direction]
            graph.vertices[room.id][opposite_direction] = prev_room.id
            graph.vertices[prev_room.id][incoming_direction] = room.id

        unexplored_dir = []
        explored_dir = []
        # print(used_directions, "<<<<<<<< used directions")
        # print(room.id, "<<<<<<<< used directions")
        for d in graph.vertices[room.id]:
            # print(d, "<<<< directions")
            if graph.vertices[room.id][d] == "?":
                unexplored_dir.append(d)
            if room.id not in used_directions or d not in used_directions[room.id]:
                explored_dir.append(d)
            # else:
            #     explored_dir.append(d)
        # print(unexplored_dir, "<<<< unexplored dir")
        # print(explored_dir, "<<<< explored dir")
        if len(unexplored_dir) > 0:
            next_dir = get_random_direction(
                unexplored_dir, room, "unexplored", len(graph.vertices), len(room_graph))
            if room.id not in used_directions:
                used_directions[room.id] = set()
            used_directions[room.id].add(next_dir)
            # else:
            #     used_directions[room.id].add(next_dir)
            player.travel(next_dir)
            traversal_path.append(next_dir)
            new_path = list(path)
            new_path.append([[next_dir, room], player.current_room])
            s.push(new_path)
        # otherwise go back
        else:
            next_dir = get_random_direction(
                explored_dir, room, "backing up", len(graph.vertices), len(room_graph))
            if room.id not in used_directions:
                used_directions[room.id] = set()
            used_directions[room.id].add(next_dir)
            player.travel(next_dir)
            traversal_path.append(next_dir)
            new_path = list(path)
            new_path.append([[next_dir, room], player.current_room])
            s.push(new_path)
    else:
        while s.size() > 0:
            s.pop()


# print(graph.vertices, "<<<< vertices <<<<")
# print(traversal_path, "<<< path <<<")

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
