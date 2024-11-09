class Book:
    def __init__(self, title, author, genre, publication_year, portada, vista_previa):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = publication_year
        self.portada = portada  # Image of the book cover
        self.vista_previa = vista_previa  # Preview fragment of the book