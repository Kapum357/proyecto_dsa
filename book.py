class Book:
    def __init__(self, cover, title, author, genre, preview, year):
        self.cover = cover
        self.title = title
        self.author = author
        self.genre = genre
        self.preview = preview
        self.year = year

    def __str__(self):
        return (
            f"Portada: {self.cover}\n"
            f"Título: {self.title}\n"
            f"Autor: {self.author}\n"
            f"Género: {self.genre}\n"
            f"Año: {self.year}\n"
            f"Vista previa: {self.preview}\n"
        )

    def __eq__(self, other):
        return (
            isinstance(other, Book) and
            self.cover == other.cover and
            self.title == other.title and
            self.author == other.author and
            self.genre == other.genre and
            self.preview == other.preview and
            self.year == other.year
        )

    def __hash__(self):
        return hash((
            self.cover,
            self.title,
            self.author,
            self.genre,
            self.preview,
            self.year
        ))