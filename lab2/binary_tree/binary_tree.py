from __future__ import annotations
from typing import Any, List, Tuple, Callable


class BinaryTree:

    class Node:

        def __init__(self, key: Any, value: Any):

            self.key = key
            self.value = value

            self.left = None
            self.right = None
            self.parent = None

        def set_left(self, new_left_node: BinaryTree.Node) -> BinaryTree.Node:
            old_node = self.left
            if self.left is not None:
                self.left.parent = None

            self.left = new_left_node

            if self.left is not None:
                self.left.parent = self

            return old_node

        def set_right(self, new_right_node: BinaryTree.Node) -> BinaryTree.Node:
            old_node = self.right
            if self.right is not None:
                self.right.parent = None

            self.right = new_right_node

            if self.right is not None:
                self.right.parent = self

            return old_node

        def is_right(self):
            if self.parent is None:
                return None

            return self is self.parent.right

    def __init__(self):

        self._root = None
        self._size = 0

    def __getitem__(self, key):

        found_node = self._find_node_by_key(key)
        return found_node.value if found_node is not None else None

    def __setitem__(self, key: Any, value: Any):
        found_node = self._add_or_find_node_by_key(key, new_only=False)
        found_node.value = value

    def __str__(self):

        final_string = ""

        for item in self._to_list_of_nodes():

            current_parent = item.parent
            identation = 0
            while current_parent is not None:
                identation += 1
                current_parent = current_parent.parent

            final_string += f"\n{'-' * identation} {'r' if item.is_right() else 'l'} [{hash(item.key)}] {item.key}"

        return final_string

    def insert(self, key: Any, value: Any):
        node = self._find_node_by_key(key)

        if node is None:
            raise ValueError(f'Entry with the key "{key}" was not found.')
        
        node.value = value
    
    def append(self, key: Any, value: Any):
        node = self._add_or_find_node_by_key(key, new_only=True)
        node.value = value

    def remove(self, key: Any) -> Any:

        found_node = self._find_node_by_key(key)

        if found_node is None:
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

    def to_graph(self) -> str:
        nodes = self._to_list_of_nodes()
        output = '\n'
        entries =  []

        for node in nodes:
            if node.parent is None:
                entries.append(f"{node.key}")
            else:
                entries.append(f"{node.parent.key},{node.key}")
        
        return output.join(entries)

    def _to_list_of_nodes(self) -> List[BinaryTree.Node]:
        result = []

        def save_children(node: BinaryTree.Node):
            if node.left is not None:
                result.append(node.left)
                save_children(node.left)
            if node.right is not None:
                result.append(node.right)
                save_children(node.right)

        if self._root is None:
            return result

        result.append(self._root)
        save_children(self._root)

        return result

    def _find_node_by_key(self, key: Any) -> BinaryTree.Node:

        current_node = self._root

        while current_node is not None and key != current_node.key:
            right_node = hash(key) > hash(current_node.key)
            current_node = current_node.right if right_node else current_node.left

        return current_node

    def _add_or_find_node_by_key(self, key: Any, new_only: bool) -> BinaryTree.Node:

        current_node = self._root
        node_parent = None
        right_node = False
        
        while current_node is not None and key != current_node.key:
            node_parent = current_node
            right_node = hash(key) > hash(current_node.key)
            current_node = current_node.right if right_node else current_node.left

        if current_node is not None:
            if new_only:
                raise ValueError(f'Entry with the key "{key}" already exists.')
        if current_node is None:
            current_node = BinaryTree.Node(key, None)

            if self._root is None:
                self._root = current_node
            elif right_node:
                node_parent.set_right(current_node)
            else:
                node_parent.set_left(current_node)
            
            self._size += 1

        return current_node

    def _new_node(self, key):
        new_node = BinaryTree.Node(key)
        new_node.left = new_node.right = new_node.parent = None

        return new_node

    def _replace_node(self, node_to_replace: Node) -> Node:

        replacement = node_to_replace

        if node_to_replace.right is not None:
            replacement = self._find_the_smallest_node_in_the_branch(node_to_replace.right)
        elif node_to_replace.left is not None:
            replacement = self._find_the_biggest_node_in_the_branch(node_to_replace.left)

        node_to_replace.key = replacement.key
        node_to_replace.value = replacement.value

        return replacement

    def _prune_leaf_node(self, node_to_prune: Node) -> None:
        
        if node_to_prune.parent is None:
            self._root = None
        else:
            replacement = node_to_prune.left if node_to_prune.left is not None else node_to_prune.right
            if node_to_prune.is_right():
                node_to_prune.parent.set_right(replacement)
            else:
                node_to_prune.parent.set_left(replacement)
        
        self._size -= 1

    def _remove_node(self, node_to_remove: Node) -> Node:
        prune_node =  self._replace_node(node_to_remove)
        self._prune_leaf_node(prune_node)

    @staticmethod
    def _find_the_smallest_node_in_the_branch(node: BinaryTree.Node) -> BinaryTree.Node:

        current_node = node
        while current_node.left is not None:
            current_node = current_node.left

        return current_node

    @staticmethod
    def _find_the_biggest_node_in_the_branch(node: BinaryTree.Node) -> BinaryTree.Node:

        current_node = node
        while current_node.right is not None:
            current_node = current_node.right

        return current_node
