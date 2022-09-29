# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))
# mysql+mysqlconnector://OneAP_ManualProvisio_so:0HdE2Qm24Q97b21@maria4110-lb-fm-in.iglb.intel.com:3307/=>prod
# mysql+mysqlconnector://OneAP_ManualProvisio_so:v1tUuLj2cTzD4Jb@maria4120-lb-fm-in.dbaas.intel.com:3307/ =>pre-prod
maria_connection_string = 'mysql+mysqlconnector://OneAP_ManualProvisio_so:0HdE2Qm24Q97b21@maria4110-lb-fm-in.iglb.intel.com:3307/'
database_name = 'OneAP_ManualProvision'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = maria_connection_string + database_name

# class TestingConfig(BaseConfig):
#     """Testing configuration."""
#     DEBUG = True
#     TESTING = True
#     BCRYPT_LOG_ROUNDS = 4
#     SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
#     PRESERVE_CONTEXT_ON_EXCEPTION = False
#
#
# class ProductionConfig(BaseConfig):
#     """Production configuration."""
#     SECRET_KEY = 'my_precious'
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
