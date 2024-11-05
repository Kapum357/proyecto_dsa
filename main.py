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