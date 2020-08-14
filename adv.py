from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from graph import Graph

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
#  a faster solution might be:
# for each node in the queue 
# first find the paths that lead to dead ends first
# create a dictionary of rooms and all the rooms that room is connected to
rooms = {}
for r in world.rooms:
    room = world.rooms[r]
    # print(room.name)
    rooms[room.name] = []
    for p in room.get_exits():
        # print(room.get_room_in_direction(p).name)
        rooms[room.name] += [[room.get_room_in_direction(p).name, p]]
# a list of all the connections    
connections = []
for r in rooms:
    for n in rooms[r]:
        connections.append([r, n[0], n[1]])
        
# print(connections)
directions = {}
# for c in connections:
#     directions[c[2]] = [c[0], c[1]]
print(directions)
# print(rooms)
# print(edges)
# create a graph to get breadth first search to find the shortest path from a to b
rg = Graph()
for r in rooms:
    rg.add_vertex(r)
for c in connections:
    rg.add_edge(c[0], c[1])
# print(rg.vertices)

def find_components(graph):
    # traverse the graph
    # when you get to a dead end
    # create a path from the last node with open paths to the dead end
    pass


# what is the starting room?
start_room = world.starting_room
opposites = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}
        

def get_path(starting_room):
    visited = []
    total = len(world.rooms)
    
    cur_room = starting_room
    open_paths = {}
    queue = []
    shortest_path = []
    # queue.remove(cur_room.name)
    while len(visited) != total:
        
        dirs = cur_room.get_exits()
        open_dirs = []       
        # print(open_dirs)
        if cur_room.name not in visited:
            visited.append(cur_room.name)
        # check for every unvisited path
        for d in dirs:
            # print(cur_room.get_room_in_direction(d).name)
            rname = cur_room.get_room_in_direction(d).name
            if rname not in visited:
                open_dirs.append(d)
        # if len(shortest_path) > 0:
        #     if cur_room.name == shortest_path[-1]:
        #         shortest_path = []
        #         for d in open_dirs:
        #             rname = cur_room.get_room_in_direction(d).name
        #             if rname in queue:
        #                 open_dirs.remove(d)
        if len(open_dirs) > 0 and cur_room.name not in queue:
            queue.append(cur_room.name)
        for d in open_dirs:
            rname = cur_room.get_room_in_direction(d).name
            if rname in queue:
                open_dirs.remove(d)
        if len(open_dirs) == 0 and cur_room.name in queue:
            for q in queue:
                if cur_room.name == q:
                    queue.remove(q)
        if len(open_dirs) > 0:
            ran_dir = random.randint(1, len(open_dirs)) - 1
            # move in that direction
            player.travel(open_dirs[ran_dir])
            # add that to the traversal path
            traversal_path.append(open_dirs[ran_dir])
            cur_room = player.current_room
            open_paths[cur_room.name] = open_dirs
        if len(open_dirs) == 0:
            if len(queue) > 0:
                shortest_path = rg.bfs(cur_room.name, queue[-1])
            # create a list of all the connected shortest paths
            spaths = []
            count = 0
            for index, p in enumerate(shortest_path):
                if count < len(shortest_path) - 1:
                    # print([shortest_path[count], shortest_path[count + 1]])
                    spaths.append([shortest_path[count], shortest_path[count + 1]])
                    count += 1
            # print(spaths)
            # break
            spath_dirs = []
            for sp in spaths:
                for c in connections:
                    if c[0] == sp[0] and c[1] == sp[1]:
                        spath_dirs.append(c[2])
            # print(spath_dirs)
            for d in spath_dirs:
                player.travel(d)
                traversal_path.append(d)
                # temp_room = player.current_room
                # temp_dirs = temp_room.get_exits()
                # for t in temp_dirs:
                #     rname = temp_room.get_room_in_direction(t).name
                #     if rname not in visited and rname not in queue:
                #         queue.append(rname)
        
            cur_room = player.current_room
            

get_path(start_room)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
