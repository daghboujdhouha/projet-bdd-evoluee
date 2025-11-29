from datetime import datetime
from typing import Optional

class User:
    """Modèle pour représenter un utilisateur dans la base de données"""
    
    ROLES = ['admin', 'etudiant', 'enseignant']
    
    def __init__(self, username: str, email: str, password_hash: str, 
                 role: str = 'etudiant', _id: Optional[str] = None):
        if role not in self.ROLES:
            raise ValueError(f"Role must be one of {self.ROLES}")
        
        self._id = _id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit l'utilisateur en dictionnaire pour MongoDB"""
        data = {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id:
            data['_id'] = self._id
        return data
    
    @staticmethod
    def from_dict(data: dict):
        """Crée un objet User à partir d'un dictionnaire MongoDB"""
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data.get('role', 'etudiant'),
            _id=str(data['_id']) if '_id' in data else None
        )
        if 'created_at' in data:
            user.created_at = data['created_at']
        if 'updated_at' in data:
            user.updated_at = data['updated_at']
        return user

