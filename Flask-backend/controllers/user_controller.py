from flask import Blueprint, request, jsonify
from services.user_service import UserService
from middleware.auth_middleware import require_role

bp = Blueprint('users', __name__)
user_service = UserService()

def serialize_user(user):
    """Sérialise un utilisateur pour la réponse JSON"""
    return {
        'id': user._id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'updated_at': user.updated_at.isoformat() if user.updated_at else None
    }

@bp.route('', methods=['GET'])
@require_role('admin')
def get_users():
    """Récupère tous les utilisateurs (admin seulement)"""
    users = user_service.get_all_users()
    return jsonify([serialize_user(user) for user in users]), 200

@bp.route('/<user_id>', methods=['GET'])
@require_role('admin')
def get_user(user_id):
    """Récupère un utilisateur par son ID (admin seulement)"""
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify(serialize_user(user)), 200

@bp.route('/<user_id>', methods=['PUT'])
@require_role('admin')
def update_user(user_id):
    """Met à jour un utilisateur (admin seulement)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400
    
    update_data = {}
    allowed_fields = ['username', 'email', 'role']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    user = user_service.update_user(user_id, update_data)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify(serialize_user(user)), 200

@bp.route('/<user_id>', methods=['DELETE'])
@require_role('admin')
def delete_user(user_id):
    """Supprime un utilisateur (admin seulement)"""
    success = user_service.delete_user(user_id)
    
    if not success:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200

