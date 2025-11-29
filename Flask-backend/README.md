# Bibliothèque Numérique - Backend Flask

Application backend Flask pour la gestion d'une bibliothèque numérique avec base de données MongoDB.

## 📋 Prérequis

- Python 3.8+
- MongoDB (local ou distant)
- pip

## 🚀 Installation

1. **Cloner le projet et naviguer vers le dossier backend**
   ```bash
   cd Flask-backend
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python3 -m venv venv
   
   # Sur Windows
   venv\Scripts\activate
   
   # Sur Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   
   Créer un fichier `.env` à la racine du projet Flask-backend :
   ```env
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DB=bibliotheque_numerique
   JWT_SECRET_KEY=your-secret-key-change-in-production
   SECRET_KEY=your-secret-key-change-in-production
   FLASK_DEBUG=True
   ```

5. **Démarrer MongoDB**
   
   Assurez-vous que MongoDB est en cours d'exécution sur votre machine.

## 🏃 Exécution

```bash
python3 app.py
```

L'API sera accessible sur `http://localhost:5000`

## 📁 Structure du Projet

```
Flask-backend/
├── app.py                 # Point d'entrée de l'application
├── config.py              # Configuration de l'application
├── database.py            # Connexion MongoDB
├── requirements.txt       # Dépendances Python
├── models/                # Modèles de données
│   ├── book.py
│   ├── user.py
│   ├── reservation.py
│   └── borrow.py
├── services/              # Logique métier
│   ├── book_service.py
│   ├── user_service.py
│   ├── auth_service.py
│   ├── reservation_service.py
│   └── borrow_service.py
├── controllers/           # Routes API
│   ├── auth_controller.py
│   ├── book_controller.py
│   ├── user_controller.py
│   ├── reservation_controller.py
│   └── borrow_controller.py
└── middleware/            # Middlewares d'authentification
    └── auth_middleware.py
```

## 🔌 API Endpoints

### Authentification (`/api/auth`)

- `POST /api/auth/register` - Enregistrer un nouvel utilisateur
- `POST /api/auth/login` - Se connecter
- `GET /api/auth/me` - Obtenir l'utilisateur actuel (authentifié)

### Livres (`/api/books`)

- `GET /api/books` - Liste tous les livres (avec filtres optionnels)
- `GET /api/books/<id>` - Obtenir un livre par ID
- `POST /api/books` - Créer un livre (admin seulement)
- `PUT /api/books/<id>` - Mettre à jour un livre (admin seulement)
- `DELETE /api/books/<id>` - Supprimer un livre (admin seulement)

**Filtres disponibles pour GET /api/books:**
- `?title=<titre>` - Recherche par titre
- `?author=<auteur>` - Recherche par auteur
- `?genre=<genre>` - Filtrer par genre
- `?year=<année>` - Filtrer par année
- `?isbn=<isbn>` - Recherche par ISBN
- `?status=<statut>` - Filtrer par statut (disponible, réservé, emprunté)

### Utilisateurs (`/api/users`)

- `GET /api/users` - Liste tous les utilisateurs (admin seulement)
- `GET /api/users/<id>` - Obtenir un utilisateur par ID (admin seulement)
- `PUT /api/users/<id>` - Mettre à jour un utilisateur (admin seulement)
- `DELETE /api/users/<id>` - Supprimer un utilisateur (admin seulement)

### Réservations (`/api/reservations`)

- `POST /api/reservations` - Créer une réservation
- `GET /api/reservations` - Liste les réservations (de l'utilisateur ou toutes si admin)
- `GET /api/reservations/<id>` - Obtenir une réservation par ID
- `DELETE /api/reservations/<id>` - Annuler une réservation

### Emprunts (`/api/borrows`)

- `POST /api/borrows` - Créer un emprunt
- `GET /api/borrows` - Liste les emprunts (de l'utilisateur ou tous si admin)
- `GET /api/borrows/<id>` - Obtenir un emprunt par ID
- `POST /api/borrows/<id>/return` - Retourner un livre

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification. 

Pour utiliser les endpoints protégés, inclure le token dans l'en-tête :
```
Authorization: Bearer <access_token>
```

## 👥 Rôles

- **admin** : Accès complet à toutes les fonctionnalités
- **etudiant** : Peut réserver et emprunter des livres
- **enseignant** : Peut réserver et emprunter des livres

## 📝 Exemples d'utilisation

### Enregistrement
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "etudiant"
  }'
```

### Connexion
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'
```

### Créer un livre (admin)
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Le Petit Prince",
    "author": "Antoine de Saint-Exupéry",
    "genre": "Fiction",
    "year": 1943,
    "description": "Un conte poétique et philosophique",
    "isbn": "978-2070612758"
  }'
```

## 🛠️ Technologies Utilisées

- **Flask** : Framework web Python
- **MongoDB** : Base de données NoSQL orientée document
- **PyMongo** : Driver Python pour MongoDB
- **Flask-JWT-Extended** : Gestion des tokens JWT
- **Flask-CORS** : Gestion CORS pour les requêtes cross-origin
- **bcrypt** : Hashage des mots de passe

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique.

