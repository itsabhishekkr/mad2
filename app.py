from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_security.decorators import auth_required
from backend.models import *  # Import models here
from backend.db import db  # Import db object here

# Configuration
class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abhishek"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'thissecret'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 3600

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

        # Create admin user
        if not datastore.find_user(email='admin@example.com'):
            admin_user = datastore.create_user(
                email='admin@example.com',
                roles=[admin_role]
            )
            admin_user.set_password('adminpassword')  # Use set_password to set the password
            db.session.commit()
            print("Admin user created: admin@example.com / adminpassword")

        # Commit all changes
        db.session.commit()
        print("Database seeding complete.")

# App Setup
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    # Initialize the database
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, datastore=datastore)

    with app.app_context():
        # Create all database tables
        db.create_all()

        # Seed initial data
        seed_data(app)

    return app

app = create_app()

# Routes
@app.get('/')
def index():
    return 'Hello World'

@app.get('/protected')
@auth_required()
def protected():
    return 'Protected'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

