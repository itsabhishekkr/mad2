from flask import jsonify, current_app
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from backend.models import db, User, Customer, Professional, Role, Service, CustomerReview
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

###----------------------------sevices api---------------------------------###

class AdminAddServiceAPI(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Parse request JSON data
            data = request.get_json()
            name = data.get('name').strip().lower()
            description = data.get('description')
            price = data.get('price')
            time_required = data.get('time_required')

            # Create a new service
            new_service = Service(
                name=name,
                description=description,
                price=price,
                time_required=time_required
            )
            db.session.add(new_service)
            db.session.commit()

            return {"message": "Service added successfully."}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

class AdminUpdateServiceAPI(Resource):
    @jwt_required()
    def put(self, service_id):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Parse request JSON data
            data = request.get_json()
            name = data.get('name').strip().lower()
            description = data.get('description')
            price = data.get('price')
            time_required = data.get('time_required')

            # Find the service by ID
            service = Service.query.get(service_id)
            if not service:
                return {"error": "Service not found."}, 404

            # Update the service
            service.name = name
            service.description = description
            service.price = price
            service.time_required = time_required
            db.session.commit()

            return {"message": "Service updated successfully."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

class AdminDeleteServiceAPI(Resource):
    @jwt_required()
    def delete(self, service_id):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Find the service by ID
            service = Service.query.get(service_id)
            if not service:
                return {"error": "Service not found."}, 404

            # Delete the service
            db.session.delete(service)
            db.session.commit()

            return {"message": "Service deleted successfully."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        
class AllAdminServiceAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve all services
            services = Service.query.all()
            service_list = []
            for service in services:
                service_data = {
                    "id": service.id,
                    "name": service.name,
                    "description": service.description,
                    "price": service.price,
                    "time_required": service.time_required,
                    "created_at": service.created_at.isoformat(),  # Convert datetime to string
                    "is_approved": service.is_approved
                }
                service_list.append(service_data)

            return {"services": service_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

class AdminServiceSummaryAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Count approved and unapproved services
            approved_count = db.session.query(func.count(Service.id)).filter_by(is_approved=True).scalar()
            unapproved_count = db.session.query(func.count(Service.id)).filter_by(is_approved=False).scalar()

            # Calculate total money for approved and unapproved services
            approved_total_money = db.session.query(func.sum(Service.price)).filter_by(is_approved=True).scalar() or 0
            unapproved_total_money = db.session.query(func.sum(Service.price)).filter_by(is_approved=False).scalar() or 0

            summary = {
                "approved_count": approved_count,
                "unapproved_count": unapproved_count,
                "approved_total_money": approved_total_money,
                "unapproved_total_money": unapproved_total_money
            }

            return {"summary": summary}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        
class AdminServiceSearchAPI(Resource):
    @jwt_required()
    def get(self, search_term):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve and process the search term
            search_term = search_term.strip().lower()

            # Build the query
            query = Service.query.filter(
                (Service.name.ilike(f'%{search_term}%')) |
                (Service.price.ilike(f'%{search_term}%')) |
                (Service.description.ilike(f'%{search_term}%')) |
                (Service.is_approved.ilike(f'%{search_term}%')) |
                (Service.time_required.ilike(f'%{search_term}%'))
            )

            services = query.all()

            service_list = []
            for service in services:
                service_data = {
                    "id": service.id,
                    "name": service.name,
                    "description": service.description,
                    "price": service.price,
                    "time_required": service.time_required,
                    "created_at": service.created_at.isoformat(),  # Convert datetime to string
                    "is_approved": service.is_approved
                }
                service_list.append(service_data)

            return {"services": service_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        


###----------------------------professional api by admin ---------------------------------###


class AdminProfessionalDetailsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve professionals and their associated users
            professionals = db.session.query(Professional, User)\
                .join(User, Professional.user_id == User.id)\
                .all()

            # Retrieve average ratings for professionals
            reviews = db.session.query(CustomerReview.professional_id, 
                                        db.func.round(db.func.avg(CustomerReview.rating), 2).label('average_rating'))\
                .group_by(CustomerReview.professional_id).all()
            
            avg_ratings = {review.professional_id: review.average_rating for review in reviews}

            professional_list = []
            for professional, user in professionals:
                professional_data = {
                    "professional_id": professional.id,
                    "fullname": professional.fullname,
                    "available_services": professional.available_services,
                    "email": user.email,
                    "pincode": professional.pincode,
                    "is_approved": professional.is_approved,
                    "average_rating": avg_ratings.get(professional.id, None)
                }
                professional_list.append(professional_data)

            return {"professionals": professional_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

### ------------------------------- admin block or unblock professional -----------------------------###

#### check check

class AdminBlockUnblockProfessionalAPI(Resource):
    @jwt_required()
    def put(self, professional_id):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Parse request JSON data
            data = request.get_json()
            is_approved = data.get('is_approved')

            # Find the professional by ID
            professional = Professional.query.get(professional_id)
            if not professional:
                return {"error": "Professional not found."}, 404

            # Update the is_approved status
            professional.is_approved = is_approved
            db.session.commit()

            return {"message": "Professional status updated successfully."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500