from typing import List, Optional, Dict
from bson import ObjectId
from database import db
from models.book import Book

class BookService:
    """Service pour gérer les opérations CRUD sur les livres"""
    
    def __init__(self):
        self.collection = db.get_db()['books']
    
    def create_book(self, book_data: dict) -> Book:
        """Crée un nouveau livre"""
        book = Book(**book_data)
        result = self.collection.insert_one(book.to_dict())
        book._id = str(result.inserted_id)
        return book
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Récupère un livre par son ID"""
        try:
            book_doc = self.collection.find_one({'_id': ObjectId(book_id)})
            if book_doc:
                return Book.from_dict(book_doc)
            return None
        except:
            return None
    
    def get_all_books(self, filters: Optional[Dict] = None) -> List[Book]:
        """Récupère tous les livres avec filtres optionnels"""
        query = {}
        if filters:
            if 'title' in filters:
                query['title'] = {'$regex': filters['title'], '$options': 'i'}
            if 'author' in filters:
                query['author'] = {'$regex': filters['author'], '$options': 'i'}
            if 'genre' in filters:
                query['genre'] = filters['genre']
            if 'year' in filters:
                query['year'] = int(filters['year'])
            if 'isbn' in filters:
                query['isbn'] = filters['isbn']
            if 'status' in filters:
                query['status'] = filters['status']
        
        books = []
        for book_doc in self.collection.find(query):
            books.append(Book.from_dict(book_doc))
        return books
    
    def update_book(self, book_id: str, update_data: dict) -> Optional[Book]:
        """Met à jour un livre"""
        try:
            # Vérifier d'abord si le livre existe
            book = self.get_book_by_id(book_id)
            if not book:
                return None
            
            # Ajouter la date de mise à jour
            from datetime import datetime
            update_data['updated_at'] = datetime.utcnow()
            
            # Effectuer la mise à jour
            result = self.collection.update_one(
                {'_id': ObjectId(book_id)},
                {'$set': update_data}
            )
            
            # Retourner le livre mis à jour (même si aucune modification n'a été faite)
            if result.matched_count > 0:
                return self.get_book_by_id(book_id)
            return None
        except Exception as e:
            print(f"Erreur lors de la mise à jour du livre: {str(e)}")
            return None
    
    def delete_book(self, book_id: str) -> bool:
        """Supprime un livre"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(book_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def update_book_status(self, book_id: str, status: str) -> bool:
        """Met à jour le statut d'un livre"""
        try:
            from datetime import datetime
            result = self.collection.update_one(
                {'_id': ObjectId(book_id)},
                {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False

