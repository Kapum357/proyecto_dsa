import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
from sorting import quick_sort, merge_sort, binary_search
from graph import Graph
from trees import Trie, TitleBST, RBTree, HashTable, NaryTree, BPlusTree
from book import Book

# Configuración avanzada del sistema de logueo
logger = logging.getLogger('LibrarySystem')
logger.setLevel(logging.DEBUG)

# Formateador
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Manejador de archivo con rotación
file_handler = RotatingFileHandler('library_operations.log', maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Manejador de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Agregar manejadores al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Implementación de funciones de inserción y búsqueda
title_trie = Trie()
author_trie = Trie()
title_bst = TitleBST()
rb_tree = RBTree()
hash_table = HashTable()
nary_tree = NaryTree()
bplus_tree = BPlusTree()
graph = Graph()

def add_book(book):
    logger.info(f"Agregando libro '{book.title}' al sistema.")
    # Insertar en el Trie de títulos
    title_trie.insert(book.title, book)
    # Insertar en el Trie de autores
    author_trie.insert(book.author, book)
    # Insertar en el Árbol Binario de Títulos
    title_bst.insert(book)
    # Insertar en el Árbol Rojo-Negro
    rb_tree.insert(book)
    # Insertar en la Tabla Hash
    hash_table.insert(book)
    # Insertar en el Árbol N-ario por género
    nary_tree.insert(book)
    # Insertar en el B+ Tree por año de publicación
    bplus_tree.insert(book)
    # Agregar al Grafo
    graph.add_book(book)
    logger.info(f"Libro '{book.title}' agregado exitosamente al sistema.")

def search_books(parameter, value):
    if parameter == 'titulo':
        return title_trie.search(value)
    elif parameter == 'autor':
        return author_trie.search(value)
    elif parameter == 'año':
        return bplus_tree.search(int(value))
    elif parameter == 'género':
        return nary_tree.search(value)
    else:
        logger.warning(f"Parámetro de búsqueda '{parameter}' no reconocido.")
        return []

def sort_books(books, key, method='quick'):
    if method == 'quick':
        quick_sort(books, key)
        logger.info(f"Books sorted by {key} using Quick Sort.")
    elif method == 'merge':
        merge_sort(books, key)
        logger.info(f"Books sorted by {key} using Merge Sort.")
    else:
        logger.warning(f"Sorting method '{method}' not recognized.")

def search_sorted_books(books, key, value):
    result = binary_search(books, key, value)
    if result:
        logger.info(f"Book found: {result.title} by {result.author}")
    else:
        logger.info(f"No book found with {key} = {value}")
    return result

# Implementación de la interfaz gráfica
class LibraryGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Biblioteca")
        self.master.geometry("800x600")

        # Search bar
        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=10)
        self.search_label = tk.Label(self.search_frame, text="Buscar:")
        self.search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(self.search_frame, text="Buscar", command=self.search_books)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Book list
        self.book_list_frame = tk.Frame(self.master)
        self.book_list_frame.pack(fill=tk.BOTH, expand=True)
        self.book_list = ttk.Treeview(self.book_list_frame, columns=("title", "author", "genre", "year"), show="headings")
        self.book_list.heading("title", text="Título")
        self.book_list.heading("author", text="Autor")
        self.book_list.heading("genre", text="Género")
        self.book_list.heading("year", text="Año")
        self.book_list.pack(fill=tk.BOTH, expand=True)
        self.book_list.bind("<Double-1>", self.show_book_details)

        # Book details
        self.details_frame = tk.Frame(self.master)
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.details_text = tk.Text(self.details_frame, wrap=tk.WORD, height=10)
        self.details_text.pack(fill=tk.BOTH, expand=True)

        # Add Book button
        self.add_button = tk.Button(self.master, text="Agregar Libro", command=self.add_book_dialog)
        self.add_button.pack(pady=5)

        # Visualize Data button
        self.visualize_button = tk.Button(self.master, text="Visualizar Datos", command=self.visualize_data)
        self.visualize_button.pack(pady=5)

    def search_books(self):
        query = self.search_entry.get()
        logger.info(f"Buscando libros con el término '{query}'")
        results = search_books('titulo', query)  # Example search by title
        self.book_list.delete(*self.book_list.get_children())
        for book in results:
            self.book_list.insert("", "end", values=(book.title, book.author, book.genre, book.publication_year))

    def show_book_details(self, event):
        selected_item = self.book_list.selection()[0]
        book_title = self.book_list.item(selected_item, "values")[0]
        book = search_books('titulo', book_title)[0]
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Título: {book.title}\n")
        self.details_text.insert(tk.END, f"Autor: {book.author}\n")
        self.details_text.insert(tk.END, f"Género: {book.genre}\n")
        self.details_text.insert(tk.END, f"Año de Publicación: {book.publication_year}\n")
        self.details_text.insert(tk.END, f"Vista Previa: {book.vista_previa}\n")
        logger.info(f"Mostrando detalles del libro '{book.title}'")

    def add_book_dialog(self):
        dialog = AddBookDialog(self.master)
        self.master.wait_window(dialog.top)
        if dialog.book:
            add_book(dialog.book)
            self.book_list.insert("", "end", values=(dialog.book.title, dialog.book.author, dialog.book.genre, dialog.book.publication_year))
            logger.info(f"Libro '{dialog.book.title}' agregado desde la interfaz gráfica.")

    def visualize_data(self):
        genres = {}
        for book in title_bst.in_order_traversal():
            if book.genre in genres:
                genres[book.genre] += 1
            else:
                genres[book.genre] = 1

        plt.figure(figsize=(10, 5))
        plt.bar(genres.keys(), genres.values())
        plt.xlabel('Género')
        plt.ylabel('Cantidad de Libros')
        plt.title('Cantidad de Libros por Género')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        logger.info("Visualización de datos generada.")

class AddBookDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        top.title("Agregar Libro")

        tk.Label(top, text="Título").pack()
        self.title_entry = tk.Entry(top)
        self.title_entry.pack()

        tk.Label(top, text="Autor").pack()
        self.author_entry = tk.Entry(top)
        self.author_entry.pack()

        tk.Label(top, text="Género").pack()
        self.genre_entry = tk.Entry(top)
        self.genre_entry.pack()

        tk.Label(top, text="Año de Publicación").pack()
        self.year_entry = tk.Entry(top)
        self.year_entry.pack()

        tk.Label(top, text="Portada (URL o path)").pack()
        self.portada_entry = tk.Entry(top)
        self.portada_entry.pack()

        tk.Label(top, text="Vista Previa").pack()
        self.preview_entry = tk.Entry(top)
        self.preview_entry.pack()

        tk.Button(top, text="Agregar", command=self.add_book).pack(pady=5)

        self.book = None

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        try:
            year = int(self.year_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Año de publicación debe ser un número.")
            return
        portada = self.portada_entry.get()
        vista_previa = self.preview_entry.get()
        self.book = Book(title, author, genre, year, portada, vista_previa)
        self.top.destroy()

def main():
    root = tk.Tk()
    app = LibraryGUI(root)
    
    # Ejemplo de adición de libro
    book = Book("El Quijote", "Miguel de Cervantes", "Novela", 1605, "portada.jpg", "En un lugar de la Mancha...")
    add_book(book)
    
    # Ejemplo de búsqueda
    resultados = search_books('titulo', 'El Qui')
    for libro in resultados:
        print(libro.title, libro.author)
    
    # Ejemplo de ordenamiento
    sorted_books = title_trst_in_order = []  # Implement in_order_traversal if needed
    sort_books(sorted_books, 'title', method='quick')
    
    root.mainloop()

if __name__ == "__main__":
    main()