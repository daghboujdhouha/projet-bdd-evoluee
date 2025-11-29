from typing import List, Optional
from bson import ObjectId
from database import db
from models.user import User

class UserService:
    """Service pour gérer les opérations sur les utilisateurs"""
    
    def __init__(self):
        self.collection = db.get_db()['users']
    
    def create_user(self, user_data: dict) -> User:
        """Crée un nouvel utilisateur"""
        user = User(**user_data)
        result = self.collection.insert_one(user.to_dict())
        user._id = str(result.inserted_id)
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        try:
            user_doc = self.collection.find_one({'_id': ObjectId(user_id)})
            if user_doc:
                return User.from_dict(user_doc)
            return None
        except:
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Récupère un utilisateur par son nom d'utilisateur"""
        user_doc = self.collection.find_one({'username': username})
        if user_doc:
            return User.from_dict(user_doc)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email"""
        user_doc = self.collection.find_one({'email': email})
        if user_doc:
            return User.from_dict(user_doc)
        return None
    
    def get_all_users(self) -> List[User]:
        """Récupère tous les utilisateurs"""
        users = []
        for user_doc in self.collection.find():
            users.append(User.from_dict(user_doc))
        return users
    
    def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """Met à jour un utilisateur"""
        try:
            from datetime import datetime
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            if result.modified_count > 0:
                return self.get_user_by_id(user_id)
            return None
        except:
            return None
    
    def delete_user(self, user_id: str) -> bool:
        """Supprime un utilisateur"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

