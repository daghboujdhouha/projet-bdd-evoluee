from datetime import datetime, timedelta
from typing import Optional

class Reservation:
    """Modèle pour représenter une réservation dans la base de données"""
    
    def __init__(self, user_id: str, book_id: str, 
                 reservation_date: Optional[datetime] = None,
                 expiry_date: Optional[datetime] = None,
                 status: str = "active",
                 _id: Optional[str] = None):
        self._id = _id
        self.user_id = user_id
        self.book_id = book_id
        self.reservation_date = reservation_date or datetime.utcnow()
        # Expire après 7 jours par défaut
        self.expiry_date = expiry_date or (self.reservation_date + timedelta(days=7))
        self.status = status  # active, expired, cancelled, completed
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit la réservation en dictionnaire pour MongoDB"""
        data = {
            'user_id': self.user_id,
            'book_id': self.book_id,
            'reservation_date': self.reservation_date,
            'expiry_date': self.expiry_date,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id:
            data['_id'] = self._id
        return data
    
    @staticmethod
    def from_dict(data: dict):
        """Crée un objet Reservation à partir d'un dictionnaire MongoDB"""
        reservation = Reservation(
            user_id=data['user_id'],
            book_id=data['book_id'],
            reservation_date=data.get('reservation_date', datetime.utcnow()),
            expiry_date=data.get('expiry_date'),
            status=data.get('status', 'active'),
            _id=str(data['_id']) if '_id' in data else None
        )
        if 'created_at' in data:
            reservation.created_at = data['created_at']
        if 'updated_at' in data:
            reservation.updated_at = data['updated_at']
        return reservation

