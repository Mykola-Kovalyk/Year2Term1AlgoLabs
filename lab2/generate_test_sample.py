from random import shuffle
from binary_tree.binary_tree import BinaryTree

if __name__ ==  '__main__':
    sample_bin = BinaryTree()

    samples = [x for x in range(25)]
    shuffle(samples)

    for sample in samples:
        sample_bin[sample] = None

    output = sample_bin.to_graph()

    with open("input.txt", "w+") as f:
        f.write(output)
    