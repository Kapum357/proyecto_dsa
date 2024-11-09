import logging
from book import Book

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Árbol binario de búsqueda por título
class TitleBSTNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class TitleBST:
    def __init__(self):
        self.root = None

    def insert(self, book):
        logger.info(f"Insertando libro '{book.title}' en el árbol por título")
        if self.root is None:
            self.root = TitleBSTNode(book)
        else:
            self._insert(self.root, book)

    def _insert(self, node, book):
        if book.title < node.book.title:
            if node.left is None:
                node.left = TitleBSTNode(book)
            else:
                self._insert(node.left, book)
        else:
            if node.right is None:
                node.right = TitleBSTNode(book)
            else:
                self._insert(node.right, book)

    def search(self, title):
        logger.info(f"Buscando libro '{title}' en el árbol por título")
        return self._search(self.root, title)

    def _search(self, node, title):
        if node is None:
            return None
        if node.book.title == title:
            return node.book
        elif title < node.book.title:
            return self._search(node.left, title)
        else:
            return self._search(node.right, title)

# Red-Black Tree implementation for storing books by title
class RBTreeNode:
    def __init__(self, book):
        self.book = book
        self.title = book.title
        self.color = 'red'  # New nodes are initially red
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.NIL = RBTreeNode(Book('', '', '', '', '', ''))  # Sentinel node
        self.NIL.color = 'black'
        self.root = self.NIL

    def insert(self, book):
        logger.info(f"Inserting book '{book.title}' into Red-Black Tree")
        node = RBTreeNode(book)
        node.left = self.NIL
        node.right = self.NIL
        node.parent = None

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if node.title < current.title:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.title < parent.title:
            parent.left = node
        else:
            parent.right = node

        node.color = 'red'
        self._insert_fixup(node)

    def _insert_fixup(self, node):
        while node.parent and node.parent.color == 'red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self._left_rotate(node.parent.parent)
        self.root.color = 'black'

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        logger.debug(f"Performed left rotation on '{x.title}'")

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x
        logger.debug(f"Performed right rotation on '{y.title}'")

    def search(self, title):
        logger.info(f"Searching for book '{title}' in Red-Black Tree")
        return self._search(self.root, title)

    def _search(self, node, title):
        if node == self.NIL or node is None:
            return None
        if title == node.title:
            return node.book
        elif title < node.title:
            return self._search(node.left, title)
        else:
            return self._search(node.right, title)

# Implementación del Trie para búsqueda por prefijo
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.books = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, book):
        node = self.root
        for char in key.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.books.append(book)
        logger.info(f"Insertado '{key}' en el Trie.")

    def search(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                logger.info(f"No se encontraron libros con el prefijo '{prefix}'.")
                return []
            node = node.children[char]
        return self._collect_books(node)

    def _collect_books(self, node):
        books = []
        if node.is_end_of_word:
            books.extend(node.books)
        for child in node.children.values():
            books.extend(self._collect_books(child))
        return books

# Implementación de la Tabla Hash para almacenar libros
class HashTableNode:
    def __init__(self, key, book):
        self.key = key
        self.book = book
        self.next = None

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * self.size
        logger.info("Inicializada la Tabla Hash.")

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, book):
        key = book.title
        index = self._hash(key)
        logger.info(f"Insertando libro '{key}' en la Tabla Hash en el índice {index}.")
        new_node = HashTableNode(key, book)
        if self.table[index] is None:
            self.table[index] = new_node
            logger.debug(f"Libro '{key}' insertado en una posición vacía.")
        else:
            current = self.table[index]
            while current.next:
                if current.key == key:
                    logger.warning(f"Libro '{key}' ya existe en la Tabla Hash. Inserción omitida.")
                    return
                current = current.next
            if current.key == key:
                logger.warning(f"Libro '{key}' ya existe en la Tabla Hash. Inserción omitida.")
            else:
                current.next = new_node
                logger.debug(f"Libro '{key}' enlazado al final de la cadena en el índice {index}.")

    def search(self, key):
        index = self._hash(key)
        logger.info(f"Buscando libro '{key}' en la Tabla Hash en el índice {index}.")
        current = self.table[index]
        while current:
            if current.key == key:
                logger.info(f"Libro '{key}' encontrado en la Tabla Hash.")
                return current.book
            current = current.next
        logger.info(f"Libro '{key}' no encontrado en la Tabla Hash.")
        return None

    def delete(self, key):
        index = self._hash(key)
        logger.info(f"Eliminando libro '{key}' de la Tabla Hash en el índice {index}.")
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                logger.info(f"Libro '{key}' eliminado de la Tabla Hash.")
                return True
            prev = current
            current = current.next
        logger.warning(f"Libro '{key}' no encontrado en la Tabla Hash. Eliminación fallida.")
        return False

# Implementación del Árbol N-ario para almacenar libros por género
class NaryTreeNode:
    def __init__(self, genre):
        self.genre = genre
        self.children = {}
        self.books = []

class NaryTree:
    def __init__(self):
        self.root = NaryTreeNode("Sin Género")
        logger.info("Inicializado el Árbol N-ario para géneros.")

    def insert(self, book):
        genres = book.genre.lower().split('/')
        current = self.root
        for genre in genres:
            if genre not in current.children:
                current.children[genre] = NaryTreeNode(genre)
                logger.info(f"Género '{genre}' añadido al Árbol N-ario.")
            current = current.children[genre]
        current.books.append(book)
        logger.info(f"Libro '{book.title}' insertado bajo el género '{current.genre}'.")

    def search(self, genre):
        genres = genre.lower().split('/')
        current = self.root
        for g in genres:
            if g in current.children:
                current = current.children[g]
            else:
                logger.info(f"Género '{genre}' no encontrado en el Árbol N-ario.")
                return []
        logger.info(f"Buscando libros bajo el género '{genre}'.")
        return current.books

# Implementación de B+ Tree para almacenar libros por año de publicación
class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(leaf=True)
        self.order = order
        logger.info("Inicializado el B+ Tree para años de publicación.")

    def insert(self, book):
        logger.info(f"Insertando libro '{book.title}' en el B+ Tree bajo el año {book.publication_year}.")
        root = self.root
        if len(root.keys) == (self.order - 1):
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, book)

    def _insert_non_full(self, node, book):
        if node.leaf:
            node.keys.append(book)
            node.keys.sort(key=lambda x: x.publication_year)
            logger.debug(f"Libro '{book.title}' insertado en una hoja del B+ Tree.")
        else:
            # Simplificación: siempre insertar en el primer hijo
            self._insert_non_full(node.children[0], book)

    def _split_child(self, parent, index):
        node = parent.children[index]
        split_point = len(node.keys) // 2
        new_node = BPlusTreeNode(leaf=node.leaf)
        new_node.keys = node.keys[split_point:]
        node.keys = node.keys[:split_point]
        parent.children.insert(index + 1, new_node)
        parent.keys.append(new_node.keys[0].publication_year)
        parent.keys.sort()
        logger.debug(f"Nodo dividido en el B+ Tree. Nueva clave de separación: {new_node.keys[0].publication_year}.")

    def search(self, year):
        logger.info(f"Buscando libros publicados en el año {year} en el B+ Tree.")
        node = self.root
        while not node.leaf:
            node = node.children[0]
        results = [book for book in node.keys if book.publication_year == year]
        if results:
            logger.info(f"Encontrados {len(results)} libros publicados en el año {year}.")
        else:
            logger.info(f"No se encontraron libros publicados en el año {year}.")
        return results