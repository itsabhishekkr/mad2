from flask import jsonify, current_app
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from backend.models import db, User, Customer, Professional, Role, Service, CustomerReview, ServiceRequest, roles_users
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
        # if not user or 'admin' or 'customer' not in [role.name for role in user.roles]:
        #     return {"error": "Unauthorized access."}, 403

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
        

class AdminProfessionalSummaryAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Count total, approved, and pending professionals
            total_professionals = Professional.query.count()
            approved_professionals = Professional.query.filter_by(is_approved=True).count()
            pending_professionals = Professional.query.filter_by(is_approved=False).count()

            # Calculate average ratings for professionals
            avg_ratings = (
                db.session.query(
                    CustomerReview.professional_id, func.avg(CustomerReview.rating)
                )
                .group_by(CustomerReview.professional_id)
                .all()
            )
            avg_ratings_dict = {prof_id: round(rating, 2) for prof_id, rating in avg_ratings}

            summary = {
                "total_professionals": total_professionals,
                "approved_professionals": approved_professionals,
                "pending_professionals": pending_professionals,
                "avg_ratings": avg_ratings_dict,
            }

            return {"summary": summary}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500


class AdminProfessionalSearchAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve query parameters
            fullname_query = request.args.get('fullname', '').strip().lower()
            email_query = request.args.get('email', '').strip().lower()
            services_query = request.args.get('services', '').strip().lower()
            experience_query = request.args.get('experience', '').strip().lower()
            is_approved_query = request.args.get('is_approved', '').strip().lower()
            avg_rating_query = request.args.get('avg_rating', '').strip().lower()

            # Build the query
            query = db.session.query(Professional, User).join(User, Professional.user_id == User.id)

            if fullname_query:
                query = query.filter(User.name.ilike(f'%{fullname_query}%'))
            if email_query:
                query = query.filter(User.email.ilike(f'%{email_query}%'))
            if services_query:
                query = query.join(Service).filter(Service.name.ilike(f'%{services_query}%'))
            if experience_query:
                query = query.filter(Professional.experience.ilike(f'%{experience_query}%'))
            if is_approved_query:
                query = query.filter(Professional.is_approved == (is_approved_query.lower() == 'true'))
            if avg_rating_query:
                avg_ratings = (
                    db.session.query(
                        CustomerReview.professional_id, func.avg(CustomerReview.rating).label('average_rating')
                    )
                    .group_by(CustomerReview.professional_id)
                    .having(func.avg(CustomerReview.rating) >= float(avg_rating_query))
                    .all()
                )
                avg_rating_ids = [rating.professional_id for rating in avg_ratings]
                query = query.filter(Professional.id.in_(avg_rating_ids))

            professionals = query.all()

            professional_list = []
            for professional, user in professionals:
                professional_data = {
                    "professional_id": professional.id,
                    "user_id": user.id,
                    "fullname": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "address": professional.address,
                    "pincode": professional.pincode,
                    "is_approved": professional.is_approved,
                    "experience": professional.experience,
                    "average_rating": avg_ratings.get(professional.id, None)
                }
                professional_list.append(professional_data)

            return {"professionals": professional_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        

class AdminProfessionalSearchAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve query parameters
            search_term = request.args.get('search_term', '').strip().lower()
            fullname_query = request.args.get('fullname', '').strip().lower()
            email_query = request.args.get('email', '').strip().lower()
            services_query = request.args.get('services', '').strip().lower()
            experience_query = request.args.get('experience', '').strip().lower()
            is_approved_query = request.args.get('is_approved', '').strip().lower()
            avg_rating_query = request.args.get('avg_rating', '').strip().lower()

            # Build the query
            query = db.session.query(Professional, User).join(User, Professional.user_id == User.id)

            # General search term
            if search_term:
                query = query.filter(
                    (Professional.fullname.ilike(f'%{search_term}%')) |
                    (User.email.ilike(f'%{search_term}%')) |
                    (Professional.address.ilike(f'%{search_term}%')) |
                    (Professional.pincode.ilike(f'%{search_term}%'))
                )

            # Specific filters
            if fullname_query:
                query = query.filter(Professional.fullname.ilike(f'%{fullname_query}%'))
            if email_query:
                query = query.filter(User.email.ilike(f'%{email_query}%'))
            if services_query:
                query = query.join(Service).filter(Service.name.ilike(f'%{services_query}%'))
            if experience_query:
                query = query.filter(Professional.experience.ilike(f'%{experience_query}%'))
            if is_approved_query:
                query = query.filter(Professional.is_approved == (is_approved_query.lower() == 'true'))
            if avg_rating_query:
                avg_ratings = (
                    db.session.query(
                        CustomerReview.professional_id, func.avg(CustomerReview.rating).label('average_rating')
                    )
                    .group_by(CustomerReview.professional_id)
                    .having(func.avg(CustomerReview.rating) >= float(avg_rating_query))
                    .all()
                )
                avg_rating_ids = [rating.professional_id for rating in avg_ratings]
                query = query.filter(Professional.id.in_(avg_rating_ids))

            professionals = query.all()

            professional_list = []
            avg_rating_map = {rating.professional_id: rating.average_rating for rating in avg_ratings} if avg_rating_query else {}
            for professional, user in professionals:
                professional_data = {
                    "professional_id": professional.id,
                    "user_id": user.id,
                    "fullname": professional.fullname,
                    "email": user.email,
                    "address": professional.address,
                    "pincode": professional.pincode,
                    "is_approved": professional.is_approved,
                    "experience": professional.experience,
                    "average_rating": avg_rating_map.get(professional.id, None)
                }
                professional_list.append(professional_data)

            return {"professionals": professional_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500


class AdminCustomerDetailsAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve all customers and their associated users
            customers = db.session.query(Customer, User).join(User, Customer.user_id == User.id).all()

            customer_list = []
            for customer, user in customers:
                customer_data = {
                    "customer_id": customer.id,
                    "user_id": user.id,
                    "fullname": customer.fullname,
                    "email": user.email,
                    "address": customer.address,
                    "pincode": customer.pincode,
                    "is_active": customer.is_active
                }
                customer_list.append(customer_data)

            return {"customers": customer_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        
class AdminCustomerSummaryAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Count total, active, and inactive customers
            total_customers = Customer.query.count()
            active_customers = Customer.query.filter_by(is_active=True).count()
            inactive_customers = Customer.query.filter_by(is_active=False).count()

            summary = {
                "total_customers": total_customers,
                "active_customers": active_customers,
                "inactive_customers": inactive_customers
            }

            return {"summary": summary}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500


class AdminBlockUnblockCustomerAPI(Resource):
    @jwt_required()
    def put(self, customer_id):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Parse request JSON data
            data = request.get_json()
            is_active = data.get('is_active')

            # Find the customer by ID
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "Customer not found."}, 404

            # Update the is_active status
            customer.is_active = is_active
            db.session.commit()

            return {"message": "Customer status updated successfully."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        
class AdminCustomerSearchAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        user = User.query.get(current_user)
        if not user or 'admin' not in [role.name for role in user.roles]:
            return {"error": "Unauthorized access."}, 403

        try:
            # Retrieve query parameters
            fullname_query = request.args.get('fullname', '').strip().lower()
            email_query = request.args.get('email', '').strip().lower()
            pincode_query = request.args.get('pincode', '').strip().lower()
            is_active_query = request.args.get('is_active', '').strip().lower()
            address_query = request.args.get('address', '').strip().lower()

            # Build the query
            query = db.session.query(Customer, User).join(User, Customer.user_id == User.id)

            if fullname_query:
                query = query.filter(Customer.fullname.ilike(f'%{fullname_query}%'))
            if email_query:
                query = query.filter(User.email.ilike(f'%{email_query}%'))
            if pincode_query:
                query = query.filter(Customer.pincode.ilike(f'%{pincode_query}%'))
            if is_active_query:
                query = query.filter(Customer.is_active == (is_active_query.lower() == 'true'))
            if address_query:
                query = query.filter(Customer.address.ilike(f'%{address_query}%'))

            customers = query.all()

            customer_list = []
            for customer, user in customers:
                customer_data = {
                    "customer_id": customer.id,
                    "user_id": user.id,
                    "fullname": customer.fullname,
                    "email": user.email,
                    "address": customer.address,
                    "pincode": customer.pincode,
                    "is_active": customer.is_active
                }
                customer_list.append(customer_data)

            return {"customers": customer_list}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500

class AdminServiceOneAPI(Resource):
    @jwt_required()
    def get(self, service_id):
        try:
            service = Service.query.get(service_id)
            if not service:
                return {"error": "Service not found"}, 404

            service_data = {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price,
                "time_required": service.time_required
            }
            return {"service": service_data}, 200

        except SQLAlchemyError as e:
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500
        