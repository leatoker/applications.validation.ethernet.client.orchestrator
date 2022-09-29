import sys

sys.path.append("logger")
from project.logger.logger_util import get_logger_instance

LOG = get_logger_instance()


class OAPMTServices:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.user_name = kwargs.get('user_name')
        self.user_wwid = kwargs.get('user_wwid')
        self.user_firstName = kwargs.get('user_firstName')
        self.user_lastName = kwargs.get('user_lastName')
        self.user_group = kwargs.get('user_group')
        self.user_role = kwargs.get('user_role')
        self.user_email = kwargs.get('user_email')

        self.controller_id = kwargs.get('controller_id')
        self.controller_name = kwargs.get('controller_name')
        self.controller_group = kwargs.get('controller_group')

        self.platform_id = kwargs.get('platform_id')
        self.platform_name = kwargs.get('platform_name')
        self.platform_group = kwargs.get('platform_group')

        self.provision_global_id = kwargs.get('provision_global_id')
        self.provision_id = kwargs.get('provision_id')
        self.provision_type = kwargs.get('provision_type')
        self.provision_isIfwi = kwargs.get('provision_isIfwi')
        self.provision_IfwiUrl = kwargs.get('provision_IfwiUrl')
        self.provision_isBios = kwargs.get('provision_isBios')
        self.provision_BiosUrl = kwargs.get('provision_BiosUrl')
        self.provision_isOs = kwargs.get('provision_isOs')
        self.provision_OsUrl = kwargs.get('provision_OsUrl')
        self.provision_createdAt = kwargs.get('provision_createdAt')
        self.provision_sharePath = kwargs.get('provision_sharePath')
        self.provision_shareUid = kwargs.get('provision_shareUid')
        