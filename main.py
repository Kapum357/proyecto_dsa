import tkinter as tk
from tkinter import messagebox, simpledialog
from library import Library
from book import Book
import logging

logging.basicConfig(filename='registro_sistema.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # Marco para la barra de búsqueda
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        # Campo de entrada para la búsqueda
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=10)

        # Botón para realizar la búsqueda
        search_button = tk.Button(search_frame, text="Buscar", command=self.search_books)
        search_button.pack(side=tk.LEFT)

        # Marco para las acciones
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        # Botón para agregar un libro
        add_book_button = tk.Button(action_frame, text="Agregar Libro", command=self.add_book)
        add_book_button.pack(side=tk.LEFT, padx=5)

        # Botón para mostrar todos los libros
        show_books_button = tk.Button(action_frame, text="Mostrar Libros", command=self.show_books)
        show_books_button.pack(side=tk.LEFT, padx=5)

        # Área de texto para mostrar resultados
        self.results_text = tk.Text(self.root, width=80, height=20)
        self.results_text.pack(pady=10)

    def search_books(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Entrada Vacía", "Por favor, ingresa un término de búsqueda.")
            return

        # Buscar por título
        book = self.library.buscar_por_titulo(query)
        if book:
            self.display_book(book)
            logging.info(f"Libro encontrado: {book.title}")
            return

        # Buscar por autor
        book = self.library.buscar_por_autor(query)
        if book:
            self.display_book(book)
            logging.info(f"Libro encontrado: {book.title}")
            return

        # Buscar por género
        books = self.library.buscar_por_genero(query)
        if books:
            for b in books:
                self.display_book(b)
            logging.info(f"{len(books)} libros encontrados por género: {query}")
            return

        # Buscar por año
        try:
            year = int(query)
            books = self.library.buscar_por_año(year)
            if books:
                for b in books:
                    self.display_book(b)
                logging.info(f"{len(books)} libros encontrados por año: {year}")
                return
        except ValueError:
            pass

        messagebox.showinfo("No Encontrado", "No se encontraron libros con la búsqueda proporcionada.")
        logging.info(f"Búsqueda sin resultados para: {query}")

    def add_book(self):
        # Solicitar información del libro al usuario
        title = simpledialog.askstring("Título", "Ingrese el título del libro:")
        if not title:
            return
        author = simpledialog.askstring("Autor", "Ingrese el autor del libro:")
        if not author:
            return
        genre = simpledialog.askstring("Género", "Ingrese el género del libro:")
        if not genre:
            return
        year = simpledialog.askinteger("Año", "Ingrese el año de publicación:")
        if not year:
            return
        preview = simpledialog.askstring("Vista Previa", "Ingrese una vista previa del libro:")
        if not preview:
            return
        cover = simpledialog.askstring("Portada", "Ingrese la URL de la portada del libro:")

        # Crear y agregar el libro a la biblioteca
        new_book = Book(cover, title, author, genre, preview, year)
        self.library.insertar_libro(new_book)
        messagebox.showinfo("Éxito", f"El libro '{title}' ha sido agregado exitosamente.")
        logging.info(f"Libro agregado: {title}")

    def show_books(self):
        self.results_text.delete(1.0, tk.END)
        for book in self.library.books:
            self.display_book(book)

    def display_book(self, book):
        self.results_text.insert(tk.END, str(book) + "\n\n")

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

def main():
    library = Library()
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal hasta que el usuario inicie sesión

    def on_login_success():
        root.deiconify()  # Mostrar la ventana principal
        login_window.destroy()
        LibraryGUI(library)

    login_window = tk.Toplevel(root)
    LoginGUI(login_window, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()