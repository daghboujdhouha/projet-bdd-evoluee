from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.borrow_service import BorrowService
from middleware.auth_middleware import require_role

bp = Blueprint('borrows', __name__)
borrow_service = BorrowService()

def serialize_borrow(borrow):
    """Sérialise un emprunt pour la réponse JSON"""
    return {
        'id': borrow._id,
        'user_id': borrow.user_id,
        'book_id': borrow.book_id,
        'borrow_date': borrow.borrow_date.isoformat() if borrow.borrow_date else None,
        'return_date': borrow.return_date.isoformat() if borrow.return_date else None,
        'due_date': borrow.due_date.isoformat() if borrow.due_date else None,
        'status': borrow.status,
        'created_at': borrow.created_at.isoformat() if borrow.created_at else None,
        'updated_at': borrow.updated_at.isoformat() if borrow.updated_at else None
    }

@bp.route('', methods=['POST'])
@jwt_required()
def create_borrow():
    """Crée un nouvel emprunt"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or 'book_id' not in data:
        return jsonify({'error': 'book_id requis'}), 400
    
    book_id = data['book_id']
    borrow = borrow_service.create_borrow(user_id, book_id)
    
    if not borrow:
        return jsonify({'error': 'Impossible de créer l\'emprunt. Le livre n\'est peut-être pas disponible.'}), 400
    
    return jsonify(serialize_borrow(borrow)), 201

@bp.route('', methods=['GET'])
@jwt_required()
def get_borrows():
    """Récupère les emprunts de l'utilisateur connecté ou tous (admin)"""
    user_id = get_jwt_identity()
    
    # Vérifier si l'utilisateur est admin
    from services.user_service import UserService
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    
    if user and user.role == 'admin':
        borrows = borrow_service.get_all_borrows()
    else:
        borrows = borrow_service.get_borrows_by_user(user_id)
    
    return jsonify([serialize_borrow(borrow) for borrow in borrows]), 200

@bp.route('/<borrow_id>', methods=['GET'])
@jwt_required()
def get_borrow(borrow_id):
    """Récupère un emprunt par son ID"""
    borrow = borrow_service.get_borrow_by_id(borrow_id)
    
    if not borrow:
        return jsonify({'error': 'Emprunt non trouvé'}), 404
    
    # Vérifier que l'utilisateur a accès à cet emprunt
    user_id = get_jwt_identity()
    from services.user_service import UserService
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    
    if user.role != 'admin' and borrow.user_id != user_id:
        return jsonify({'error': 'Accès refusé'}), 403
    
    return jsonify(serialize_borrow(borrow)), 200

@bp.route('/<borrow_id>/return', methods=['POST'])
@jwt_required()
def return_book(borrow_id):
    """Retourne un livre emprunté"""
    user_id = get_jwt_identity()
    
    # Vérifier si l'utilisateur est admin
    from services.user_service import UserService
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    is_admin = user and user.role == 'admin'
    
    # Valider l'ID
    from bson import ObjectId
    try:
        ObjectId(borrow_id)
    except:
        return jsonify({'error': 'ID d\'emprunt invalide'}), 400
    
    # Vérifier que l'emprunt existe
    borrow = borrow_service.get_borrow_by_id(borrow_id)
    if not borrow:
        return jsonify({'error': 'Emprunt non trouvé'}), 404
    
    # Vérifier les permissions
    if not is_admin and borrow.user_id != user_id:
        return jsonify({'error': 'Vous n\'avez pas la permission de retourner ce livre'}), 403
    
    # Vérifier que l'emprunt est actif
    if borrow.status != 'active':
        return jsonify({'error': f'Cet emprunt est déjà retourné (statut: {borrow.status})'}), 400
    
    success = borrow_service.return_book(borrow_id, user_id, is_admin)
    
    if not success:
        return jsonify({'error': 'Impossible de retourner le livre'}), 400
    
    return jsonify({'message': 'Livre retourné avec succès'}), 200

