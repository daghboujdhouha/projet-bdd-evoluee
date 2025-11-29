from pymongo import MongoClient
from config import Config

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Établit la connexion à MongoDB"""
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client[Config.MONGODB_DB]
        return self._db
    
    def get_db(self):
        """Retourne l'instance de la base de données"""
        if self._db is None:
            return self.connect()
        return self._db
    
    def close(self):
        """Ferme la connexion à MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Instance globale
db = Database()

