from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from database import db
from models.reservation import Reservation
from services.book_service import BookService

class ReservationService:
    """Service pour gérer les réservations"""
    
    def __init__(self):
        self.collection = db.get_db()['reservations']
        self.book_service = BookService()
    
    def create_reservation(self, user_id: str, book_id: str) -> Optional[Reservation]:
        """Crée une nouvelle réservation"""
        # Vérifier que le livre est disponible
        book = self.book_service.get_book_by_id(book_id)
        if not book or book.status != 'disponible':
            return None
        
        # Vérifier si l'utilisateur a déjà une réservation active pour ce livre
        existing = self.collection.find_one({
            'user_id': user_id,
            'book_id': book_id,
            'status': 'active'
        })
        if existing:
            return None
        
        reservation = Reservation(user_id=user_id, book_id=book_id)
        result = self.collection.insert_one(reservation.to_dict())
        reservation._id = str(result.inserted_id)
        
        # Mettre à jour le statut du livre
        self.book_service.update_book_status(book_id, 'réservé')
        
        return reservation
    
    def get_reservation_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Récupère une réservation par son ID"""
        try:
            reservation_doc = self.collection.find_one({'_id': ObjectId(reservation_id)})
            if reservation_doc:
                return Reservation.from_dict(reservation_doc)
            return None
        except:
            return None
    
    def get_reservations_by_user(self, user_id: str) -> List[Reservation]:
        """Récupère toutes les réservations d'un utilisateur"""
        reservations = []
        for res_doc in self.collection.find({'user_id': user_id}):
            reservations.append(Reservation.from_dict(res_doc))
        return reservations
    
    def get_all_reservations(self) -> List[Reservation]:
        """Récupère toutes les réservations"""
        reservations = []
        for res_doc in self.collection.find():
            reservations.append(Reservation.from_dict(res_doc))
        return reservations
    
    def cancel_reservation(self, reservation_id: str, user_id: str) -> bool:
        """Annule une réservation"""
        try:
            reservation = self.get_reservation_by_id(reservation_id)
            if not reservation or reservation.user_id != user_id:
                return False
            
            result = self.collection.update_one(
                {'_id': ObjectId(reservation_id)},
                {'$set': {'status': 'cancelled', 'updated_at': datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                # Vérifier s'il y a d'autres réservations actives pour ce livre
                active_count = self.collection.count_documents({
                    'book_id': reservation.book_id,
                    'status': 'active'
                })
                if active_count == 0:
                    self.book_service.update_book_status(reservation.book_id, 'disponible')
                return True
            return False
        except:
            return False
    
    def complete_reservation(self, reservation_id: str) -> bool:
        """Marque une réservation comme complétée"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(reservation_id)},
                {'$set': {'status': 'completed', 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False

