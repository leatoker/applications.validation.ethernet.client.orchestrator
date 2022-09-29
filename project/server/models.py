# project/server/models.py

import datetime
import json

import jwt

from project.server import app, db, bcrypt


class OAPUsersRole(db.Model):
    __tablename__ = "OAP_USERS_ROLE"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wwid = db.Column(db.Integer, nullable=False)
    group = db.Column(db.String(255))
    role = db.Column(db.String(255))
    create_At = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.role_id = kwargs.get('role_id')
        self.wwid = kwargs.get('wwid')
        self.group = kwargs.get('group')
        self.role = kwargs.get('role')
        self.create_At = datetime.datetime.now()


class NickelResult(db.Model):
    __tablename__ = "NICKEL_RESULT"
    trigger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_name = db.Column(db.String(255))
    executor = db.Column(db.String(255))
    owner_name = db.Column(db.String(250))
    tws_version= db.Column(db.String(250))
    sut = db.Column(db.String(255))
    result_status = db.Column(db.String(255))
    result_link = db.Column(db.String(255))
    controller = db.Column(db.String(255))
    create_At = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.trigger_id = kwargs.get('trigger_id')
        self.profile_name = kwargs.get('profile_name')
        self.executor = kwargs.get('executor')
        self.owner_name = kwargs.get('owner_name')
        self.tws_version = kwargs.get('tws_version')
        self.sut = kwargs.get('sut')
        self.result_status = kwargs.get('result_status')
        self.result_link = kwargs.get('result_link')
        self.create_At = kwargs.get('create_At')
        self.controller = kwargs.get('controller')


class NickelExecution(db.Model):
    __tablename__ = "NICKEL_EXECUTION"
    execution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer)
    fanout_attr = db.Column(db.String(255))
    fanout_value = db.Column(db.String(255))
    executor = db.Column(db.Integer)
    create_At = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.execution_id = kwargs.get('execution_id')
        self.profile_id = kwargs.get('profile_id')
        self.fanout_attr = kwargs.get('fanout_attr')
        self.fanout_value = kwargs.get('fanout_value')
        self.executor = kwargs.get('executor')
        self.create_At = kwargs.get('create_At')


class NickelProject(db.Model):
    __tablename__ = "NICKEL_PROJECT"
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255))
    creator = db.Column(db.String(255))
    create_At = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.project_id = kwargs.get('project_id')
        self.project_name = kwargs.get('project_name')
        self.creator = kwargs.get('creator')
        self.create_At = datetime.datetime.now()


class NickelProjectProfile_Map(db.Model):
    __tablename__ = "NICKEL_PROJECT_PROFILE_MAPPING"
    project_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(255))
    create_At = db.Column(db.DateTime)
    owner_name = db.Column(db.String(250))

    def __init__(self, **kwargs):
        self.project_id = kwargs.get('project_id')
        self.profile_id = kwargs.get('profile_id')
        self.creator = kwargs.get('creator')
        self.create_At = datetime.datetime.now()
        self.owner_name = kwargs.get('owner_name')

