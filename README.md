# 📚 Bibliothèque Numérique

Application web complète pour la gestion d'une bibliothèque numérique permettant la gestion des livres, des utilisateurs, des réservations et des emprunts.

## 📋 Description du Projet

Ce projet consiste à développer une bibliothèque numérique permettant la gestion complète des livres ainsi que la gestion des utilisateurs. Le système inclut des fonctionnalités de base pour ajouter, consulter, modifier et supprimer des livres, gérer les emprunts et les réservations, et permettre aux étudiants et enseignants de réserver ou emprunter des ouvrages.

## 🎯 Objectifs

L'objectif principal est de fournir un système simple mais efficace permettant la gestion complète des livres, des utilisateurs, des réservations et des emprunts dans une bibliothèque numérique. Ce système doit être intuitif, sécurisé et facilement maintenable.

Les objectifs spécifiques incluent :

- ✅ Une gestion complète des livres (ajout, suppression, modification, consultation)
- ✅ Une gestion des utilisateurs avec différents rôles (administrateur, étudiant, enseignant)
- ✅ La possibilité pour les utilisateurs de réserver et emprunter des livres
- ✅ Un système de recherche et de filtrage des livres
- ✅ Un système d'authentification sécurisé avec JWT
- ✅ Une interface utilisateur moderne et responsive

## 🚀 Démarrage Rapide

### Prérequis

- **Python** 3.8+
- **Node.js** 18+ et npm
- **MongoDB Community Server** - [Télécharger](https://www.mongodb.com/try/download/community)
- **MongoDB Compass** (optionnel) - [Télécharger](https://www.mongodb.com/try/download/compass)

> 📖 **Documentation détaillée** : 
> - [Guide d'installation Backend Flask](Flask-backend/README.md)
> - [Guide d'installation Frontend Angular](Angular-frontend/README.md)

## 🏗️ Architecture

Le projet est organisé en deux applications principales :

### Backend (Flask)
- **Technologie** : Python Flask
- **Base de données** : MongoDB (NoSQL orientée document)
- **API** : REST API
- **Authentification** : JWT (JSON Web Tokens)
- **Structure** : Architecture MVC avec séparation models/services/controllers

### Frontend (Angular)
- **Technologie** : Angular 17
- **Langage** : TypeScript
- **Interface** : Application web responsive
- **Structure** : Services, Components, Guards, Pages

## 🛠️ Technologies Utilisées

### Backend
- **Flask** 3.0.0 - Framework web Python
- **MongoDB** - Base de données NoSQL orientée document
- **PyMongo** - Driver Python pour MongoDB
- **Flask-JWT-Extended** - Gestion des tokens JWT
- **Flask-CORS** - Gestion CORS
- **bcrypt** - Hashage des mots de passe

### Frontend
- **Angular** 17 - Framework frontend
- **TypeScript** - Langage de programmation
- **RxJS** - Programmation réactive
- **Angular Router** - Navigation
- **Angular Forms** - Gestion des formulaires
- **HTTP Client** - Appels API

## ✨ Fonctionnalités

### Gestion des Livres
- ✅ Consultation de la liste des livres
- ✅ Recherche et filtrage (titre, auteur, genre, année, ISBN, statut)
- ✅ Détails d'un livre
- ✅ Création, modification, suppression (admin seulement)

### Gestion des Utilisateurs
- ✅ Inscription et connexion
- ✅ Gestion des rôles (admin, étudiant, enseignant)
- ✅ Gestion des utilisateurs (admin seulement)

### Réservations
- ✅ Réserver un livre disponible
- ✅ Consulter ses réservations
- ✅ Annuler une réservation

### Emprunts
- ✅ Emprunter un livre (disponible ou réservé par l'utilisateur)
- ✅ Consulter ses emprunts
- ✅ Retourner un livre

### Sécurité
- ✅ Authentification JWT
- ✅ Autorisations basées sur les rôles
- ✅ Protection des routes sensibles

## 📖 Documentation

- **Backend** : Voir [Flask-backend/README.md](Flask-backend/README.md)
- **Frontend** : Voir [Angular-frontend/README.md](Angular-frontend/README.md)
- **API** : Collection Postman disponible dans le dossier `Postman/`

## 🔐 Rôles et Permissions

### Administrateur
- Accès complet à toutes les fonctionnalités
- Gestion des livres (CRUD)
- Gestion des utilisateurs
- Consultation de toutes les réservations et emprunts

### Étudiant / Enseignant
- Consultation des livres
- Réservation de livres
- Emprunt de livres
- Gestion de ses propres réservations et emprunts

## 📝 Livrables

- ✅ Base de données fonctionnelle avec MongoDB
- ✅ Interface utilisateur web intuitive et responsive
- ✅ API REST complète et documentée
- ✅ Collection Postman pour tester l'API
- ✅ Documentation complète (README)

## 🧪 Tests

### Tester l'API avec Postman

1. Importer la collection Postman depuis le dossier `Postman/`
2. Importer l'environnement Postman
3. Commencer par les endpoints d'authentification (Register/Login)
4. Le token JWT sera automatiquement sauvegardé pour les requêtes suivantes

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique.

## 👥 Auteurs

Projet réalisé dans le cadre du cours "Base de données évoluée".

---

**Note** : Assurez-vous que MongoDB est en cours d'exécution avant de démarrer les applications backend et frontend.

