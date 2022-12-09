
class WhatTheHeckException(Exception):
    pass


POS_X = 0
POS_Y = 1
LETTER = 2

def get_data(input_file):
    in_file = open(input_file, 'r')
    dimensions = [int(x) for x in in_file.readline().split(' ')]
    width = dimensions[0]
    height = dimensions[1]

    letter_matrix = []

    while line := in_file.readline():
        line_list = [ x for x in list(line) if x != '\n']
        
        if len(line_list) != width:
            raise WhatTheHeckException(f"What the heck are you putting in? Open your eyes and check how many letters in row '{line}'")
        
        letter_matrix.append(line_list)

    return width, height, letter_matrix
        

def convert(data, width, height):


    converted  = []
    for line_number, line in enumerate(data):
        for letter_number, letter in enumerate(line):
            converted.append([letter_number,line_number,letter])

    connections = []
    for letter in converted:

        for potential_neighbour in converted:
            if potential_neighbour[POS_X] > letter[POS_X]:
                if (potential_neighbour[POS_X] == (letter[POS_X] + 1) and potential_neighbour[POS_Y] == letter[POS_Y]) or potential_neighbour[LETTER] == letter[LETTER]:
                    connections.append([letter, potential_neighbour])

    return connections


def dfs(root, connections, target_nodes):

    paths = []

    nodes = []
    for connection in connections:
        for node in connection:
            if node in nodes:
                continue 
            nodes.append(node)

    leads_to_exit = {}
    for node in nodes:
        leads_to_exit[node] = False

    for target in target_nodes:
        leads_to_exit[target] = True

    stack = [[None, root]]
    current_path = []
    while len(stack) > 0:
        parent_node, current_node = stack.pop()
        
        if parent_node is not None:
            current_path = current_path[:current_path.index(parent_node)+1]
        current_path.append(current_node)

        neighbours = []
        for connection in connections:
            if current_node != connection[0]:
                continue
            neighbours.append(connection[1])

        for neighbour in neighbours:
            stack.append([current_node, neighbour])
            
            if leads_to_exit[neighbour]:
                paths.append(list(current_path) + [neighbour])
    
    return paths



if __name__ ==  '__main__':
    width, height, data = get_data('ijohnes.in')
    converted = convert(data, width, height)

    target_nodes = [f"{width - 1}_{0}_{data[0][width - 1]}", f"{width - 1}_{height - 1}_{data[height - 1][width - 1]}"]
    converted = [[f"{x[0][POS_X]}_{x[0][POS_Y]}_{x[0][LETTER]}", f"{x[1][POS_X]}_{x[1][POS_Y]}_{x[1][LETTER]}"] for x in converted]

    result = dfs(f"0_0_{data[0][0]}", converted, target_nodes)
    print(f"found: {len(result)} paths")
    for path in result:
        print(path)

    nodes = []
    for connection in data:
        for node in connection:
            if node in nodes:
                continue 
            nodes.append(node)