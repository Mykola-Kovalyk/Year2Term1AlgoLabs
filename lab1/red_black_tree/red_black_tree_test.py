import logging
import sys
import traceback
import unittest
import random
from red_black_tree import NULL, RED, RedBlackTree
from math import log2


class Film:

    def __init__(self, name, year, duration_in_minutes, genre, studio):
        self.name = name
        self.year = year
        self.duration_in_minutes = duration_in_minutes
        self.genre = genre
        self.studio = studio


    def __str__(self):
        return  f'---------- film ---------- \n'\
                f'name: {self.name} \n' \
                f'year: {self.year} \n ' \
                f'genre: {self.genre} \n' \
                f'studio: {self.studio} \n' \
                f'duration: {self.duration_in_minutes}'

class MyTestCase(unittest.TestCase):

    def test_binary_tree(self):

        log = logging.getLogger( "SomeTest.testSomething" )

        def check_red_black_tree_properties(tree: RedBlackTree):
            nodes = tree._to_list_of_nodes()
            black_height = 0
            for node in nodes:
                if node.color is RED:
                    self.assertFalse(node.parent.color is RED or node.left.color is RED or node.right.color is RED, tree)
                
                if node.left is NULL and node.right is NULL:
                    if black_height == 0:
                        black_height = node.black_height()
                    else:
                        self.assertEqual(node.black_height(), black_height)


        def run_test():
        
            names = [
                'Top gun',
                'Avatar',
                'Illovaysk',
                'Inception',
                'Pacific rim',
                'Transformers',
                'Interstellar',
                'Oblivion',
                'Dune',
                'Zahar Berkut',
                'World War Z',
                'Fury',
                'Harry Potter and the Sorcerer\'s Stone',
                'The Angry Birds Movie',
                'Valkyrie',
                'American Made',
                'Joker',
                'Deadpool'
            ]

            random.shuffle(names)

            test_list = []
            for i in range(len(names)):
                test_list.append(Film(
                    names[i],
                    random.randint(2000, 2022),
                    random.randint(120, 180),
                    'action',
                    'Hollywood'
                ))

            bin_tree = RedBlackTree()
            
            self.assertEqual(bin_tree.size(), 0)

            for film in test_list:
                bin_tree.append(film.name, film)

            self.assertEqual(bin_tree.size(), len(test_list))

            check_red_black_tree_properties(bin_tree)

            if 1:
                test_subject_1 = test_list[random.randint(0, len(test_list) - 1)]
                test_list.remove(test_subject_1)
                bin_tree.remove(test_subject_1.name)
                self.assertEqual(bin_tree.size(), len(test_list))

                test_subject_2 = test_list[random.randint(0, len(test_list) - 1)]
                test_list.remove(test_subject_2)
                bin_tree.remove(test_subject_2.name)
                self.assertEqual(bin_tree.size(), len(test_list))

                bin_tree.append(test_subject_1.name, test_subject_1)
                bin_tree.append(test_subject_2.name, test_subject_2)

                self.assertEqual(bin_tree[test_subject_1.name], test_subject_1)
                self.assertEqual(bin_tree[test_subject_2.name], test_subject_2)

                bin_tree.insert(test_subject_1.name, test_subject_2)
                bin_tree[test_subject_2.name] = test_subject_1

                self.assertEqual(bin_tree[test_subject_1.name], test_subject_2)
                self.assertEqual(bin_tree[test_subject_2.name], test_subject_1)

                removed = [y for (x, y) in bin_tree.remove_by(
                    lambda key, value: key is test_subject_1.name or key is test_subject_2.name)]
                self.assertIn(test_subject_1, removed)
                self.assertIn(test_subject_2, removed)

                self.assertEqual(bin_tree[test_subject_1.name], None)
                for film in test_list:
                    self.assertEqual(bin_tree[film.name], film)

                self.assertEqual(bin_tree[test_subject_2.name], None)
                for film in test_list:
                    self.assertEqual(bin_tree[film.name], film)

                remove_test_list = list(test_list)
                while len(remove_test_list) > 0:
                    i = len(remove_test_list) - 1
                    to_remove = remove_test_list[i]
                    remove_test_list.remove(to_remove)
                    bin_tree.remove(to_remove.name)

                    for film in remove_test_list:
                        self.assertEqual(bin_tree[film.name], film)

                self.assertEqual(bin_tree.size(), 0, bin_tree)
                try:
                    for film in test_list:
                        bin_tree.append(film.name, film)
                except Exception as e:
                    self.assertFalse(True, f"{e}, {bin_tree.size()} {bin_tree}")

            self.assertLessEqual(bin_tree.get_max_depth(),  int(2 * log2(bin_tree.size())))

        for i in range(1000):
            run_test()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger( "SomeTest.testSomething" ).setLevel(logging.DEBUG)
    unittest.main()
