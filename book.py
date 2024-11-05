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