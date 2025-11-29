from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.book_service import BookService
from middleware.auth_middleware import require_role
from datetime import datetime

bp = Blueprint('books', __name__)
book_service = BookService()

def serialize_book(book):
    """Sérialise un livre pour la réponse JSON"""
    return {
        'id': book._id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year': book.year,
        'description': book.description,
        'isbn': book.isbn,
        'status': book.status,
        'created_at': book.created_at.isoformat() if book.created_at else None,
        'updated_at': book.updated_at.isoformat() if book.updated_at else None
    }

@bp.route('', methods=['GET'])
@jwt_required()
def get_books():
    """Récupère tous les livres avec filtres optionnels"""
    filters = {}
    
    if request.args.get('title'):
        filters['title'] = request.args.get('title')
    if request.args.get('author'):
        filters['author'] = request.args.get('author')
    if request.args.get('genre'):
        filters['genre'] = request.args.get('genre')
    if request.args.get('year'):
        filters['year'] = request.args.get('year')
    if request.args.get('isbn'):
        filters['isbn'] = request.args.get('isbn')
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    
    books = book_service.get_all_books(filters)
    return jsonify([serialize_book(book) for book in books]), 200

@bp.route('/<book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    """Récupère un livre par son ID"""
    book = book_service.get_book_by_id(book_id)
    
    if not book:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify(serialize_book(book)), 200

@bp.route('', methods=['POST'])
@require_role('admin')
def create_book():
    """Crée un nouveau livre (admin seulement)"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['title', 'author', 'genre', 'year', 'description', 'isbn']):
        return jsonify({'error': 'Données manquantes'}), 400
    
    book_data = {
        'title': data['title'],
        'author': data['author'],
        'genre': data['genre'],
        'year': int(data['year']),
        'description': data['description'],
        'isbn': data['isbn'],
        'status': data.get('status', 'disponible')
    }
    
    book = book_service.create_book(book_data)
    return jsonify(serialize_book(book)), 201

@bp.route('/<book_id>', methods=['PUT'])
@require_role('admin')
def update_book(book_id):
    """Met à jour un livre (admin seulement)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    update_data = {}
    allowed_fields = ['title', 'author', 'genre', 'year', 'description', 'isbn', 'status']
    
    for field in allowed_fields:
        if field in data:
            if field == 'year':
                update_data[field] = int(data[field])
            else:
                update_data[field] = data[field]
    
    book = book_service.update_book(book_id, update_data)
    
    if not book:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify(serialize_book(book)), 200

@bp.route('/<book_id>', methods=['DELETE'])
@require_role('admin')
def delete_book(book_id):
    """Supprime un livre (admin seulement)"""
    success = book_service.delete_book(book_id)
    
    if not success:
        return jsonify({'error': 'Livre non trouvé'}), 404
    
    return jsonify({'message': 'Livre supprimé avec succès'}), 200

