from flask import jsonify, current_app
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from backend.models import db, User, Customer, Professional, Role, Service, CustomerReview, ServiceRequest, roles_users
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime

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
        

### full customer api 
class CustomerBookServiceAPI(Resource):
    @jwt_required()
    def post(self, service_id):
        try:
            current_user = get_jwt_identity()

            # Check if the user is a customer
            user = User.query.get(current_user)
            if not user or not any(role.name == "customer" for role in user.roles):
                return {"error": "Unauthorized access."}, 403

            # Get the service (returns 404 automatically if not found)
            service = Service.query.get_or_404(service_id)

            # Get the customer
            customer = Customer.query.filter_by(user_id=user.id).first()
            if not customer:
                return {"error": "Customer not found."}, 404

            # Create a new service request
            new_request = ServiceRequest(
                service_id=service.id,
                customer_id=customer.id,
                service_status='requested'
            )
            db.session.add(new_request)
            db.session.commit()

            return {"message": "Service requested successfully."}, 201

        except SQLAlchemyError as e:
            db.session.rollback()  # Ensure rollback on any DB error
            return {"error": f"Database error: {str(e)}"}, 500

        except Exception as e:
            db.session.rollback()  # Rollback on unexpected errors too
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
        


class CustomerBookHistoryAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            print("user id:", current_user)

            # Check if the user is a customer
            user = User.query.get(current_user)
            if not user or not any(role.name == "customer" for role in user.roles):
                return {"error": "Unauthorized access."}, 403

            # Get the customer
            customer = Customer.query.filter_by(user_id=user.id).first()
            if not customer:
                return {"error": "Customer not found."}, 404

            # Fetch all service bookings for the customer
            all_bookings = ServiceRequest.query.filter_by(customer_id=customer.id).all()

            bookings = []
            for booking in all_bookings:
                service = Service.query.get(booking.service_id)
                professional = Professional.query.get(booking.professional_id) if booking.professional_id else None
                user = professional.user if professional else None

                # Convert datetime to string if they exist
                date_of_request = booking.date_of_request.strftime('%Y-%m-%d %H:%M:%S') if booking.date_of_request else None
                date_of_completion = booking.date_of_completion.strftime('%Y-%m-%d %H:%M:%S') if booking.date_of_completion else None

                bookings.append({
                    "service_name": service.name if service else "Unknown",
                    "service_description": service.description if service else "N/A",
                    "status": booking.service_status,
                    "date_of_request": date_of_request,
                    "date_of_completion": date_of_completion,
                    "professional_name": professional.fullname if professional else "Not Assigned",
                    "professional_email": user.email if user else "N/A"
                })
            return {"bookings": bookings}, 200
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500



        

