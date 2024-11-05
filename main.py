import tkinter as tk
from tkinter import messagebox, simpledialog
import logging

logging.basicConfig(filename='registro_sistema.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Book:
    def __init__(self, cover, title, author, genre, preview, year):
        self.cover = cover
        self.title = title
        self.author = author
        self.genre = genre
        self.preview = preview
        self.year = year

    def __str__(self):
        return f"Portada: {self.cover}\nTítulo: {self.title}\nAutor: {self.author}\nGénero: {self.genre}\nAño: {self.year}\nVista previa: {self.preview}\n"

    def __eq__(self, other):
        return (
            isinstance(other, Book) and
            self.title == other.title and
            self.author == other.author and
            self.year == other.year
        )

    def __hash__(self):
        return hash((self.title, self.author, self.year))

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

class Graph:
    def __init__(self):
        self.graph = {}

    def add_book(self, book):
        if book not in self.graph:
            self.graph[book] = []

    def add_edge(self, book1, book2):
        if book1 in self.graph and book2 in self.graph:
            self.graph[book1].append(book2)
            self.graph[book2].append(book1)

    def build_graph(self, books):
        # Agregar todos los libros al grafo
        for book in books:
            self.add_book(book)
        # Crear relaciones basadas en autor, año y título
        for i in range(len(books)):
            for j in range(i + 1, len(books)):
                if books[i].author == books[j].author:
                    self.add_edge(books[i], books[j])
                elif books[i].year == books[j].year:
                    self.add_edge(books[i], books[j])
                elif books[i].title == books[j].title:
                    self.add_edge(books[i], books[j])

class LibraryGUI:
    def __init__(self, library):
        self.library = library
        self.root = tk.Tk()
        self.root.title("Sistema de Biblioteca")

        # Crear elementos de la interfaz
        self.create_widgets()
        logging.info('Interfaz gráfica iniciada.')

        # Iniciar el bucle principal
        self.root.mainloop()

    def create_widgets(self):
        # Marco para las acciones
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        # Botón para agregar un libro
        add_book_button = tk.Button(action_frame, text="Agregar Libro", command=self.add_book)
        add_book_button.grid(row=0, column=0, padx=5)

        # Botón para buscar libros
        search_button = tk.Button(action_frame, text="Buscar Libros", command=self.search_books)
        search_button.grid(row=0, column=1, padx=5)

        # Botón para ordenar libros
        sort_button = tk.Button(action_frame, text="Ordenar Libros", command=self.sort_books)
        sort_button.grid(row=0, column=2, padx=5)

        # Área de texto para mostrar resultados
        self.result_text = tk.Text(self.root, height=20, width=80)
        self.result_text.pack(pady=10)

    def add_book(self):
        # Solicitar información del libro
        title = simpledialog.askstring("Título", "Ingrese el título del libro:")
        author = simpledialog.askstring("Autor", "Ingrese el autor del libro:")
        genre = simpledialog.askstring("Género", "Ingrese el género del libro:")
        year = simpledialog.askinteger("Año", "Ingrese el año de publicación:")
        cover = simpledialog.askstring("Portada", "Ingrese la portada del libro:")
        preview = simpledialog.askstring("Vista Previa", "Ingrese la vista previa del libro:")

        # Crear y agregar el libro
        if title and author and genre and year:
            book = Book(cover, title, author, genre, preview, year)
            self.library.insertar_libro(book)
            messagebox.showinfo("Éxito", f"Libro '{title}' agregado.")
            logging.info(f"Libro '{title}' agregado a través de la interfaz gráfica.")
        else:
            messagebox.showwarning("Información incompleta", "Todos los campos son obligatorios.")
            logging.warning("Intento de agregar libro con información incompleta.")

    def search_books(self):
        # Ventana para seleccionar el tipo de búsqueda
        search_window = tk.Toplevel(self.root)
        search_window.title("Buscar Libros")

        tk.Label(search_window, text="Seleccione el criterio de búsqueda:").pack(pady=5)

        # Botones para diferentes tipos de búsqueda
        tk.Button(search_window, text="Por Título", command=lambda: self.perform_search("título")).pack(pady=5)
        tk.Button(search_window, text="Por Autor", command=lambda: self.perform_search("autor")).pack(pady=5)
        tk.Button(search_window, text="Por Género", command=lambda: self.perform_search("género")).pack(pady=5)
        tk.Button(search_window, text="Por Año", command=lambda: self.perform_search("año")).pack(pady=5)

    def perform_search(self, criterion):
        query = simpledialog.askstring("Buscar", f"Ingrese el {criterion} a buscar:")
        if query:
            if criterion == "título":
                results = self.library.buscar_por_titulo(query)
            elif criterion == "autor":
                results = self.library.buscar_por_autor(query)
            elif criterion == "género":
                results = self.library.buscar_por_genero(query)
            elif criterion == "año":
                try:
                    year = int(query)
                    results = self.library.buscar_por_año(year)
                except ValueError:
                    messagebox.showerror("Error", "El año debe ser un número.")
                    logging.error("Error al buscar por año: el año debe ser un número.")
                    return
            else:
                results = []

            # Mostrar resultados
            self.result_text.delete(1.0, tk.END)
            if results:
                for book in results:
                    self.result_text.insert(tk.END, str(book) + "\n")
                logging.info(f"Búsqueda por {criterion} '{query}' realizada. {len(results)} resultados encontrados.")
            else:
                self.result_text.insert(tk.END, "No se encontraron libros.")
                logging.info(f"Búsqueda por {criterion} '{query}' realizada. No se encontraron resultados.")

    def sort_books(self):
        # Ventana para seleccionar el tipo de ordenamiento
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Ordenar Libros")

        tk.Label(sort_window, text="Seleccione el criterio de ordenamiento:").pack(pady=5)

        # Botones para diferentes tipos de ordenamiento
        tk.Button(sort_window, text="Por Autor", command=lambda: self.perform_sort("autor")).pack(pady=5)
        tk.Button(sort_window, text="Por Título", command=lambda: self.perform_sort("título")).pack(pady=5)
        tk.Button(sort_window, text="Por Año", command=lambda: self.perform_sort("año")).pack(pady=5)

    def perform_sort(self, criterion):
        if criterion == "autor":
            self.library.ordenar_por_autor()
        elif criterion == "título":
            self.library.ordenar_por_titulo()
        elif criterion == "año":
            self.library.ordenar_por_año()
        # Mostrar libros ordenados
        self.result_text.delete(1.0, tk.END)
        for book in self.library.books:
            self.result_text.insert(tk.END, str(book) + "\n")
        logging.info(f"Libros ordenados por {criterion}.")

class LoginGUI:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.on_login_success = on_login_success

        # Crear elementos de la interfaz de inicio de sesión
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validar credenciales (aquí se puede agregar lógica para validar contra una base de datos o archivo)
        if username == "admin" and password == "password":
            logging.info(f"Usuario '{username}' inició sesión exitosamente.")
            self.on_login_success()
        else:
            logging.warning(f"Intento de inicio de sesión fallido para el usuario '{username}'.")
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Asumiendo que las clases Library, Book y demás ya están definidas

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal temporalmente

    def on_login_success():
        root.deiconify()  # Mostrar la ventana principal
        root.destroy()  # Cerrar la ventana de inicio de sesión
        biblioteca = Library()
        gui = LibraryGUI(biblioteca)

    login_gui = LoginGUI(root, on_login_success)
    root.mainloop()