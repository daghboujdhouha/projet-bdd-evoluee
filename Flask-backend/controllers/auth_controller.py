from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import AuthService
from services.user_service import UserService

bp = Blueprint('auth', __name__)
auth_service = AuthService()
user_service = UserService()

@bp.route('/register', methods=['POST'])
def register():
    """Enregistre un nouvel utilisateur"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Données manquantes'}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    role = data.get('role', 'etudiant')
    
    # Vérifier que le rôle est valide
    if role not in ['admin', 'etudiant', 'enseignant']:
        return jsonify({'error': 'Rôle invalide'}), 400
    
    user = auth_service.register(username, email, password, role)
    
    if not user:
        return jsonify({'error': 'Nom d\'utilisateur ou email déjà utilisé'}), 400
    
    access_token = create_access_token(identity=user._id)
    
    return jsonify({
        'message': 'Utilisateur créé avec succès',
        'access_token': access_token,
        'user': {
            'id': user._id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Authentifie un utilisateur"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Nom d\'utilisateur et mot de passe requis'}), 400
    
    username = data['username']
    password = data['password']
    
    user = auth_service.login(username, password)
    
    if not user:
        return jsonify({'error': 'Identifiants invalides'}), 401
    
    access_token = create_access_token(identity=user._id)
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user._id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Récupère l'utilisateur actuel"""
    user_id = get_jwt_identity()
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify({
        'id': user._id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200

