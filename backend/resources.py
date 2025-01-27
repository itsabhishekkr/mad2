from flask_restful import Resource, Api, reqparse, fields, marshal_with
from backend.models import User
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from backend.db import db
from backend.routes.allroutes import LoginAPI, RegisterCustomerAPI, RegisterProfessionalAPI
from backend.routes.admin import AllAdminServiceAPI,AdminAddServiceAPI, AdminUpdateServiceAPI, AdminDeleteServiceAPI
from backend.routes.admin import AdminServiceSummaryAPI, AdminServiceSearchAPI, AdminProfessionalDetailsAPI, AdminBlockUnblockProfessionalAPI
from backend.routes.admin import AdminProfessionalSummaryAPI, AdminProfessionalSearchAPI, AdminCustomerDetailsAPI,AdminCustomerSummaryAPI
from backend.routes.admin import AdminBlockUnblockCustomerAPI,AdminCustomerSearchAPI,AdminServiceOneAPI
from backend.routes.customer import AdminBlockCustomer, AdminUnblockCustomer

api = Api(prefix='/api')

api.add_resource(LoginAPI, '/login')
api.add_resource(RegisterCustomerAPI, '/register/customer')
api.add_resource(RegisterProfessionalAPI, '/register/professional')
api.add_resource(AdminAddServiceAPI, '/admin/service/add/')
api.add_resource(AllAdminServiceAPI, '/admin/service/all')
api.add_resource(AdminServiceOneAPI, '/admin/service/one/<int:service_id>') 
api.add_resource(AdminUpdateServiceAPI, '/admin/service/update/<int:service_id>')
api.add_resource(AdminDeleteServiceAPI, '/admin/service/delete/<int:service_id>') 
api.add_resource(AdminServiceSummaryAPI, '/admin/service/summary')
api.add_resource(AdminServiceSearchAPI, '/admin/service/search/<string:search_term>')
api.add_resource(AdminProfessionalDetailsAPI, '/admin/professional/details')
api.add_resource(AdminBlockUnblockProfessionalAPI, '/admin/professional/block_unblock/<int:professional_id>') 
api.add_resource(AdminProfessionalSummaryAPI, '/admin/summary/professionals') 
api.add_resource(AdminProfessionalSearchAPI, '/admin/professional/search')
api.add_resource(AdminCustomerDetailsAPI, '/admin/customer/details')
api.add_resource(AdminCustomerSummaryAPI, '/admin/summary/customers')
api.add_resource(AdminBlockUnblockCustomerAPI, '/admin/customer/block_unblock/<int:customer_id>') 
api.add_resource(AdminCustomerSearchAPI, '/admin/customer/search')
api.add_resource(AdminBlockCustomer, '/admin/customer/block/<int:customer_id>')
api.add_resource(AdminUnblockCustomer, '/admin/customer/unblock/<int:customer_id>')
