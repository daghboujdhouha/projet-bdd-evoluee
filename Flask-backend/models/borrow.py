from datetime import datetime, timedelta
from typing import Optional

class Borrow:
    """Modèle pour représenter un emprunt dans la base de données"""
    
    def __init__(self, user_id: str, book_id: str,
                 borrow_date: Optional[datetime] = None,
                 return_date: Optional[datetime] = None,
                 due_date: Optional[datetime] = None,
                 status: str = "active",
                 _id: Optional[str] = None):
        self._id = _id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date or datetime.utcnow()
        self.return_date = return_date
        # Date d'échéance par défaut: 30 jours
        self.due_date = due_date or (self.borrow_date + timedelta(days=30))
        self.status = status  # active, returned, overdue
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit l'emprunt en dictionnaire pour MongoDB"""
        data = {
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date,
            'due_date': self.due_date,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id:
            data['_id'] = self._id
        return data
    
    @staticmethod
    def from_dict(data: dict):
        """Crée un objet Borrow à partir d'un dictionnaire MongoDB"""
        borrow = Borrow(
            user_id=data['user_id'],
            book_id=data['book_id'],
            borrow_date=data.get('borrow_date', datetime.utcnow()),
            return_date=data.get('return_date'),
            due_date=data.get('due_date'),
            status=data.get('status', 'active'),
            _id=str(data['_id']) if '_id' in data else None
        )
        if 'created_at' in data:
            borrow.created_at = data['created_at']
        if 'updated_at' in data:
            borrow.updated_at = data['updated_at']
        return borrow

