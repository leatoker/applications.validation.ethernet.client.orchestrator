import json
import unittest

from project.tests.base import BaseTestCase


class TestOapFlows(BaseTestCase):
    def test_add_controller(self):
        """ test_add_controller """
        with self.client:
            # user registration
            resp_controller = self.client.post(
                '/oap/controller',
                data=json.dumps(dict(
                    controller='test_alias',
                    group='1',
                    alias_name="test_alias"
                )),
                content_type='application/json',
            )
            data = json.loads(resp_controller.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_controller(self):
        """ test_fetch_controller """
        with self.client:
            resp_controller = self.client.get(
                '/oap/controller',
                content_type='application/json',
            )
            data = json.loads(resp_controller.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_platform(self):
        """ test_add_controller """
        with self.client:
            # user registration
            resp_platform = self.client.post(
                '/oap/platform',
                data=json.dumps(dict(
                    platform='Alder Lake',
                    alias_name='ADL',
                    controller_id='1'
                )),
                content_type='application/json',
            )
            data = json.loads(resp_platform.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_platform(self):
        """ test_fetch_controller """
        with self.client:
            resp_platform = self.client.get(
                '/oap/platform',
                content_type='application/json',
            )
            data = json.loads(resp_platform.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_provision_master(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/provision_master',
                data=json.dumps(dict(
                    user_id=1
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_provision_master(self):
        """ test_fetch_controller """
        with self.client:
            response = self.client.get(
                '/oap/provision_master',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_provision(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/provision',
                data=json.dumps([dict(controller='test-controller', sut='test-sut',
                                      is_ifwi='In Progress',
                                      tws_result_ifwi='http://ifwi-url.com',
                                      is_bios='In Progress',
                                      tws_result_bios='http://bios-url.com',
                                      is_os='In Progress',
                                      tws_result_os='http://os-url.com',
                                      request_id=1,
                                      user_id=1,
                                      share_path='dummy-share-path',
                                      share_uid='dummy-share-uid',
                                      share_pwd='dummy-share-pwd',
                                      location_type='artifactory',
                                      wwid=11918760
                                      )]),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_profile(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/nic/profile?type=new',
                data=json.dumps(dict(profile_name='gs-test',
                                     owner=11918760,
                                     profile_desc='profile_desc',
                                     build_number='build_number',
                                     choco_source='choco_source',
                                     share_path='share_path',
                                     share_uname='share_uname',
                                     share_pwd='share_pwd ',
                                     kit_name='kit_name',
                                     ifwi_bin='ifwi_bin',
                                     wim_name='wim_name',
                                     group_name='group-1',
                                     owner_name='vishal',
                                     sx_cycling_count='3',
                                     ifwi_flash_method_list=['test41', 'test42', 'test43'],
                                     execution_mode_list=['test1', 'test21'],
                                     execution_type_list=['test1', 'test32'],
                                     network_type_list=['test1', 'test25'],
                                     image_type_list=['test1', 'test29'],
                                     cycle_type_list=['test1', 'test42'],
                                     wake_mode_list=['test1', 'test22'],
                                     power_mode_list=['test1', 'test24'],
                                     tws_version_list=['test1', 'test26'],
                                     system_provisioning='native',
                                     firmware_sku='test123',
                                     controller='con-1',
                                     fanout_attr='fanout_attr',
                                     wimager_version='wimager_version',
                                     fanout_value='fanout_value'

                                     )
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_project(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/nic/project',
                data=json.dumps(dict(project_name='profile_53',
                                     creator=11918760)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_project(self):
        with self.client:
            response = self.client.get(
                '/oap/nic/project',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_delete_project(self):
        with self.client:
            response = self.client.delete(
                '/oap/nic/project',
                data=json.dumps(dict(project_id=2)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_update_profile(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.patch(
                '/oap/nic/profile',
                data=json.dumps(dict(profile_name='gs-test',
                                     profile_id=161,
                                     owner=11918760,
                                     profile_desc='profile_desc',
                                     build_number='build_number',
                                     choco_source='choco_source',
                                     share_path='share_path',
                                     share_uname='share_uname',
                                     share_pwd='share_pwd ',
                                     kit_name='kit_name',
                                     ifwi_bin='ifwi_bin',
                                     wim_name='wim_name',
                                     group_name='group-2',
                                     sx_cycling_count='13',
                                     ifwi_flash_method_list=['test411', 'test421', 'test431'],
                                     execution_mode_list=['test111', 'test2111'],
                                     execution_type_list=['test111', 'test3211'],
                                     network_type_list=['test111', 'test2511'],
                                     image_type_list=['test1111', 'test2911'],
                                     cycle_type_list=['test1111', 'test42111'],
                                     wake_mode_list=['test1111', 'test221111'],
                                     power_mode_list=['test1111', 'test24111'],
                                     tws_version_list=['test1111', 'test24111'],
                                     system_provisioning='native12',
                                     firmware_sku='test321',
                                     controller='con-2',
                                     fanout_attr='fanout_attr-new',
                                     fanout_value='fanout_value-new'
                                     )

                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_profile(self):
        with self.client:
            response = self.client.get(
                '/oap/nic/profile',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_delete_profile(self):
        with self.client:
            response = self.client.delete(
                '/oap/nic/profile?profile_id=1',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_provision(self):
        with self.client:
            response = self.client.get(
                '/oap/provision?type=new&page=2',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_provision_result(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/provision_result',
                data=json.dumps(dict(page=1,
                                     per_page=15)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_provision_result_new(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/provision_result_new',
                data=json.dumps(dict(page=1,
                                     per_page=15)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_sut_status(self):
        with self.client:
            response = self.client.get(
                '/oap/controller/sutstatus?controller=UST-AF2-TWS-01.gar.corp.intel.com',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_update_provision(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.patch(
                '/oap/provision',
                data=json.dumps(dict(provision_id=1,
                                     provision_type='is_ifwi',
                                     provision_status='PASS'
                                     )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'PASS')

    def test_add_project_profile_mapping(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/nic/project-profile-map',
                data=json.dumps(dict(project_id=4,
                                     profile_id=48,
                                     creator=11918760)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_project_profile_mapping(self):
        with self.client:
            response = self.client.get(
                '/oap/nic/project-profile-map',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_delete_project_profile_mapping(self):
        with self.client:
            response = self.client.delete(
                '/oap/nic/project-profile-map',
                data=json.dumps(dict(project_id=1,
                                     profile_id=49)
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_add_nickel_result(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.post(
                '/oap/nic/result',
                data=json.dumps(dict(profile_name=12,
                                     executor=11918760,
                                     sut='SUT-1',
                                     controller='controller-1',
                                     result_status='PASS',
                                     result_link='https://google.com')
                                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_fetch_nickel_result(self):
        with self.client:
            response = self.client.get(
                '/oap/nic/result',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')

    def test_update_nickel_result(self):
        """ test_add_controller """
        with self.client:
            # user registration
            response = self.client.patch(
                '/oap/nic/result',
                data=json.dumps(dict(trigger_id=3,
                                     status='FAIL'
                                     )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')


        if __name__ == '__main__':
            unittest.main()
            test_oap_flow = TestOapFlows()
            test_oap_flow.test_fetch_provision_result_new()