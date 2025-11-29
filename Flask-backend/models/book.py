from datetime import datetime
from typing import Optional

class Book:
    """Modèle pour représenter un livre dans la base de données"""
    
    def __init__(self, title: str, author: str, genre: str, year: int, 
                 description: str, isbn: str, status: str = "disponible",
                 _id: Optional[str] = None):
        self._id = _id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.description = description
        self.isbn = isbn
        self.status = status  # disponible, réservé, emprunté
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit le livre en dictionnaire pour MongoDB"""
        data = {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year': self.year,
            'description': self.description,
            'isbn': self.isbn,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id:
            data['_id'] = self._id
        return data
    
    @staticmethod
    def from_dict(data: dict):
        """Crée un objet Book à partir d'un dictionnaire MongoDB"""
        book = Book(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            year=data['year'],
            description=data['description'],
            isbn=data['isbn'],
            status=data.get('status', 'disponible'),
            _id=str(data['_id']) if '_id' in data else None
        )
        if 'created_at' in data:
            book.created_at = data['created_at']
        if 'updated_at' in data:
            book.updated_at = data['updated_at']
        return book

