

import csv
from typing import Dict, List

def get_min_depth(root, nodes, connections):
    
    
    marked = {}
    marked[root] = False
    for node in nodes:
        marked[node] = False

    queue = [root]
    shortest_path_node = None
    while len(queue) > 0:
        current_node = queue.pop(0)
        
        if not marked[current_node]:
            marked[current_node] = True

            neighbours = []
            for connection in connections:
                if connection[0] == current_node:
                    neighbours.append(connection[1])

            if len(neighbours) == 0:
                shortest_path_node = current_node
                break

            for neighbour in neighbours:
                if not marked[neighbour]:
                    queue.append(neighbour)
    
    depth = 1
    current_node = shortest_path_node
    
    found_parent = True
    while found_parent:
        found_parent = False
        for connection in connections:
            if connection[1] == current_node:
                current_node = connection[0]
                depth+=1
                found_parent = True
                break
    
    return depth




if __name__ == "__main__":
    connections = []
    with open("input.txt", "r") as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')
        for csv_row in csv_reader:
            csv_row[0] = int(csv_row[0])

            if len(csv_row) > 1:
                csv_row[1] = int(csv_row[1])
            
            connections.append(csv_row)
    
    nodes = []
    root = connections[0][0]
    del connections[0]

    for connection in connections:
        nodes.append(connection[-1])

    shortest_root_null_path = get_min_depth(root, nodes, connections)
    print(f"Shortest path is: {shortest_root_null_path}")

    with open("output.txt", "w+") as input_file:
        input_file.write(str(shortest_root_null_path))