from __future__ import annotations
from operator import irshift
from typing import Any, List, Tuple, Callable


RED = True
BLACK =  False
NULL = None

class RedBlackTree:

    class Node:

        def __init__(self, key: Any):

            self.key = key
            self.value = None

            self.left = None
            self.right = None
            self.parent = None

            self.color = RED

        def set_left(self, new_left_node: RedBlackTree.Node) -> RedBlackTree.Node:
            old_node = self.left
            if self.left is not NULL:
                self.left.parent = NULL

            self.left = new_left_node

            if self.left is not NULL:
                self.left.parent = self

            return old_node

        def set_right(self, new_right_node: RedBlackTree.Node) -> RedBlackTree.Node:
            old_node = self.right
            if self.right is not NULL:
                self.right.parent = NULL

            self.right = new_right_node

            if self.right is not NULL:
                self.right.parent = self

            return old_node

        def is_right(self):
            if self.parent is NULL:
                return None

            return self is self.parent.right

        def black_height(self):
            node = self
            height = 0
            while node is not NULL:
                if node.color is BLACK:
                    height += 1
                node = node.parent
            
            return height

    def __init__(self):

        global NULL

        if NULL is None:
            NULL = RedBlackTree.Node(None)
            NULL.color = BLACK

        self.root = NULL
        self._size = 0

    def __getitem__(self, key):

        found_node = self._find_node_by_key(key)
        return found_node.value if found_node is not NULL else None

    def __setitem__(self, key: Any, value: Any):
        found_node = self._add_or_find_node_by_key(key, new_only=False)
        found_node.value = value

    def __str__(self):

        final_string = ""

        for item in self._to_list_of_nodes():

            current_parent = item.parent
            identation = 0
            while current_parent is not NULL:
                identation += 1
                current_parent = current_parent.parent

            final_string += f"\n{'-' * identation} {'r' if item.color else 'b'} {'r' if item.is_right() else 'l'} [{hash(item.key)}] {item.key}"

        return final_string

    def insert(self, key: Any, value: Any):
        node = self._find_node_by_key(key)

        if node is NULL:
            raise ValueError(f'Entry with the key "{key}" was not found.')
        
        node.value = value
    
    def append(self, key: Any, value: Any):
        node = self._add_or_find_node_by_key(key, new_only=True)
        node.value = value

    def remove(self, key: Any) -> Any:

        found_node = self._find_node_by_key(key)

        if found_node is NULL:
            return None

        value = found_node.value
        self._remove_node(found_node)
        return value

    def remove_by(self, predicate: Callable[[Any, Any], bool]) -> List[(Any, Any)]:

        list_to_remove = self.get_by(predicate)

        for key, item in list_to_remove:
            self.remove(key)

        return list_to_remove

    def get_by(self, predicate: Callable[[Any, Any], bool]) -> List[(Any, Any)]:
        return [(x.key, x.value) for x in self._to_list_of_nodes() if predicate(x.key, x.value)]

    def top_to_bottom_list(self) -> List[(Any, Any)]:
        return [(x.key, x.value) for x in self._to_list_of_nodes()]

    def size(self) -> int:
        return self._size

    def _to_list_of_nodes(self) -> List[RedBlackTree.Node]:
        result = []

        def save_children(node: RedBlackTree.Node):
            if node.left is not NULL:
                result.append(node.left)
                save_children(node.left)
            if node.right is not NULL:
                result.append(node.right)
                save_children(node.right)

        if self.root is NULL:
            return result

        result.append(self.root)
        save_children(self.root)

        return result

    def _find_node_by_key(self, key: Any) -> RedBlackTree.Node:

        current_node = self.root

        while current_node is not NULL and key != current_node.key:
            right_node = hash(key) > hash(current_node.key)
            current_node = current_node.right if right_node else current_node.left

        return current_node

    def _add_or_find_node_by_key(self, key: Any, new_only: bool) -> RedBlackTree.Node:

        current_node = self.root
        node_parent = NULL
        right_node = False
        
        while current_node is not NULL and key != current_node.key:
            node_parent = current_node
            right_node = hash(key) > hash(current_node.key)
            current_node = current_node.right if right_node else current_node.left

        if current_node is not NULL:
            if new_only:
                raise ValueError(f'Entry with the key "{key}" already exists.')
        if current_node is NULL:
            current_node = self._new_node(key)

            if self.root is NULL:
                self.root = current_node
            elif right_node:
                node_parent.set_right(current_node)
            else:
                node_parent.set_left(current_node)
            
            self._size += 1
            self._insert_fixup(current_node)

        return current_node

    def _new_node(self, key):
        new_node = RedBlackTree.Node(key)
        new_node.left = NULL
        new_node.right = NULL
        new_node.parent = NULL

        return new_node

    def _replace_node(self, node_to_replace: RedBlackTree.Node) -> RedBlackTree.Node:

        replacement = node_to_replace

        if node_to_replace.right is not NULL:
            replacement = self._find_the_smallest_node_in_the_branch(node_to_replace.right)
        elif node_to_replace.left is not NULL:
            replacement = self._find_the_biggest_node_in_the_branch(node_to_replace.left)

        node_to_replace.key = replacement.key
        node_to_replace.value = replacement.value

        return replacement

    def _prune_leaf_node(self, node_to_prune: RedBlackTree.Node) -> RedBlackTree.Node:

        replacement = None
        
        if node_to_prune.parent is NULL:
            self._root = NULL
        else:
            replacement = node_to_prune.left if node_to_prune.left is not NULL else node_to_prune.right
            if node_to_prune.is_right():
                node_to_prune.parent.set_right(replacement)
            else:
                node_to_prune.parent.set_left(replacement)
        
        self._size -= 1

        return replacement

    def _remove_node(self, node_to_remove: RedBlackTree.Node) -> RedBlackTree.Node:
        prune_node =  self._replace_node(node_to_remove)

        original_color =  prune_node.color
        fixup_node = self._prune_leaf_node(prune_node)

        if original_color is BLACK:
            self._remove_fixup(fixup_node)

    def get_max_depth(self):
        depth = 0
        for node in self._to_list_of_nodes():
            current_depth = 1
            while node.parent is not NULL:
                node =  node.parent
                current_depth += 1
            
            if current_depth > depth:
                depth =  current_depth

        return depth

    def _insert_fixup(self, node): 

        if node.parent is NULL:
            node.color = BLACK
            return

        if node.parent.parent is NULL:
            return

        while node is not self.root and node.parent.color is RED:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color is RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right

                if uncle.color is RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)

        self.root.color = BLACK

    def _remove_fixup(self, node):
        while node is not self.root and node.color is BLACK:
            if node is node.parent.left:
                sibling = node.parent.right
                if sibling.color is RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if sibling.left.color is BLACK and sibling.right.color is BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.right.color is BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right

                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color is RED:
                    sibling.color = BLACK
                    node.parent.color = RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if sibling.right.color is BLACK and sibling.left.color is BLACK:
                    sibling.color = RED
                    node = node.parent
                else:
                    if sibling.left.color is BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._right_rotate(node.parent)
                    node = self.root
        node.color = BLACK

    def _left_rotate(self, node):
        new_parent = node.right
        node.right = new_parent.left
        if new_parent.left != NULL:
            new_parent.left.parent = node

        new_parent.parent = node.parent
        if node.parent == NULL:
            self.root = new_parent
        elif node == node.parent.left:
            node.parent.left = new_parent
        else:
            node.parent.right = new_parent
        new_parent.left = node
        node.parent = new_parent

    def _right_rotate(self, node):
        left_node = node.left
        node.left = left_node.right
        if left_node.right != NULL:
            left_node.right.parent = node

        left_node.parent = node.parent
        if node.parent == NULL:
            self.root = left_node
        elif node == node.parent.right:
            node.parent.right = left_node
        else:
            node.parent.left = left_node
        left_node.right = node
        node.parent = left_node            
    


    def _find_the_smallest_node_in_the_branch(self, node: RedBlackTree.Node) -> RedBlackTree.Node:

        current_node = node
        while current_node.left is not NULL:
            current_node = current_node.left

        return current_node

    def _find_the_biggest_node_in_the_branch(self, node: RedBlackTree.Node) -> RedBlackTree.Node:

        current_node = node
        while current_node.right is not NULL:
            current_node = current_node.right

        return current_node
