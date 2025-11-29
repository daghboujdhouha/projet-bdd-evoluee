from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.reservation_service import ReservationService
from middleware.auth_middleware import require_role

bp = Blueprint('reservations', __name__)
reservation_service = ReservationService()

def serialize_reservation(reservation):
    """Sérialise une réservation pour la réponse JSON"""
    return {
        'id': reservation._id,
        'user_id': reservation.user_id,
        'book_id': reservation.book_id,
        'reservation_date': reservation.reservation_date.isoformat() if reservation.reservation_date else None,
        'expiry_date': reservation.expiry_date.isoformat() if reservation.expiry_date else None,
        'status': reservation.status,
        'created_at': reservation.created_at.isoformat() if reservation.created_at else None,
        'updated_at': reservation.updated_at.isoformat() if reservation.updated_at else None
    }

@bp.route('', methods=['POST'])
@jwt_required()
def create_reservation():
    """Crée une nouvelle réservation"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or 'book_id' not in data:
        return jsonify({'error': 'book_id requis'}), 400
    
    book_id = data['book_id']
    reservation = reservation_service.create_reservation(user_id, book_id)
    
    if not reservation:
        return jsonify({'error': 'Impossible de créer la réservation. Le livre n\'est peut-être pas disponible.'}), 400
    
    return jsonify(serialize_reservation(reservation)), 201

@bp.route('', methods=['GET'])
@jwt_required()
def get_reservations():
    """Récupère les réservations de l'utilisateur connecté ou toutes (admin)"""
    user_id = get_jwt_identity()
    
    # Vérifier si l'utilisateur est admin
    from services.user_service import UserService
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    
    if user and user.role == 'admin':
        reservations = reservation_service.get_all_reservations()
    else:
        reservations = reservation_service.get_reservations_by_user(user_id)
    
    return jsonify([serialize_reservation(res) for res in reservations]), 200

@bp.route('/<reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    """Récupère une réservation par son ID"""
    reservation = reservation_service.get_reservation_by_id(reservation_id)
    
    if not reservation:
        return jsonify({'error': 'Réservation non trouvée'}), 404
    
    # Vérifier que l'utilisateur a accès à cette réservation
    user_id = get_jwt_identity()
    from services.user_service import UserService
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)
    
    if user.role != 'admin' and reservation.user_id != user_id:
        return jsonify({'error': 'Accès refusé'}), 403
    
    return jsonify(serialize_reservation(reservation)), 200

@bp.route('/<reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    """Annule une réservation"""
    user_id = get_jwt_identity()
    success = reservation_service.cancel_reservation(reservation_id, user_id)
    
    if not success:
        return jsonify({'error': 'Impossible d\'annuler la réservation'}), 400
    
    return jsonify({'message': 'Réservation annulée avec succès'}), 200

