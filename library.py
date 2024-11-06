import logging
from nodes import HashTable
from sort import quick_sort
from graph import Graph
from book import Book

class Library:
    def __init__(self):
        self.books = []
        self.hash_table_genres = HashTable()
        self.hash_table_years = HashTable()
        self.graph = Graph()
        self.cargar_libros('books.txt')
        logging.info("Biblioteca inicializada y libros cargados.")

    def cargar_libros(self, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                content = file.read()
            entries = content.split('---')
            for entry in entries:
                if entry.strip():
                    lines = entry.strip().split('\n')
                    book_data = {}
                    for line in lines:
                        key, value = line.split(':', 1)
                        book_data[key.strip().lower()] = value.strip()
                    new_book = Book(
                        cover=book_data.get('cover', ''),
                        title=book_data.get('title', ''),
                        author=book_data.get('author', ''),
                        genre=book_data.get('genre', ''),
                        preview=book_data.get('preview', ''),
                        year=int(book_data.get('year', 0))
                    )
                    self.insertar_libro(new_book)
            logging.info(f"Todos los libros han sido cargados desde {archivo}.")
        except FileNotFoundError:
            logging.error(f"El archivo {archivo} no fue encontrado.")
        except Exception as e:
            logging.error(f"Error al cargar libros: {e}")

    def insertar_libro(self, book):
        self.books.append(book)
        self.hash_table_genres.insert(book.genre.lower(), book)
        self.hash_table_years.insert(book.year, book)
        self.graph.add_book(book)
        logging.info(f"Libro '{book.title}' insertado en la biblioteca.")

    def buscar_por_titulo(self, titulo):
        for book in self.books:
            if book.title.lower() == titulo.lower():
                logging.info(f"Búsqueda por título '{titulo}' realizada. Encontrado.")
                return book
        logging.info(f"Búsqueda por título '{titulo}' realizada. No encontrado.")
        return None

    def buscar_por_autor(self, autor):
        for book in self.books:
            if book.author.lower() == autor.lower():
                logging.info(f"Búsqueda por autor '{autor}' realizada. Encontrado.")
                return book
        logging.info(f"Búsqueda por autor '{autor}' realizada. No encontrado.")
        return None

    def buscar_por_genero(self, genero):
        results = self.hash_table_genres.search(genero.lower())
        logging.info(f"Búsqueda por género '{genero}' realizada. {len(results)} resultados encontrados.")
        return results

    def buscar_por_año(self, año):
        results = self.hash_table_years.search(año)
        logging.info(f"Búsqueda por año '{año}' realizada. {len(results)} resultados encontrados.")
        return results

    def get_related_books(self, book):
        return self.graph.get_related_books(book)

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
        self.books = quick_sort(self.books, key=lambda book: book.author.lower())
        logging.info("Libros ordenados por autor.")

    def ordenar_por_titulo(self):
        self.books = quick_sort(self.books, key=lambda book: book.title.lower())
        logging.info("Libros ordenados por título.")

    def ordenar_por_año(self):
        self.books = quick_sort(self.books, key=lambda book: book.year)
        logging.info("Libros ordenados por año.")

    def quick_sort(self, books_list, key):
        if len(books_list) <= 1:
            return books_list
        else:
            pivot = books_list[0]
            lesser = [book for book in books_list[1:] if key(book) < key(pivot)]
            greater = [book for book in books_list[1:] if key(book) >= key(pivot)]
            return self.quick_sort(lesser, key) + [pivot] + self.quick_sort(greater, key)

    def buscar_por_prefijo_titulo(self, prefix):
        return self.trie_titles.search(prefix.lower())

    def buscar_por_prefijo_autor(self, prefix):
        return self.trie_authors.search(prefix.lower())