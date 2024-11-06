from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_book(self, book):
        if book not in self.graph:
            self.graph[book] = []

    def add_edge(self, book1, book2, relation):
        self.graph[book1].append((book2, relation))
        self.graph[book2].append((book1, relation))

    def build_graph(self, books):
        for book in books:
            self.add_book(book)
        for i in range(len(books)):
            for j in range(i + 1, len(books)):
                if books[i].author == books[j].author:
                    self.add_edge(books[i], books[j], 'autor')
                if books[i].year == books[j].year:
                    self.add_edge(books[i], books[j], 'año')
                if books[i].genre == books[j].genre:
                    self.add_edge(books[i], books[j], 'género')
                if books[i].title == books[j].title:
                    self.add_edge(books[i], books[j], 'título')

    def get_related_books(self, book):
        return self.graph[book]