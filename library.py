from graph import Graph
from nodes import YearNode, GenreNode

class Library:
    def __init__(self):
        self.books = []
        self.year_tree = None
        self.genre_root = None
        self.graph = Graph()

    def insertar_libro(self, book):
        self.books.append(book)
        # Insertar en el árbol de años
        if self.year_tree is None:
            self.year_tree = YearNode(book.year)
            self.year_tree.books.append(book)
        else:
            self.year_tree = self.year_tree.insert(book)
        # Insertar en el árbol de géneros
        if self.genre_root is None:
            self.genre_root = GenreNode(book.genre)
            self.genre_root.add_book(book)
        else:
            self.insertar_en_genero(self.genre_root, book)
        # Agregar al grafo
        self.graph.add_book(book)
        print(f"Libro '{book.title}' insertado.")

    def insertar_en_genero(self, nodo_actual, book):
        if nodo_actual.genre_name == book.genre:
            nodo_actual.add_book(book)
        else:
            # Buscar en subgéneros
            for subgenero in nodo_actual.subgenres:
                if subgenero.genre_name == book.genre:
                    subgenero.add_book(book)
                    return
            # Si no se encuentra, agregar como nuevo subgénero
            nuevo_subgenero = GenreNode(book.genre)
            nuevo_subgenero.add_book(book)
            nodo_actual.add_subgenre(nuevo_subgenero)

    def buscar_por_titulo(self, titulo):
        resultados = [book for book in self.books if titulo.lower() in book.title.lower()]
        return resultados

    def buscar_por_autor(self, autor):
        resultados = [book for book in self.books if autor.lower() in book.author.lower()]
        return resultados

    def buscar_por_genero(self, genero):
        resultados = []
        def buscar_en_genero(nodo):
            if nodo.genre_name.lower() == genero.lower():
                resultados.extend(nodo.books)
            for subgenero in nodo.subgenres:
                buscar_en_genero(subgenero)
        if self.genre_root:
            buscar_en_genero(self.genre_root)
        return resultados

    def buscar_por_año(self, año):
        resultados = []
        def buscar_en_arbol(nodo):
            if nodo is None:
                return
            if nodo.year == año:
                resultados.extend(nodo.books)
            elif año < nodo.year:
                buscar_en_arbol(nodo.left)
            else:
                buscar_en_arbol(nodo.right)
        buscar_en_arbol(self.year_tree)
        return resultados

    def buscar_por_autor_y_año(self, autor, año):
        resultados_por_año = self.buscar_por_año(año)
        resultados = [book for book in resultados_por_año if autor.lower() in book.author.lower()]
        return resultados

    def buscar_por_titulo_y_autor(self, titulo, autor):
        resultados_por_titulo = self.buscar_por_titulo(titulo)
        resultados = [book for book in resultados_por_titulo if autor.lower() in book.author.lower()]
        return resultados

    def eliminar_libro(self, title):
        for i, book in enumerate(self.books):
            if book.title == title:
                del self.books[i]
                print(f"Libro '{title}' eliminado.")
                return
        print(f"Libro '{title}' no encontrado.")

    def buscar_libros(self, keyword):
        resultados = []
        for book in self.books:
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword.lower() in book.preview.lower()):
                resultados.append(book)
        return resultados

    def ordenar_libros_por_titulo(self):
        self.books.sort(key=lambda book: book.title)

    def ordenar_libros_por_autor(self):
        self.books.sort(key=lambda book: book.author)

    def ordenar_libros_por_año(self):
        self.books.sort(key=lambda book: book.year)

    def mostrar_libros(self):
        for book in self.books:
            print(book)

    def ordenar_por_autor(self):
        self.books = self.quick_sort(self.books, key=lambda book: book.author.lower())

    def ordenar_por_titulo(self):
        self.books = self.quick_sort(self.books, key=lambda book: book.title.lower())

    def ordenar_por_año(self):
        self.books = self.quick_sort(self.books, key=lambda book: book.year)

    def quick_sort(self, books_list, key):
        if len(books_list) <= 1:
            return books_list
        else:
            pivot = books_list[0]
            lesser = [book for book in books_list[1:] if key(book) < key(pivot)]
            greater = [book for book in books_list[1:] if key(book) >= key(pivot)]
            return self.quick_sort(lesser, key) + [pivot] + self.quick_sort(greater, key)