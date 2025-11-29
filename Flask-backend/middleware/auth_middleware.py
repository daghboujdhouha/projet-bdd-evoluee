from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from services.user_service import UserService

def require_auth(f):
    """Décorateur pour exiger une authentification"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def require_role(*allowed_roles):
    """Décorateur pour exiger un rôle spécifique"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user_service = UserService()
                user = user_service.get_user_by_id(user_id)
                
                if not user:
                    return jsonify({'error': 'Utilisateur non trouvé'}), 404
                
                if user.role not in allowed_roles:
                    return jsonify({'error': 'Accès refusé'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': str(e)}), 401
        return decorated_function
    return decorator

