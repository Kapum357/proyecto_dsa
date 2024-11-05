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