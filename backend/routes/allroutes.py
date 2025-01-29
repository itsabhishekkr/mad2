from flask import jsonify, current_app
from flask_restful import Resource, request
from sqlalchemy.exc import SQLAlchemyError
from backend.models import db, User, Customer, Professional, Role, Service
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename

class LoginAPI(Resource):
    def post(self):
        try:
            # Extract email and password from the request JSON
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            # Query the user by email
            user = User.query.filter_by(email=email).first()

            if not user:
                return {
                    "status": "error",
                    "message": "Invalid email or password."
                }, 401  # Unauthorized

            # Check if the password is correct
            if not user.check_password(password):
                return {
                    "status": "error",
                    "message": "Invalid email or password."
                }, 401

            # Check if the user is active
            if not user.active:
                return {
                    "status": "error",
                    "message": "Your account is inactive."
                }, 403  # Forbidden

            # Generate an access token
            access_token = create_access_token(identity=str(user.id))

            # Role-based checks
            if user.roles:
                if 'customer' in [role.name for role in user.roles]:
                    customer = Customer.query.filter_by(user_id=user.id).first()
                    if not customer or not customer.is_active:
                        return {
                            "status": "error",
                            "message": "Customer account is not active."
                        }, 403

                    return {
                        "status": "success",
                        "message": "Login successful.",
                        "role": "customer",
                        "access_token": access_token
                    }, 200

                elif 'professional' in [role.name for role in user.roles]:
                    professional = Professional.query.filter_by(user_id=user.id).first()
                    if not professional or not professional.is_approved:
                        return {
                            "status": "error",
                            "message": "Professional account is not approved."
                        }, 403

                    return {
                        "status": "success",
                        "message": "Login successful.",
                        "role": "professional",
                        "access_token": access_token
                    }, 200

                elif 'admin' in [role.name for role in user.roles]:
                    return {
                        "status": "success",
                        "message": "Login successful.",
                        "role": "admin",
                        "access_token": access_token
                    }, 200

            return {
                "status": "error",
                "message": "User role is not defined or invalid."
            }, 400  # Bad request

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }, 500  # Internal server error

        except Exception as e:
            return {
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, 500

class RegisterCustomerAPI(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            # Parse request JSON data
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            fullname = data.get('fullname')
            address = data.get('address')
            pincode = data.get('pincode')

            # Validate required fields
            if not email or not password or not fullname or not address or not pincode:
                return {"error": "Missing required fields."}, 400

            # Check for existing user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"error": "Email already exists."}, 409

            # Create and save the user
            user = User(email=email, active=True)
            user.password = generate_password_hash(password)
            role = Role.query.filter_by(name='customer').first()
            if not role:
                role = Role(name='customer')
                db.session.add(role)
                db.session.commit()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()

            # Create and save the customer profile
            customer = Customer(
                fullname=fullname,
                address=address,
                pincode=pincode,
                user_id=user.id
            )
            db.session.add(customer)
            db.session.commit()

            return {"message": "Registration successful."}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: {}".format(str(e))}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred: {}".format(str(e))}, 500

    def get(self):
        return {"message": "This endpoint supports POST requests to register a customer."}, 200
    




####------------------------------------Register Professional API------------------------------------####



class RegisterProfessionalAPI(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            # Retrieve form fields and file
            email = request.form.get('email')
            password = request.form.get('password')
            fullname = request.form.get('fullname')
            available_services = request.form.getlist('available_services')
            experience = request.form.get('experience')
            address = request.form.get('address')
            pincode = request.form.get('pincode')
            documents = request.files.get('documents')

            # Validate required fields
            if not email or not password or not fullname or not experience:
                return jsonify({"error": "Missing required fields."}), 400

            # Check for existing user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"error": "Email already exists."}), 409

            # Handle file upload (if file is uploaded)
            if documents:
                filename = secure_filename(documents.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                documents.save(upload_path)
            else:
                upload_path = None  # You can set a default value if necessary

            # Create new user
            user = User(email=email, active=True)
            user.password = generate_password_hash(password)
            role = Role.query.filter_by(name='professional').first()
            if not role:
                role = Role(name='professional')
                db.session.add(role)
                db.session.commit()
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()

            # Create professional profile
            professional = Professional(
                fullname=fullname,
                available_services=', '.join(available_services),
                experience=int(experience),
                address=address,
                pincode=pincode,
                user_id=user.id,
                documents_path=upload_path  # Store the file path or other info as needed
            )
            db.session.add(professional)
            db.session.commit()

            # Return a proper JSON response with a 201 status code
            return jsonify({"message": "Registration successful. Awaiting admin approval."}), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Database error: {}".format(str(e))}), 500

        except Exception as e:
            # Return the error as JSON
            return jsonify({"error": "An unexpected error occurred: {}".format(str(e))}), 500

    def get(self):
        return jsonify({"message": "This endpoint supports POST requests to register a professional."}), 200
    
