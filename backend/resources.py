from flask_restful import Resource, Api, reqparse, fields, marshal_with
from backend.models import User
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from backend.db import db
from backend.routes.allroutes import LoginAPI, RegisterCustomerAPI, RegisterProfessionalAPI

api = Api(prefix='/api')

api.add_resource(LoginAPI, '/login')
api.add_resource(RegisterCustomerAPI, '/register/customer')
api.add_resource(RegisterProfessionalAPI, '/register/professional')