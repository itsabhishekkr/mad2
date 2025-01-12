from flask import Flask, request, jsonify
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_security.decorators import auth_required
from backend.models import *  # Import models here
from backend.db import db  # Import db object here
from werkzeug.security import check_password_hash



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
    security = Security(app, datastore=datastore, register_blueprint=False)

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

@app.route('/login', methods=['POST'])
def login():
    # Parse JSON request data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate email and password
    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    # Query user by email
    user = User.query.filter_by(email=email).first()

    # Check user existence and password
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password.'}), 401

    # Check if user account is active
    if not user.active:
        return jsonify({'message': 'Your account is blocked.'}), 403

    # Check roles and additional conditions
    roles = [role.name for role in user.roles]

    if 'customer' in roles:
        # Check if the customer is active and approved
        customer = Customer.query.filter_by(user_id=user.id).first()
        if customer and not customer.is_active:
            return jsonify({'message': 'Your account is inactive.'}), 403
        if customer and not customer.is_approved:
            return jsonify({'message': 'Your account is not approved.'}), 403
        return jsonify({'message': 'Login successful.', 'user_id': user.id, 'role': 'customer'}), 200

    elif 'professional' in roles:
        # Check if professional is active and approved
        professional = Professional.query.filter_by(user_id=user.id).first()
        if professional and not professional.is_active:
            return jsonify({'message': 'Your account is inactive.'}), 403
        if professional and not professional.is_approved:
            return jsonify({'message': 'Your account is not approved.'}), 403
        return jsonify({'message': 'Login successful.', 'user_id': user.id, 'role': 'professional'}), 200

    elif 'admin' in roles:
        return jsonify({'message': 'Login successful.', 'user_id': user.id, 'role': 'admin'}), 200

    # Default response if no role matches
    return jsonify({'message': 'No valid role assigned to user.'}), 403



@app.route('/register/customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    address = data.get('address')
    pincode = data.get('pincode')

    # Check if required fields are provided
    if not all([email, password, fullname, address, pincode]):
        return jsonify({'message': 'All fields are required.'}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already exists.'}), 400

    # Determine role
    users = User.query.all()
    role_name = 'admin' if len(users) == 0 else 'customer'
    role = Role.query.filter_by(name=role_name).first()

    # Create new user
    user = User(email=email, active=True)
    user.set_password(password)
    user.roles.append(role)

    try:
        db.session.add(user)
        db.session.commit()

        # If role is customer, create customer record
        if role_name == 'customer':
            customer = Customer(fullname=fullname, address=address, pincode=pincode, user_id=user.id)
            db.session.add(customer)
            db.session.commit()

        return jsonify({'message': 'Registration successful.', 'role': role_name}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed. Please try again.', 'error': str(e)}), 500
    
    


# Run the application
if __name__ == '__main__':
    app.run(debug=True)

