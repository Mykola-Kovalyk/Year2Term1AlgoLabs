

import csv
from typing import Dict, List

def bfs(root, connections):
    found_nodes = []

    nodes = []
    for connection in connections:
        for node in connection:
            if node in nodes:
                continue 
            nodes.append(node)
    
    marked = {}
    for node in nodes:
        marked[node] = False

    queue = [root]
    while len(queue) > 0:
        current_node = queue.pop(0)
        found_nodes.append(current_node)

        if not marked[current_node]:
            marked[current_node] = True

            neighbours = []
            for connection in connections:
                if not current_node in connection:
                    continue
                for node in connection:
                    if node != current_node:
                        neighbours.append(node)

            for neighbour in neighbours:
                if not marked[neighbour]:
                    queue.append(neighbour)
    
    return found_nodes


def get_pairs_of_people(tribes):
    pairs_of_people = []

    for tribe in tribes:
        men = [member for member in tribe if member % 2 == 1]
        women = [member for member in tribe if member % 2 == 0]
        
        for another_tribe in tribes:
            if another_tribe == tribe:
                continue

            another_men = [member for member in another_tribe if member % 2 == 1]
            another_women = [member for member in another_tribe if member % 2 == 0]

            for man in men:
                for woman in another_women:
                    potential_pair = [man, woman]
                    if not potential_pair in pairs_of_people:
                        pairs_of_people.append(potential_pair)

            for woman in women:
                for man in another_men:
                    potential_pair = [man, woman]
                    if not potential_pair in pairs_of_people:
                        pairs_of_people.append(potential_pair)

    return pairs_of_people



if __name__ == "__main__":
    connections = []
    count_of_pairs = int(input("Enter number of pairs: "))
    print("Enter the pairs: ")
    for i in range(count_of_pairs):
        person, another = input(" > ").split()
        connections.append([int(person), int(another)])


    root = connections[0][0]

    nodes = []
    for connection in connections:
        for node in connection:
            if node in nodes:
                continue 
            nodes.append(node)

    tribes = [] 
    while len(nodes) > 0:
        tribe = bfs(nodes[0], connections)
        for node in tribe:
            nodes.remove(node)
        tribes.append(tribe)
    
    pairs = get_pairs_of_people(tribes)

    print(f"Tribes: {tribes}")
    print(f"Count of people: {len(pairs)}")
    print(f"Pairs: {pairs}")