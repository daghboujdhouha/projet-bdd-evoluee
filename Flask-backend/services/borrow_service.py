from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from database import db
from models.borrow import Borrow
from services.book_service import BookService
from services.reservation_service import ReservationService

class BorrowService:
    """Service pour gérer les emprunts"""
    
    def __init__(self):
        self.collection = db.get_db()['borrows']
        self.book_service = BookService()
        self.reservation_service = ReservationService()
    
    def create_borrow(self, user_id: str, book_id: str) -> Optional[Borrow]:
        """Crée un nouvel emprunt"""
        book = self.book_service.get_book_by_id(book_id)
        if not book:
            return None
        
        # Le livre doit être disponible ou réservé par cet utilisateur
        if book.status == 'emprunté':
            return None
        
        # Si le livre est réservé, vérifier que c'est par cet utilisateur
        if book.status == 'réservé':
            reservations = self.reservation_service.get_reservations_by_user(user_id)
            user_reservation = next(
                (r for r in reservations if r.book_id == book_id and r.status == 'active'),
                None
            )
            if not user_reservation:
                return None
            # Marquer la réservation comme complétée
            self.reservation_service.complete_reservation(user_reservation._id)
        
        borrow = Borrow(user_id=user_id, book_id=book_id)
        result = self.collection.insert_one(borrow.to_dict())
        borrow._id = str(result.inserted_id)
        
        # Mettre à jour le statut du livre
        self.book_service.update_book_status(book_id, 'emprunté')
        
        return borrow
    
    def get_borrow_by_id(self, borrow_id: str) -> Optional[Borrow]:
        """Récupère un emprunt par son ID"""
        try:
            borrow_doc = self.collection.find_one({'_id': ObjectId(borrow_id)})
            if borrow_doc:
                return Borrow.from_dict(borrow_doc)
            return None
        except:
            return None
    
    def get_borrows_by_user(self, user_id: str) -> List[Borrow]:
        """Récupère tous les emprunts d'un utilisateur"""
        borrows = []
        for borrow_doc in self.collection.find({'user_id': user_id}):
            borrows.append(Borrow.from_dict(borrow_doc))
        return borrows
    
    def get_all_borrows(self) -> List[Borrow]:
        """Récupère tous les emprunts"""
        borrows = []
        for borrow_doc in self.collection.find():
            borrows.append(Borrow.from_dict(borrow_doc))
        return borrows
    
    def return_book(self, borrow_id: str, user_id: str, is_admin: bool = False) -> bool:
        """Retourne un livre emprunté"""
        try:
            # Valider l'ID
            try:
                ObjectId(borrow_id)
            except:
                return False
            
            borrow = self.get_borrow_by_id(borrow_id)
            if not borrow:
                return False
            
            # Vérifier que l'emprunt est actif
            if borrow.status != 'active':
                return False
            
            # Vérifier que l'utilisateur est le propriétaire ou un admin
            if not is_admin and borrow.user_id != user_id:
                return False
            
            result = self.collection.update_one(
                {'_id': ObjectId(borrow_id)},
                {'$set': {
                    'status': 'returned',
                    'return_date': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }}
            )
            
            if result.matched_count > 0:
                # Vérifier s'il y a des réservations en attente
                from services.reservation_service import ReservationService
                res_service = ReservationService()
                active_reservations = res_service.collection.count_documents({
                    'book_id': borrow.book_id,
                    'status': 'active'
                })
                
                if active_reservations > 0:
                    self.book_service.update_book_status(borrow.book_id, 'réservé')
                else:
                    self.book_service.update_book_status(borrow.book_id, 'disponible')
                return True
            return False
        except Exception as e:
            print(f"Erreur lors du retour du livre: {str(e)}")
            return False

