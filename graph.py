import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Implementación del Grafo para relaciones entre libros
class Edge:
    def __init__(self, from_book, to_book, relation):
        self.from_book = from_book
        self.to_book = to_book
        self.relation = relation  # e.g., 'same_author', 'same_genre'

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        logger.info("Inicializado el Grafo de relaciones entre libros.")

    def add_book(self, book):
        if book.title not in self.nodes:
            self.nodes[book.title] = book
            logger.info(f"Added book '{book.title}' to the graph.")
        else:
            logger.warning(f"Book '{book.title}' already exists in the graph.")

    def connect_books(self, book1_title, book2_title):
        book1 = self.nodes.get(book1_title)
        book2 = self.nodes.get(book2_title)
        if not book1 or not book2:
            logger.warning("One or both books not found in the graph.")
            return

        relations = []
        if book1.author == book2.author:
            relations.append('same_author')
        if book1.genre == book2.genre:
            relations.append('same_genre')
        if book1.publication_year == book2.publication_year:
            relations.append('same_publication_year')

        for relation in relations:
            edge = Edge(book1, book2, relation)
            self.edges.append(edge)
            logger.info(f"Connected '{book1.title}' and '{book2.title}' via '{relation}'.")

    def get_relations(self, book_title):
        relations = []
        for edge in self.edges:
            if edge.from_book.title == book_title or edge.to_book.title == book_title:
                related_title = edge.to_book.title if edge.from_book.title == book_title else edge.from_book.title
                relations.append((related_title, edge.relation))
        return relations