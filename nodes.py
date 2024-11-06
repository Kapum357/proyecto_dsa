class GenreNode:
    def __init__(self, genre_name):
        self.genre_name = genre_name
        self.books = []
        self.subgenres = {}

    def add_book(self, book):
        self.books.append(book)

    def add_subgenre(self, subgenre_name):
        if subgenre_name not in self.subgenres:
            self.subgenres[subgenre_name] = GenreNode(subgenre_name)
        return self.subgenres[subgenre_name]

class YearNode:
    def __init__(self, year):
        self.year = year
        self.books = []
        self.left = None
        self.right = None
        self.height = 1  # Height of the node for balancing the tree

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)

    def right_rotate(self):
        y = self.left
        T2 = y.right

        # Perform rotation
        y.right = self
        self.left = T2

        # Update heights
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        y.height = 1 + max(y.get_height(y.left), y.get_height(y.right))

        # Return new root
        return y

    def left_rotate(self):
        y = self.right
        T2 = y.left

        # Perform rotation
        y.left = self
        self.right = T2

        # Update heights
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        y.height = 1 + max(y.get_height(y.left), y.get_height(y.right))

        # Return new root
        return y

    def balance(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))
        balance_factor = self.get_balance()

        # Left Heavy
        if balance_factor > 1:
            if self.left.get_balance() < 0:
                self.left = self.left.left_rotate()
            return self.right_rotate()

        # Right Heavy
        if balance_factor < -1:
            if self.right.get_balance() > 0:
                self.right = self.right.right_rotate()
            return self.left_rotate()

        return self

    def insert(self, book):
        if book.year < self.year:
            if self.left is None:
                self.left = YearNode(book.year)
                self.left.books.append(book)
            else:
                self.left = self.left.insert(book)
        elif book.year > self.year:
            if self.right is None:
                self.right = YearNode(book.year)
                self.right.books.append(book)
            else:
                self.right = self.right.insert(book)
        else:
            self.books.append(book)
        return self.balance()

class RedBlackNode:
    def __init__(self, book):
        self.book = book
        self.color = 'red'  # Los nuevos nodos se insertan como rojos
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RedBlackNode(None)
        self.NIL.color = 'black'
        self.root = self.NIL

    def insert(self, book):
        new_node = RedBlackNode(book)
        new_node.left = self.NIL
        new_node.right = self.NIL
        self._insert_node(new_node)
        self._fix_insert(new_node)

    def _insert_node(self, node):
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if node.book.title < current.book.title:
                current = current.left
            else:
                current = current.right
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.book.title < parent.book.title:
            parent.left = node
        else:
            parent.right = node
        node.color = 'red'

    def _fix_insert(self, node):
        while node != self.root and node.parent.color == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._rotate_left(node.parent.parent)
        self.root.color = 'black'

    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NIL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NIL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def search(self, title):
        current = self.root
        while current != self.NIL and title != current.book.title:
            if title < current.book.title:
                current = current.left
            else:
                current = current.right
        return current.book if current != self.NIL else None

class AVLNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, book):
        if not root:
            return AVLNode(book)
        elif book.year < root.book.year:
            root.left = self.insert(root.left, book)
        else:
            root.right = self.insert(root.right, book)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and book.year < root.left.book.year:
            return self.right_rotate(root)

        if balance < -1 and book.year > root.right.book.year:
            return self.left_rotate(root)

        if balance > 1 and book.year > root.left.book.year:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and book.year < root.right.book.year:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def search(self, root, year):
        if not root or root.book.year == year:
            return root
        elif year < root.book.year:
            return self.search(root.left, year)
        else:
            return self.search(root.right, year)

class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, book):
        if key not in self.table:
            self.table[key] = []
        self.table[key].append(book)

    def search(self, key):
        return self.table.get(key, [])

class TrieNode:
    def __init__(self):
        self.children = {}
        self.books = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, book):
        node = self.root
        for char in word:
            if (char not in node.children):
                node.children[char] = TrieNode()
            node = node.children[char]
        node.books.append(book)

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.books

def binary_search(arr, key, value):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if key(arr[mid]) < value:
            low = mid + 1
        elif key(arr[mid]) > value:
            high = mid - 1
        else:
            return mid
    return -1