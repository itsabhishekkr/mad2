from flask import Flask, request, jsonify, render_template
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from backend.models import *
from backend.db import db
from backend.resources import api

# Configuration
class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abhishek"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'thissecret'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 3600
    JWT_SECRET_KEY = "your_jwt_secret_key"  # Add JWT secret key
    UPLOAD_FOLDER = 'uploads'  # Add upload folder configuration

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379
    WTF_CSRF_ENABLED = False

# Data Seeding Function
def seed_data(app):
    with app.app_context():
        # Initialize Flask-Security datastore
        datastore = SQLAlchemyUserDatastore(db, User, Role)

        # Create roles
        admin_role = datastore.find_or_create_role(name='admin', description='Superuser')
        customer_role = datastore.find_or_create_role(name='customer', description='Customer user')
        professional_role = datastore.find_or_create_role(name='professional', description='Professional user')

        # Check if admin user already exists
        if not datastore.find_user(email='admin@gmail.com'):
            admin_user = datastore.create_user(
                email='admin@gmail.com',
                roles=[admin_role],
                active=True  # Set active to True
            )
            admin_user.set_password('adminpassword')  # Use set_password to set the password
            db.session.commit()
            print("Admin user created: admin@gmail.com / adminpassword")

        # Commit all changes
        db.session.commit()
        print("Database seeding complete.")

# App Setup
def create_app():
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')
    app.config.from_object(LocalDevelopmentConfig)

    # Initialize the database
    db.init_app(app)

    # Initialize flask-restful
    api.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore=datastore, register_blueprint=False)

    # Initialize JWT
    jwt = JWTManager(app)

    # Add CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    with app.app_context():
        # Create all database tables
        db.create_all()

        # Seed initial data
        seed_data(app)

    return app

app = create_app()

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5001)