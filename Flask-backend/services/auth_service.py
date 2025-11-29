import bcrypt
from typing import Optional
from services.user_service import UserService
from models.user import User

class AuthService:
    """Service pour gérer l'authentification"""
    
    def __init__(self):
        self.user_service = UserService()
    
    def hash_password(self, password: str) -> str:
        """Hash un mot de passe"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Vérifie un mot de passe"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def register(self, username: str, email: str, password: str, role: str = 'etudiant') -> Optional[User]:
        """Enregistre un nouvel utilisateur"""
        # Vérifier si l'utilisateur existe déjà
        if self.user_service.get_user_by_username(username):
            return None
        if self.user_service.get_user_by_email(email):
            return None
        
        # Créer l'utilisateur
        password_hash = self.hash_password(password)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role
        }
        return self.user_service.create_user(user_data)
    
    def login(self, username: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = self.user_service.get_user_by_username(username)
        if user and self.verify_password(password, user.password_hash):
            return user
        return None

