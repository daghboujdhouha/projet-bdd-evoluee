from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from controllers import auth_controller, book_controller, user_controller, reservation_controller, borrow_controller

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize database connection
    db.connect()
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(auth_controller.bp, url_prefix='/api/auth')
    app.register_blueprint(book_controller.bp, url_prefix='/api/books')
    app.register_blueprint(user_controller.bp, url_prefix='/api/users')
    app.register_blueprint(reservation_controller.bp, url_prefix='/api/reservations')
    app.register_blueprint(borrow_controller.bp, url_prefix='/api/borrows')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

