# project/server/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.notification.oap_email_notofier import EmailNotifier
from project.server import db, bcrypt, app
from project.server.models import User, BlacklistToken, OAPUsersRole


class UserRole(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            user_role = OAPUsersRole(
                wwid=post_data.get('wwid'),
                group=post_data.get('group'),
                role=post_data.get('role')
            )

            db.session.add(user_role)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully Added Role.',
                'wwid': post_data.get('wwid')
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500

    def get(self):
        try:
            data = request.args
            wwid = data['wwid']
            roles = OAPUsersRole.query.filter_by(wwid=wwid).all()
            list_roles = []
            user_group = ''
            for role in roles:
                user_group = role.group
                list_roles.append(role.role)
            responseObject = {
                'status': 'success',
                'user_roles': {'wwid': wwid, 'roles': list_roles, 'group': user_group}
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Unable to Fetch role.',
                'description': e
            }
            return make_response(jsonify(responseObject)), 500


class UpdateUserPassword(MethodView):
    def get(self):
        params = request.args
        username = params['email']
        c_password = params['password'].encode('utf-8')
        n_password = params['new_password'].encode('utf-8')
        try:
            user = User.query.filter_by(email=username).first()
            if user and bcrypt.check_password_hash(user.user_password.encode('utf-8'), c_password):
                user.user_password = bcrypt.generate_password_hash(
                    n_password, app.config.get('BCRYPT_LOG_ROUNDS')
                ).decode()
                db.session.commit()
                db.session.close()
                responseObject = {
                    'status': 'success',
                    'message': 'password updated Successfully !!.'
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'success',
                    'message': 'No user found !!.'
                }
                return make_response(jsonify(responseObject)), 201


        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': e
            }
            return make_response(jsonify(responseObject)), 500


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    user_password=post_data.get('password'),
                    user_name=post_data.get('user_name'),
                    user_group=post_data.get('user_group'),
                    first_name=post_data.get('first_name'),
                    last_name=post_data.get('last_name'),
                    wwid=post_data.get('wwid'),
                    role=post_data.get('role')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.user_id)
                self.triggerEmail(user.user_id, post_data.get('password'))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

    def triggerEmail(self, user_id, user_password):
        user = User.query.filter_by(user_id=user_id).first()
        email = EmailNotifier(oap_user=user.email,
                              oap_user_password=user_password,
                              password_reset_link='https://oap-middletier-upgrade.apps1-fm-int.icloud.intel.com/user/'
                                                  'update-password?email=EMAIL&password=PASSWORD'
                                                  '&new_password=NEW_PASSWORD',
                              to_list=user.email,
                              oap_user_fullname=user.first_name,
                              notification_type='new_user')
        email.trigger_email_notification()


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and bcrypt.check_password_hash(user.user_password, post_data.get('password')):
                auth_token = user.encode_auth_token(user.user_id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(user_id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.user_id,
                        'user_name': user.user_name,
                        'user_group': user.user_group,
                        'role': user.role,
                        'email': user.email,
                        'registered_on': user.create_At,
                        'wwid': user.wwid
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


auth_blueprint = Blueprint('auth', __name__)
# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
updated_password = UpdateUserPassword.as_view('updated_password')
user_roles = UserRole.as_view('user_roles')
auth_blueprint.add_url_rule(
    '/auth/user/roles',
    view_func=user_roles,
    methods=['GET', 'POST']
)
# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['GET', 'POST']
)
auth_blueprint.add_url_rule(
    '/user/update-password',
    view_func=updated_password,
    methods=['GET', 'POST']
)