class NickelProfile(db.Model):
    __tablename__ = "NICKEL_PROFILE"
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_name = db.Column(db.String(255))
    owner = db.Column(db.Integer, nullable=False)
    profile_desc = db.Column(db.String(255))
    build_number = db.Column(db.String(255))
    choco_source = db.Column(db.String(255))
    share_path = db.Column(db.String(255))
    share_uname = db.Column(db.String(255))
    share_pwd = db.Column(db.String(255))
    kit_name = db.Column(db.String(255))
    ifwi_bin = db.Column(db.String(255))
    wim_name = db.Column(db.String(255))
    flashing_method = db.Column(db.String(255))
    execution_mode = db.Column(db.String(255))
    execution_type = db.Column(db.String(255))
    network_type = db.Column(db.String(255))
    imaging_type = db.Column(db.String(255))
    sx_cycle_type = db.Column(db.String(255))
    sx_continue_on_fail = db.Column(db.String(255))
    sx_debug_arg = db.Column(db.String(255))
    sx_sleep_time = db.Column(db.String(255))
    sx_wake_mode = db.Column(db.String(255))
    sx_wake_time = db.Column(db.String(255))
    ict_result_path = db.Column(db.String(255))
    tws_no_wait = db.Column(db.String(255))
    wrapper_fanout = db.Column(db.String(255))
    power_mode = db.Column(db.String(255))
    isct_version = db.Column(db.String(255))
    execution_dir = db.Column(db.String(255))
    install_dir = db.Column(db.String(255))
    group_name = db.Column(db.String(250))
    owner_name = db.Column(db.String(250))
    sx_cycling_count = db.Column(db.String(250))
    create_At = db.Column(db.DateTime)
    ifwi_flash_method_list = db.Column(db.String(500))
    execution_mode_list = db.Column(db.String(500))
    execution_type_list = db.Column(db.String(500))
    network_type_list = db.Column(db.String(500))
    image_type_list = db.Column(db.String(500))
    cycle_type_list = db.Column(db.String(500))
    wake_mode_list = db.Column(db.String(500))
    power_mode_list = db.Column(db.String(500))
    tws_version_list = db.Column(db.String(500))
    System_Provisioning = db.Column(db.String(250))
    FirmwareSKU = db.Column(db.String(250))
    tws_version = db.Column(db.String(250))

    controller = db.Column(db.String(250))
    fanout_attr = db.Column(db.String(250))
    wimager_version = db.Column(db.String(250))
    fanout_value = db.Column(db.String(250))
    jarvis_pwd = db.Column(db.String(250))

    def __init__(self, **kwargs):
        self.profile_id = kwargs.get('profile_id')
        self.profile_name = kwargs.get('profile_name')
        self.owner = kwargs.get('owner')
        self.profile_desc = kwargs.get('profile_desc')
        self.build_number = kwargs.get('build_number')
        self.choco_source = kwargs.get('choco_source')
        self.share_path = kwargs.get('share_path')
        self.share_uname = kwargs.get('share_uname')
        self.share_pwd = kwargs.get('share_pwd')
        self.kit_name = kwargs.get('kit_name')
        self.ifwi_bin = kwargs.get('ifwi_bin')
        self.wim_name = kwargs.get('wim_name')
        self.flashing_method = kwargs.get('flashing_method')
        self.execution_mode = kwargs.get('execution_mode')
        self.execution_type = kwargs.get('execution_type')
        self.network_type = kwargs.get('network_type')
        self.imaging_type = kwargs.get('imaging_type')
        self.sx_cycle_type = kwargs.get('sx_cycle_type')
        self.sx_continue_on_fail = kwargs.get('sx_continue_on_fail')
        self.sx_debug_arg = kwargs.get('sx_debug_arg')
        self.sx_sleep_time = kwargs.get('sx_sleep_time')
        self.sx_wake_mode = kwargs.get('sx_wake_mode')
        self.sx_wake_time = kwargs.get('sx_wake_time')
        self.ict_result_path = kwargs.get('ict_result_path')
        self.tws_no_wait = kwargs.get('tws_no_wait')
        self.wrapper_fanout = kwargs.get('wrapper_fanout')
        self.power_mode = kwargs.get('power_mode')
        self.isct_version = kwargs.get('isct_version')
        self.execution_dir = kwargs.get('execution_dir')
        self.install_dir = kwargs.get('install_dir')
        self.group_name = kwargs.get('group_name')
        self.owner_name = kwargs.get('owner_name')
        self.create_At = kwargs.get('create_At')
        self.sx_cycling_count = kwargs.get('sx_cycling_count')

        self.ifwi_flash_method_list = kwargs.get('ifwi_flash_method_list')
        self.execution_mode_list = kwargs.get('execution_mode_list')
        self.execution_type_list = kwargs.get('execution_type_list')
        self.network_type_list = kwargs.get('network_type_list')
        self.image_type_list = kwargs.get('image_type_list')
        self.cycle_type_list = kwargs.get('cycle_type_list')
        self.wake_mode_list = kwargs.get('wake_mode_list')
        self.power_mode_list = kwargs.get('power_mode_list')
        self.tws_version_list = kwargs.get('tws_version_list')
        self.System_Provisioning = kwargs.get('System_Provisioning')
        self.FirmwareSKU = kwargs.get('FirmwareSKU')
        self.tws_version = kwargs.get('tws_version')

        self.controller = kwargs.get('controller')
        self.fanout_attr = kwargs.get('fanout_attr')
        self.wimager_version = kwargs.get('wimager_version')
        self.fanout_value = kwargs.get('fanout_value')
        self.jarvis_pwd = kwargs.get('jarvis_pwd')


class OapUserACL(db.Model):
    __tablename__ = "OAP_User_ACL"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    resource_id = db.Column(db.Integer)
    permission_type = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.resource_id = kwargs.get('resource_id')
        self.permission_type = kwargs.get('permission_type')
        self.desc = kwargs.get('desc')


