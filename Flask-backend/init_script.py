"""
Script d'initialisation pour créer des utilisateurs de base, des livres français et des emprunts
S'exécute automatiquement au démarrage de l'application si la base est vide
"""
from database import db
from services.auth_service import AuthService
from services.user_service import UserService
from services.book_service import BookService
from services.borrow_service import BorrowService

def is_database_empty():
    """Vérifie si la collection users est vide"""
    try:
        collection = db.get_db()['users']
        # Décommenter pour supprimer tous les utilisateurs
        # collection.delete_many({})  
        count = collection.count_documents({})
        print(f"⚠️  La base de données contient {count} utilisateurs.")
        return count == 0
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification de la base de données: {str(e)}")
        return False

def init_users():
    """Initialise les utilisateurs de base dans la base de données si elle est vide"""
    # Initialiser la connexion à la base de données
    db.connect()
    
    # Vérifier si la base de données est vide
    if not is_database_empty():
        print("ℹ️  La base de données contient déjà des utilisateurs. Initialisation ignorée.")
        return
    
    auth_service = AuthService()
    user_service = UserService()
    
    # Liste des utilisateurs à créer
    users_to_create = [
        {
            'username': 'daghboujdhouhaa',
            'email': 'daghboujdhouhaa@gmail.com',
            'password': 'password',
            'role': 'admin'
        },
        {
            'username': 'etudiant1',
            'email': 'etudiant1@example.com',
            'password': 'password',
            'role': 'etudiant'
        },
        {
            'username': 'enseignant1',
            'email': 'enseignant1@example.com',
            'password': 'password',
            'role': 'enseignant'
        }
    ]
    
    print("🚀 Initialisation des utilisateurs de base...")
    print("-" * 50)
    
    for user_data in users_to_create:
        # Vérifier si l'utilisateur existe déjà (double vérification)
        existing_user = user_service.get_user_by_username(user_data['username'])
        if existing_user:
            print(f"⚠️  L'utilisateur '{user_data['username']}' existe déjà. Ignoré.")
            continue
        
        # Vérifier si l'email existe déjà
        existing_email = user_service.get_user_by_email(user_data['email'])
        if existing_email:
            print(f"⚠️  L'email '{user_data['email']}' est déjà utilisé. Ignoré.")
            continue
        
        # Créer l'utilisateur
        try:
            user = auth_service.register(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role']
            )
            
            if user:
                print(f"✅ Utilisateur créé : {user_data['username']} ({user_data['role']}) - {user_data['email']}")
            else:
                print(f"❌ Erreur lors de la création de l'utilisateur '{user_data['username']}'")
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'utilisateur '{user_data['username']}': {str(e)}")
    
    print("-" * 50)
    print("✨ Initialisation des utilisateurs terminée!")
    print("\n📝 Utilisateurs créés :")
    print("   - daghboujdhouhaa (admin) - daghboujdhouhaa@gmail.com - Mot de passe: password")
    print("   - etudiant1 (étudiant) - etudiant1@example.com - Mot de passe: password")
    print("   - enseignant1 (enseignant) - enseignant1@example.com - Mot de passe: password")

def is_books_collection_empty():
    """Vérifie si la collection books est vide"""
    try:
        collection = db.get_db()['books']
        count = collection.count_documents({})
        print(f"📚 La base de données contient {count} livres.")
        return count == 0
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification de la collection books: {str(e)}")
        return False

