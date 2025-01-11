from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt

db = SQLAlchemy()

# Association table for many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', secondary=roles_users, back_populates='roles')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, back_populates='users')
    customers = db.relationship('Customer', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    professionals = db.relationship('Professional', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(6), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    customer_reviews = db.relationship('CustomerReview', backref='customer', lazy='dynamic', cascade='all, delete-orphan')


class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    available_services = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.Integer, nullable=False)
    documents = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(6), nullable=False, index=True)
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    professional_reviews = db.relationship('CustomerReview', backref='professional', lazy='dynamic', cascade='all, delete-orphan')
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy='dynamic', cascade='all, delete-orphan')


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    is_approved = db.Column(db.Boolean, default=True)
    service_requests = db.relationship('ServiceRequest', backref='service', lazy='dynamic', cascade='all, delete-orphan')


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id', ondelete='CASCADE'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), nullable=False, default="Pending")
    remarks = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: dt.datetime.now(dt.timezone.utc), onupdate=lambda: dt.datetime.now(dt.timezone.utc))


class CustomerReview(db.Model):
    __tablename__ = 'customer_review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id', ondelete='CASCADE'), nullable=False)
    review_text = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))
