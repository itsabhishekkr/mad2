from flask import jsonify, current_app
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from backend.models import db, User, Customer, Professional, Role, Service, CustomerReview, ServiceRequest, roles_users
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

## block and unblock customer by admin
class AdminBlockCustomer(Resource):
    @jwt_required()
    def put(self, customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "Customer not found"}, 404

            customer.is_active = False
            db.session.commit()
            return {"message": "Customer blocked successfully"}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500

class AdminUnblockCustomer(Resource):
    @jwt_required()
    def put(self, customer_id):
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "Customer not found"}, 404

            customer.is_active = True
            db.session.commit()
            return {"message": "Customer unblocked successfully"}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