def init_books():
    """Initialise les livres français dans la base de données si la collection est vide"""
    # Vérifier si la collection books est vide
    if not is_books_collection_empty():
        print("ℹ️  La base de données contient déjà des livres. Initialisation ignorée.")
        return []
    
    book_service = BookService()
    
    # Liste des livres français à créer
    books_to_create = [
        {
            'title': 'Le Petit Prince',
            'author': 'Antoine de Saint-Exupéry',
            'genre': 'Conte philosophique',
            'year': 1943,
            'description': 'Le Petit Prince est une œuvre de langue française, la plus connue d\'Antoine de Saint-Exupéry. Publié en 1943 à New York, c\'est un conte poétique et philosophique sous l\'apparence d\'un conte pour enfants.',
            'isbn': '978-2-07-061275-8',
            'status': 'disponible'
        },
        {
            'title': 'Les Misérables',
            'author': 'Victor Hugo',
            'genre': 'Roman historique',
            'year': 1862,
            'description': 'Les Misérables est un roman de Victor Hugo publié en 1862. L\'histoire se déroule en France au début du XIXe siècle et suit la vie de Jean Valjean, un ancien forçat qui cherche la rédemption.',
            'isbn': '978-2-07-036789-5',
            'status': 'disponible'
        },
        {
            'title': 'L\'Étranger',
            'author': 'Albert Camus',
            'genre': 'Roman philosophique',
            'year': 1942,
            'description': 'L\'Étranger est un roman d\'Albert Camus, paru en 1942. Il prend place dans la tétralogie que Camus nommera « cycle de l\'absurde » qui décrit les fondements de la philosophie camusienne : l\'absurde.',
            'isbn': '978-2-07-036002-4',
            'status': 'disponible'
        },
        {
            'title': 'Madame Bovary',
            'author': 'Gustave Flaubert',
            'genre': 'Roman réaliste',
            'year': 1857,
            'description': 'Madame Bovary est un roman de Gustave Flaubert paru en 1857. Le roman retrace le parcours d\'Emma Bovary, une jeune femme qui, déçue par son mariage avec un médecin de province, cherche à échapper à l\'ennui de sa vie.',
            'isbn': '978-2-07-036131-1',
            'status': 'disponible'
        },
        {
            'title': 'Le Comte de Monte-Cristo',
            'author': 'Alexandre Dumas',
            'genre': 'Roman d\'aventure',
            'year': 1844,
            'description': 'Le Comte de Monte-Cristo est un roman d\'Alexandre Dumas, écrit avec la collaboration d\'Auguste Maquet et achevé en 1844. Il est partiellement inspiré de faits réels, très lointainement empruntés à la vie de Pierre Picaud.',
            'isbn': '978-2-253-00543-5',
            'status': 'disponible'
        },
        {
            'title': 'À la recherche du temps perdu',
            'author': 'Marcel Proust',
            'genre': 'Roman',
            'year': 1913,
            'description': 'À la recherche du temps perdu est un roman de Marcel Proust, écrit de 1906 à 1922 et publié de 1913 à 1927 en sept tomes. L\'œuvre est une réflexion majeure sur le temps et la mémoire affective.',
            'isbn': '978-2-07-010718-5',
            'status': 'disponible'
        },
        {
            'title': 'Candide',
            'author': 'Voltaire',
            'genre': 'Conte philosophique',
            'year': 1759,
            'description': 'Candide ou l\'Optimisme est un conte philosophique de Voltaire paru à Genève en janvier 1759. Il s\'agit d\'un récit de formation, récit d\'un voyage qui transformera son héros éponyme en philosophe.',
            'isbn': '978-2-07-036805-4',
            'status': 'disponible'
        },
        {
            'title': 'Les Fleurs du mal',
            'author': 'Charles Baudelaire',
            'genre': 'Poésie',
            'year': 1857,
            'description': 'Les Fleurs du mal est un recueil de poèmes de Charles Baudelaire, publié le 25 juin 1857. L\'œuvre regroupe la quasi-totalité de la production poétique de l\'auteur depuis 1840.',
            'isbn': '978-2-07-030184-6',
            'status': 'disponible'
        },
        {
            'title': 'Germinal',
            'author': 'Émile Zola',
            'genre': 'Roman naturaliste',
            'year': 1885,
            'description': 'Germinal est un roman d\'Émile Zola publié en 1885. Treizième volume de la série Les Rougon-Macquart, il raconte la grève des mineurs dans le Nord de la France à la fin du Second Empire.',
            'isbn': '978-2-07-036043-0',
            'status': 'disponible'
        },
        {
            'title': 'Le Rouge et le Noir',
            'author': 'Stendhal',
            'genre': 'Roman psychologique',
            'year': 1830,
            'description': 'Le Rouge et le Noir, sous-titré Chronique du XIXe siècle, est un roman écrit par Stendhal, publié pour la première fois à Paris en novembre 1830. Il retrace le parcours de Julien Sorel, un jeune homme ambitieux.',
            'isbn': '978-2-07-036001-0',
            'status': 'disponible'
        }
    ]
    
    print("\n📚 Initialisation des livres français...")
    print("-" * 50)
    
    created_books = []
    for book_data in books_to_create:
        # Vérifier si le livre existe déjà (par ISBN)
        existing_books = book_service.get_all_books({'isbn': book_data['isbn']})
        if existing_books:
            print(f"⚠️  Le livre '{book_data['title']}' existe déjà. Ignoré.")
            created_books.append(existing_books[0])
            continue
        
        # Créer le livre
        try:
            book = book_service.create_book(book_data)
            if book:
                print(f"✅ Livre créé : {book_data['title']} - {book_data['author']} ({book_data['year']})")
                created_books.append(book)
            else:
                print(f"❌ Erreur lors de la création du livre '{book_data['title']}'")
        except Exception as e:
            print(f"❌ Erreur lors de la création du livre '{book_data['title']}': {str(e)}")
    
    print("-" * 50)
    print(f"✨ Initialisation des livres terminée! {len(created_books)} livre(s) créé(s).")
    
    return created_books