class OapUserGroup(db.Model):
    __tablename__ = "OAP_USER_GROUP"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')


class OapUserRole(db.Model):
    __tablename__ = "OAP_USER_ROLE"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.desc = kwargs.get('desc')


class OapResource(db.Model):
    __tablename__ = "OAP_RESOURCE"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.desc = kwargs.get('desc')


class Platform(db.Model):
    __tablename__ = "PLATFORM"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_name = db.Column(db.String(255))
    alias_name = db.Column(db.String(255))
    controller_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.platform_name = kwargs.get('platform_name')
        self.alias_name = kwargs.get('alias_name')
        self.controller_id = kwargs.get('controller_id')


class Controller(db.Model):
    __tablename__ = "CONTROLLER"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    controller_name = db.Column(db.String(255))
    group_id = db.Column(db.Integer)
    alias_name = db.Column(db.String(255))

    def __init__(self, **kwargs):
        self.controller_name = kwargs.get('controller_name')
        self.group_id = kwargs.get('group_id')
        self.alias_name = kwargs.get('alias_name')


from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class ManualProvisionMaster(db.Model):
    __tablename__ = "MANUAL_PROVISION_MASTER"
    global_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')


class ManualProvision(db.Model):
    __tablename__ = "OAP_MANUAL_PROVISION"
    provision_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    controller = db.Column(db.String(255))
    sut = db.Column(db.String(255))
    is_ifwi = db.Column(db.String(255))
    tws_result_ifwi = db.Column(db.String(255))
    is_bios = db.Column(db.String(255))
    tws_result_bios = db.Column(db.String(255))
    is_os = db.Column(db.String(255))
    tws_result_os = db.Column(db.String(255))
    request_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    create_At = db.Column(db.DateTime)
    share_path = db.Column(db.String(255))
    share_uid = db.Column(db.String(255))
    share_pwd = db.Column(db.String(45))
    location_type = db.Column(db.String(255))
    wwid = db.Column(db.Integer)
    external_id = db.Column(db.String(250))
    email = db.Column(db.String(256))
    kit = db.Column(db.String(256))
    ifwi = db.Column(db.String(256))
    wim_name = db.Column(db.String(256))
    bios_file = db.Column(db.String(256))
    is_e2e = db.Column(db.String(255))
    e2e_tws_result = db.Column(db.String(256))
    wifi_name = db.Column(db.String(255))
    wifi_password = db.Column(db.String(45))

    def __init__(self, **kwargs):
        self.controller = kwargs.get('controller')
        self.sut = kwargs.get('sut')
        self.is_ifwi = kwargs.get('is_ifwi')
        self.tws_result_ifwi = kwargs.get('tws_result_ifwi')
        self.is_bios = kwargs.get('is_bios')
        self.tws_result_bios = kwargs.get('tws_result_bios')
        self.is_os = kwargs.get('is_os')
        self.tws_result_os = kwargs.get('tws_result_os')
        self.request_id = kwargs.get('request_id')
        self.user_id = kwargs.get('user_id')
        self.create_At = datetime.datetime.now()
        self.share_path = kwargs.get('share_path')
        self.share_uid = kwargs.get('share_uid')
        self.share_pwd = kwargs.get('share_pwd')
        self.location_type = kwargs.get('location_type')
        self.wwid = kwargs.get('wwid')
        self.external_id = kwargs.get('external_id')
        self.email = kwargs.get('email')
        self.kit = kwargs.get('kit')
        self.ifwi = kwargs.get('ifwi')
        self.wim_name = kwargs.get('wim_name')
        self.bios_file = kwargs.get('bios_file')
        self.is_e2e = kwargs.get('is_e2e')
        self.e2e_tws_result = kwargs.get('e2e_tws_result')
        self.wifi_name = kwargs.get('wifi_name')
        self.wifi_password = kwargs.get('wifi_password')


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "OAP_USERS"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wwid = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    user_group = db.Column(db.Integer)
    email = db.Column(db.String(255))
    user_password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    create_At = db.Column(db.DateTime)
    role = db.Column(db.Integer)

    def __init__(self, wwid='test', user_name='test', user_group=1, email='test@intel.com', user_password='',
                 first_name='test', last_name='test', role=1):
        self.wwid = wwid
        self.user_name = user_name
        self.user_group = user_group
        self.email = email
        self.user_password = bcrypt.generate_password_hash(
            user_password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.create_At = datetime.datetime.now()
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=45, seconds=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
