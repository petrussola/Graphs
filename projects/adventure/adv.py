from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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

# test_line.txt map

# create Queue
q = Queue()
# create visited (will store room ids)
visited = []
# enqueue current room path to the queue
q.enqueue([player.current_room])
# print(player.current_room.id, "<<< current room <<<")
# while queue is not empty
while q.size() > 0:
    # dequeue path from queue
    path = q.dequeue()
    # get the last direction in the path
    room = path[-1]
    # print(room.name, "<<< room id <<<")
    # if room not in visited:
    if room.id not in visited:
        # add room_id to visited
        visited.append(room.id)
        # get exits from current room and iterate over them
        directions = player.current_room.get_exits()
        for d in directions:
            # travel in d direction (this will set the current room)
            player.travel(d)
            # add direction to the traversal_path list
            traversal_path.append(d)
            # create new path
            new_path = list(path)
            # add current room to the new path
            new_path.append(player.current_room)
            # add new path in queue
            q.enqueue(new_path)

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