def init_borrows():
    """Crée des emprunts sur les livres disponibles"""
    user_service = UserService()
    book_service = BookService()
    borrow_service = BorrowService()
    
    # Vérifier si des emprunts existent déjà
    existing_borrows = borrow_service.get_all_borrows()
    if existing_borrows:
        print("\n📖 Des emprunts existent déjà dans la base de données. Création d'emprunts ignorée.")
        return
    
    # Récupérer les utilisateurs
    etudiant = user_service.get_user_by_username('etudiant1')
    enseignant = user_service.get_user_by_username('enseignant1')
    
    if not etudiant or not enseignant:
        print("⚠️  Impossible de créer des emprunts : utilisateurs non trouvés.")
        return
    
    # Récupérer tous les livres disponibles
    all_books = book_service.get_all_books({'status': 'disponible'})
    
    if not all_books or len(all_books) < 4:
        print("⚠️  Pas assez de livres disponibles pour créer des emprunts (minimum 4 requis).")
        return
    
    print("\n📖 Création des emprunts...")
    print("-" * 50)
    
    # Créer quelques emprunts sur les 4 premiers livres disponibles
    borrows_to_create = [
        {'user': etudiant, 'book': all_books[0]},  # Premier livre pour l'étudiant
        {'user': etudiant, 'book': all_books[1]},  # Deuxième livre pour l'étudiant
        {'user': enseignant, 'book': all_books[2]},  # Troisième livre pour l'enseignant
        {'user': enseignant, 'book': all_books[3]},  # Quatrième livre pour l'enseignant
    ]
    
    created_borrows = 0
    for borrow_data in borrows_to_create:
        book = borrow_data['book']
        user = borrow_data['user']
        
        # Vérifier si le livre est toujours disponible
        current_book = book_service.get_book_by_id(book._id)
        if not current_book or current_book.status != 'disponible':
            print(f"⚠️  Le livre '{book.title}' n'est plus disponible. Ignoré.")
            continue
        
        # Vérifier si l'utilisateur a déjà un emprunt actif sur ce livre
        user_borrows = borrow_service.get_borrows_by_user(user._id)
        existing_borrow = next(
            (b for b in user_borrows if b.book_id == book._id and b.status == 'active'),
            None
        )
        if existing_borrow:
            print(f"⚠️  L'utilisateur '{user.username}' a déjà emprunté '{book.title}'. Ignoré.")
            continue
        
        # Créer l'emprunt
        try:
            borrow = borrow_service.create_borrow(user._id, book._id)
            if borrow:
                print(f"✅ Emprunt créé : {user.username} a emprunté '{book.title}'")
                created_borrows += 1
            else:
                print(f"❌ Erreur lors de la création de l'emprunt pour '{book.title}'")
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'emprunt : {str(e)}")
    
    print("-" * 50)
    if created_borrows > 0:
        print(f"✨ Création des emprunts terminée! {created_borrows} emprunt(s) créé(s).")
    else:
        print("ℹ️  Aucun nouvel emprunt créé.")

def init_all():
    """Initialise tous les éléments : utilisateurs, livres et emprunts"""
    print("=" * 50)
    print("🚀 DÉMARRAGE DE L'INITIALISATION")
    print("=" * 50)
    
    # Initialiser les utilisateurs
    init_users()
    
    # Initialiser les livres
    init_books()
    
    # Initialiser les emprunts (vérifie automatiquement la disponibilité)
    init_borrows()
    
    print("\n" + "=" * 50)
    print("✨ INITIALISATION COMPLÈTE TERMINÉE!")
    print("=" * 50)

if __name__ == '__main__':
    init_all()

