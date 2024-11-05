class GenreNode:
    def __init__(self, genre_name):
        self.genre_name = genre_name
        self.books = []
        self.subgenres = []

    def add_subgenre(self, subgenre_node):
        self.subgenres.append(subgenre_node)

    def add_book(self, book):
        self.books.append(book)
class YearNode:
    def __init__(self, year):
        self.year = year
        self.books = []
        self.left = None
        self.right = None
        self.height = 1  # Altura del nodo para balancear el árbol

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

    def balance_factor(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def update_height(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)

    def rotate_left(self):
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        self.update_height()
        new_root.update_height()
        return new_root

    def rotate_right(self):
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        self.update_height()
        new_root.update_height()
        return new_root

    def balance(self):
        self.update_height()
        balance = self.balance_factor()
        if balance > 1:
            if self.left.balance_factor() < 0:
                self.left = self.left.rotate_left()
            return self.rotate_right()
        if balance < -1:
            if self.right.balance_factor() > 0:
                self.right = self.right.rotate_right()
            return self.rotate_left()
        return self