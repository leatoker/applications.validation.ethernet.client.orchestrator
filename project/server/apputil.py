from project.server.models import User, ManualProvision, NickelProfile


class AppUtil:
    def __init__(self, **kwargs):
        self.auth_token = kwargs.get('auth_token')
        self.list_obj = kwargs.get('list_obj')

    def validateUser(self):
        auth_header = self.auth_token
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
                if auth_token:
                    resp = User.decode_auth_token(auth_token)
                    if not isinstance(resp, str):
                        user = User.query.filter_by(user_id=resp).first()
                        if user:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            except IndexError:
                return False

    def prepareNickelProfile(self):
        responses = []
        for post_data in self.list_obj:
            print(post_data)
            print(type(post_data))
            responses.append(NickelProfile(
                profile_name=post_data.get('profile_name')
            ))

    def prepareObject(self):
        provision_lists = []
        for post_data in self.list_obj:
            provision_lists.append(
                ManualProvision(
                    controller=post_data.get('controller'),
                    sut=post_data.get('sut'),
                    is_ifwi=post_data.get('is_ifwi'),
                    tws_result_ifwi=post_data.get('tws_result_ifwi'),
                    is_bios=post_data.get('is_bios'),
                    tws_result_bios=post_data.get('tws_result_bios'),
                    is_os=post_data.get('is_os'),
                    tws_result_os=post_data.get('tws_result_os'),
                    request_id=post_data.get('request_id'),
                    user_id=post_data.get('user_id'),
                    share_path=post_data.get('share_path'),
                    share_uid=post_data.get('share_uid'),
                    share_pwd=post_data.get('share_pwd'),
                    location_type=post_data.get('location_type'),
                    wwid=post_data.get('wwid'),
                    external_id=post_data.get('external_id'),
                    email=post_data.get('email'),
                    kit=post_data.get('kit'),
                    ifwi=post_data.get('ifwi'),
                    wim_name=post_data.get('wim_name'),
                    bios_file=post_data.get('bios_file'),
                    e2e_tws_result=post_data.get('e2e_tws_result'),
                    is_e2e=post_data.get('is_e2e'),
                    wifi_name=post_data.get('wifi_name'),
                    wifi_password=post_data.get('wifi_password')
                )
            )
        return provision_lists
