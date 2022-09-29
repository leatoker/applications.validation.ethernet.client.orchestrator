# project/server/oap/nickel/nickelviews.py

import datetime

from flask import request, make_response, jsonify, Blueprint
from flask.views import MethodView
from sqlalchemy import text

from project.server import db
from project.server.models import NickelProfile, NickelProject, NickelProjectProfile_Map, NickelResult


class NickelResultAPI(MethodView):
    def patch(self):
        post_data = request.get_json()
        try:
            trigger_id = int(post_data.get('trigger_id'))
            status = post_data.get('status')
            updated = db.session.query(NickelResult).filter(
                text("trigger_id=:id")).params(
                id=trigger_id).first()
            if updated and updated.result_status != status:
                updated.result_status = status
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully Updated.',
                    'id': trigger_id,
                    'provision_status': status
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'success',
                    'message': 'No Row To Update.',
                    'id': trigger_id,
                    'provision_status': status
                }
                return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Unable to Update Result.'
            }
            return make_response(jsonify(responseObject)), 500

    def post(self):
        post_data = request.get_json()
        nickel_result = NickelResult(
            profile_name=post_data.get('profile_name'),
            executor=post_data.get('executor'),
            owner_name=post_data.get('owner_name'),
            tws_version=post_data.get('tws_version'),
            sut=post_data.get('sut'),
            result_status=post_data.get('result_status'),
            controller=post_data.get('controller'),
            result_link=post_data.get('result_link'),
            create_At=datetime.datetime.now()
        )
        try:
            db.session.add(nickel_result)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully Added Nickel Result.'
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'Fail',
                'message': 'Error While Nickel Execution Result.'
            }
            return make_response(jsonify(responseObject)), 500

    def get(self):
        try:
            projects = NickelResult.query.all()
            results = []
            for p in projects:
                results.append(
                    {'profile_name': p.profile_name, 'result_link': p.result_link, 'executor': p.executor,
                     'owner_name': p.owner_name,'tws_version': p.tws_version,
                     'sut': p.sut, 'result_status': p.result_status, 'controller': p.controller,
                     'create_At': p.create_At,
                     'trigger_id': p.trigger_id})
            responseObject = {
                'status': 'success',
                'data': results
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Unable to Fetch project.',
                'description': e
            }
            return make_response(jsonify(responseObject)), 500


class NickelProjectAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        project = NickelProject.query.filter_by(project_name=post_data.get('project_name')).first()
        if project is None:
            new_project = NickelProject(
                project_name=post_data.get('project_name'),
                creator=post_data.get('creator'),
                create_At=datetime.datetime.now()
            )
            try:
                db.session.add(new_project)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully Added Project.',
                    'project_id': new_project.project_id
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Could not save your Project.'
                }
                return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'success',
            'message': 'Project already exist'
        }
        return make_response(jsonify(responseObject)), 200

    def get(self):
        try:
            projects = NickelProject.query.all()
            results = []
            for p in projects:
                results.append({'project_id': p.project_id, 'project_name': p.project_name, 'creator': p.creator,
                                'create_at': p.create_At})
            responseObject = {
                'status': 'success',
                'data': results
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Unable to Fetch project.',
                'description': e
            }
            return make_response(jsonify(responseObject)), 500

    def delete(self):
        post_data = request.get_json()
        project = db.session.query(NickelProject).filter(
            NickelProject.project_id == post_data.get('project_id'))
        if project is not None:
            try:
                project.delete()
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'project  delete success'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Error while project  delete'
                }
                return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'success',
            'message': 'No project exist for delete'
        }
        return make_response(jsonify(responseObject)), 200


class NickelProjectProfileMapAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        mapping = db.session.query(NickelProjectProfile_Map).filter(
            NickelProjectProfile_Map.project_id == post_data.get('project_id'),
            NickelProjectProfile_Map.profile_id == post_data.get('profile_id')).first()
        if mapping is None:
            new_map = NickelProjectProfile_Map(
                project_id=post_data.get('project_id'),
                profile_id=post_data.get('profile_id'),
                creator=post_data.get('creator'),
                create_At=datetime.datetime.now(),
                owner_name=post_data.get('owner_name')
            )
            try:
                db.session.add(new_map)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully Added Mapping.'
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Could not save your Project.'
                }
                return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'success',
            'message': 'Mapping already exist'
        }
        return make_response(jsonify(responseObject)), 200

    def get(self):
        try:
            results = []
            for p, data, project in db.session.query(NickelProjectProfile_Map, NickelProfile, NickelProject).filter(
                    NickelProjectProfile_Map.profile_id == NickelProfile.profile_id,
                    NickelProjectProfile_Map.project_id == NickelProject.project_id).all():
                results.append(
                    {'profile_name': data.profile_name, 'profile_desc': data.profile_desc,
                     'build_number': data.build_number, 'choco_source': data.choco_source,
                     'share_path': data.share_path, 'share_uname': data.share_uname,
                     'share_pwd': data.share_pwd, 'kit_name': data.kit_name, 'ifwi_bin': data.ifwi_bin,
                     'wim_name': data.wim_name, 'flashing_method': data.flashing_method,
                     'execution_mode': data.execution_mode, 'execution_type': data.execution_type,
                     'network_type': data.network_type, 'imaging_type': data.imaging_type,
                     'sx_cycle_type': data.sx_cycle_type, 'sx_continue_on_fail': data.sx_continue_on_fail,
                     'sx_debug_arg': data.sx_debug_arg, 'sx_sleep_time': data.sx_sleep_time,
                     'sx_wake_mode': data.sx_wake_mode, 'sx_wake_time': data.sx_wake_time,
                     'ict_result_path': data.ict_result_path, 'tws_no_wait': data.tws_no_wait,
                     'wrapper_fanout': data.wrapper_fanout, 'power_mode': data.power_mode,
                     'isct_version': data.isct_version, 'execution_dir': data.execution_dir,
                     'install_dir': data.install_dir, 'group_name': data.group_name,
                     'owner_name': data.owner_name, 'wwid': data.owner, 'profile_id': data.profile_id,
                     'create_at': data.create_At, 'sx_cycling_count': data.sx_cycling_count,
                     'controller': data.controller, 'fanout_attr': data.fanout_attr,
                     'wimager_version': data.wimager_version,
                     'fanout_value': data.fanout_value, 'jarvis_pwd': data.jarvis_pwd,
                     'ifwi_flash_method_list': data.ifwi_flash_method_list,
                     'execution_mode_list': data.execution_mode_list,
                     'execution_type_list': data.execution_type_list,
                     'network_type_list': data.network_type_list,
                     'image_type_list': data.image_type_list, 'cycle_type_list': data.cycle_type_list,
                     'wake_mode_list': data.wake_mode_list, 'power_mode_list': data.power_mode_list,
                     'tws_version_list': data.tws_version_list,
                     'project_id': p.project_id, 'project_name': project.project_name})

            responseObject = {
                'status': 'success',
                'data': results
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Unable to Fetch provision.',
                'description': e
            }
            return make_response(jsonify(responseObject)), 500

    def delete(self):
        post_data = request.get_json()
        mapping = db.session.query(NickelProjectProfile_Map).filter(
            NickelProjectProfile_Map.project_id == post_data.get('project_id'),
            NickelProjectProfile_Map.profile_id == post_data.get('profile_id'))
        if mapping is not None:
            try:
                mapping.delete()
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Mapping  delete success'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Error while Mapping  delete'
                }
                return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'success',
            'message': 'No Mapping exist for delete'
        }
        return make_response(jsonify(responseObject)), 200


class NickelProfileAPI(MethodView):
    @staticmethod
    def prepare_list_data(list_data):
        res = None
        for val in list_data:
            if res is None:
                res = val
            else:
                res = res + "#" + val
        return res

    def post(self):
        post_data = request.get_json()
        operation_type = request.args['type']
        profile = NickelProfile(profile_name=post_data.get('profile_name'),
                                owner=post_data.get('owner'),
                                profile_desc=post_data.get('profile_desc'),
                                build_number=post_data.get('build_number'),
                                choco_source=post_data.get('choco_source'),
                                share_path=post_data.get('share_path'),
                                share_uname=post_data.get('share_uname'),
                                share_pwd=post_data.get('share_pwd'),
                                kit_name=post_data.get('kit_name'),
                                ifwi_bin=post_data.get('ifwi_bin'),
                                wim_name=post_data.get('wim_name'),
                                sx_continue_on_fail=post_data.get('sx_continue_on_fail'),
                                sx_debug_arg=post_data.get('sx_debug_arg'),
                                sx_sleep_time=post_data.get('sx_sleep_time'),
                                sx_wake_time=post_data.get('sx_wake_time'),
                                ict_result_path=post_data.get('ict_result_path'),
                                tws_no_wait=post_data.get('tws_no_wait'),
                                wrapper_fanout=post_data.get('wrapper_fanout'),
                                isct_version=post_data.get('isct_version'),
                                execution_dir=post_data.get('execution_dir'),
                                install_dir=post_data.get('install_dir'),
                                create_At=datetime.datetime.now(),
                                group_name=post_data.get('group_name'),
                                owner_name=post_data.get('owner_name'),
                                sx_cycling_count=post_data.get('sx_cycling_count'),
                                System_Provisioning=post_data.get('system_provisioning'),
                                FirmwareSKU=post_data.get('firmware_sku'),
                                tws_version=post_data.get('tws_version'),
                                controller=post_data.get('controller'),
                                fanout_attr=post_data.get('fanout_attr'),
                                wimager_version=post_data.get('wimager_version'),
                                fanout_value=post_data.get('fanout_value'),
                                jarvis_pwd=post_data.get('jarvis_pwd')
                                )
        # list add
        flash_method_list = post_data.get('ifwi_flash_method_list')
        execution_mode_list = post_data.get('execution_mode_list')
        execution_type_list = post_data.get('execution_type_list')
        network_type_list = post_data.get('network_type_list')
        image_type_list = post_data.get('image_type_list')
        cycle_type_list = post_data.get('cycle_type_list')
        wake_mode_list = post_data.get('wake_mode_list')
        power_mode_list = post_data.get('power_mode_list')
        tws_version_list = post_data.get('tws_version_list')
        if flash_method_list is not None and len(flash_method_list) > 0:
            if operation_type == 'new':
                profile.flashing_method = flash_method_list[0]
            else:
                profile.flashing_method = post_data.get('flashing_method')
            profile.ifwi_flash_method_list = NickelProfileAPI.prepare_list_data(
                flash_method_list) if operation_type == 'new' else flash_method_list

        if execution_mode_list is not None and len(execution_mode_list) > 0:
            if operation_type == 'new':
                profile.execution_mode = execution_mode_list[0]
            else:
                profile.execution_mode = post_data.get('execution_mode')

            profile.execution_mode_list = NickelProfileAPI.prepare_list_data(
                execution_mode_list) if operation_type == 'new' else execution_mode_list
        if execution_type_list is not None and len(execution_type_list) > 0:
            if operation_type == 'new':
                profile.execution_type = execution_type_list[0]
            else:
                profile.execution_type = post_data.get('execution_type')
            profile.execution_type_list = NickelProfileAPI.prepare_list_data(
                execution_type_list) if operation_type == 'new' else execution_type_list
        if network_type_list is not None and len(network_type_list) > 0:
            if operation_type == 'new':
                profile.network_type = network_type_list[0]
            else:
                profile.network_type = post_data.get('network_type')

            profile.network_type_list = NickelProfileAPI.prepare_list_data(
                network_type_list) if operation_type == 'new' else network_type_list
        if image_type_list is not None and len(image_type_list) > 0:
            if operation_type == 'new':
                profile.imaging_type = image_type_list[0]
            else:
                profile.imaging_type = post_data.get('imaging_type')
            profile.image_type_list = NickelProfileAPI.prepare_list_data(
                image_type_list) if operation_type == 'new' else image_type_list
        if cycle_type_list is not None and len(cycle_type_list) > 0:
            if operation_type == 'new':
                profile.sx_cycle_type = cycle_type_list[0]
            else:
                profile.sx_cycle_type = post_data.get('sx_cycle_type')
            profile.cycle_type_list = NickelProfileAPI.prepare_list_data(
                cycle_type_list) if operation_type == 'new' else cycle_type_list
        if wake_mode_list is not None and len(wake_mode_list) > 0:
            if operation_type == 'new':
                profile.sx_wake_mode = wake_mode_list[0]
            else:
                profile.sx_wake_mode = post_data.get('sx_wake_mode')
            profile.wake_mode_list = NickelProfileAPI.prepare_list_data(
                wake_mode_list) if operation_type == 'new' else wake_mode_list
        if power_mode_list is not None and len(power_mode_list) > 0:
            if operation_type == 'new':
                profile.power_mode = power_mode_list[0]
            else:
                profile.power_mode = post_data.get('power_mode')
            profile.power_mode_list = NickelProfileAPI.prepare_list_data(
                power_mode_list) if operation_type == 'new' else power_mode_list

        if tws_version_list is not None and len(tws_version_list) > 0:
            if operation_type == 'new':
                profile.tws_version = tws_version_list[0]
            else:
                profile.tws_version = post_data.get('tws_version')
            profile.tws_version_list = NickelProfileAPI.prepare_list_data(
                tws_version_list) if operation_type == 'new' else tws_version_list

        try:
            db.session.add(profile)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully Added Profile.'
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'Fail',
                'message': 'Could not save your profile.'
            }
            return make_response(jsonify(responseObject)), 500

    def patch(self):
        post_data = request.get_json()
        profile = NickelProfile.query.filter_by(profile_id=post_data.get('profile_id')).one()
        if profile:
            profile.profile_name = post_data.get('profile_name')
            profile.owner = post_data.get('owner')
            profile.profile_desc = post_data.get('profile_desc')
            profile.build_number = post_data.get('build_number')
            profile.choco_source = post_data.get('choco_source')
            profile.share_path = post_data.get('share_path')
            profile.share_uname = post_data.get('share_uname')
            profile.share_pwd = post_data.get('share_pwd')
            profile.kit_name = post_data.get('kit_name')
            profile.ifwi_bin = post_data.get('ifwi_bin')
            # profile.flashing_method = post_data.get('flashing_method')
            # profile.execution_mode = post_data.get('execution_mode')
            # profile.execution_type = post_data.get('execution_type')
            # profile.network_type = post_data.get('network_type')
            # profile.imaging_type = post_data.get('imaging_type')
            # profile.sx_cycle_type = post_data.get('sx_cycle_type')
            profile.sx_continue_on_fail = post_data.get('sx_continue_on_fail')
            profile.sx_debug_arg = post_data.get('sx_debug_arg')
            profile.sx_sleep_time = post_data.get('sx_sleep_time')
            # profile.sx_wake_mode = post_data.get('sx_wake_mode')
            profile.sx_wake_time = post_data.get('sx_wake_time')
            profile.ict_result_path = post_data.get('ict_result_path')
            profile.tws_no_wait = post_data.get('tws_no_wait')
            profile.wrapper_fanout = post_data.get('wrapper_fanout')
            # profile.power_mode = post_data.get('power_mode')
            profile.isct_version = post_data.get('isct_version')
            profile.install_dir = post_data.get('install_dir')
            profile.group_name = post_data.get('group_name')
            profile.owner_name = post_data.get('owner_name')
            profile.sx_cycling_count = post_data.get('sx_cycling_count')
            profile.System_Provisioning = post_data.get('system_provisioning')
            profile.FirmwareSKU = post_data.get('firmware_sku')
            profile.tws_version = post_data.get('tws_version')

            profile.controller = post_data.get('controller')
            profile.fanout_attr = post_data.get('fanout_attr')
            profile.wimager_version = post_data.get('wimager_version')
            profile.fanout_value = post_data.get('fanout_value')
            profile.jarvis_pwd = post_data.get('jarvis_pwd')

            # list add
            flash_method_list = post_data.get('ifwi_flash_method_list')
            execution_mode_list = post_data.get('execution_mode_list')
            execution_type_list = post_data.get('execution_type_list')
            network_type_list = post_data.get('network_type_list')
            image_type_list = post_data.get('image_type_list')
            cycle_type_list = post_data.get('cycle_type_list')
            wake_mode_list = post_data.get('wake_mode_list')
            power_mode_list = post_data.get('power_mode_list')
            tws_version_list = post_data.get('tws_version_list')
            if flash_method_list is not None and len(flash_method_list) > 0:
                profile.flashing_method = flash_method_list[0]
                profile.ifwi_flash_method_list = NickelProfileAPI.prepare_list_data(flash_method_list)

            if execution_mode_list is not None and len(execution_mode_list) > 0:
                profile.execution_mode = execution_mode_list[0]
                profile.execution_mode_list = NickelProfileAPI.prepare_list_data(execution_mode_list)

            if execution_type_list is not None and len(execution_type_list) > 0:
                profile.execution_type = execution_type_list[0]
                profile.execution_type_list = NickelProfileAPI.prepare_list_data(execution_type_list)

            if network_type_list is not None and len(network_type_list) > 0:
                profile.network_type = network_type_list[0]
                profile.network_type_list = NickelProfileAPI.prepare_list_data(network_type_list)

            if image_type_list is not None and len(image_type_list) > 0:
                profile.imaging_type = image_type_list[0]
                profile.image_type_list = NickelProfileAPI.prepare_list_data(image_type_list)

            if cycle_type_list is not None and len(cycle_type_list) > 0:
                profile.sx_cycle_type = cycle_type_list[0]
                profile.cycle_type_list = NickelProfileAPI.prepare_list_data(cycle_type_list)

            if wake_mode_list is not None and len(wake_mode_list) > 0:
                profile.sx_wake_mode = wake_mode_list[0]
                profile.wake_mode_list = NickelProfileAPI.prepare_list_data(wake_mode_list)

            if power_mode_list is not None and len(power_mode_list) > 0:
                profile.power_mode = power_mode_list[0]
                profile.power_mode_list = NickelProfileAPI.prepare_list_data(power_mode_list)

            if tws_version_list is not None and len(tws_version_list) > 0:
                profile.tws_version = tws_version_list[0]
                profile.tws_version_list = NickelProfileAPI.prepare_list_data(tws_version_list)


            try:
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully Updated Profile.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Profile update failure'
                }
                return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'success',
            'message': 'No Profile found for update'
        }
        return make_response(jsonify(responseObject)), 200

    def get(self):
        try:
            results = []
            for data in db.session.query(NickelProfile).all():
                results.append({'profile_name': data.profile_name, 'profile_desc': data.profile_desc,
                                'build_number': data.build_number, 'choco_source': data.choco_source,
                                'share_path': data.share_path, 'share_uname': data.share_uname,
                                'share_pwd': data.share_pwd, 'kit_name': data.kit_name, 'ifwi_bin': data.ifwi_bin,
                                'wim_name': data.wim_name, 'flashing_method': data.flashing_method,
                                'execution_mode': data.execution_mode, 'execution_type': data.execution_type,
                                'network_type': data.network_type, 'imaging_type': data.imaging_type,
                                'sx_cycle_type': data.sx_cycle_type, 'sx_continue_on_fail': data.sx_continue_on_fail,
                                'sx_debug_arg': data.sx_debug_arg, 'sx_sleep_time': data.sx_sleep_time,
                                'sx_wake_mode': data.sx_wake_mode, 'sx_wake_time': data.sx_wake_time,
                                'ict_result_path': data.ict_result_path, 'tws_no_wait': data.tws_no_wait,
                                'wrapper_fanout': data.wrapper_fanout, 'power_mode': data.power_mode,
                                'isct_version': data.isct_version, 'execution_dir': data.execution_dir,
                                'install_dir': data.install_dir, 'group_name': data.group_name,
                                'owner_name': data.owner_name, 'wwid': data.owner, 'profile_id': data.profile_id,
                                'create_at': data.create_At, 'sx_cycling_count': data.sx_cycling_count,

                                'ifwi_flash_method_list': data.ifwi_flash_method_list,
                                'execution_mode_list': data.execution_mode_list,
                                'execution_type_list': data.execution_type_list,
                                'network_type_list': data.network_type_list,
                                'image_type_list': data.image_type_list, 'cycle_type_list': data.cycle_type_list,
                                'wake_mode_list': data.wake_mode_list, 'power_mode_list': data.power_mode_list,
                                'tws_version_list': data.tws_version_list,
                                'system_provisioning': data.System_Provisioning, 'firmware_sku': data.FirmwareSKU,
                                'tws_version': data.tws_version,
                                'controller': data.controller, 'fanout_attr': data.fanout_attr,
                                'wimager_version': data.wimager_version,
                                'fanout_value': data.fanout_value, 'jarvis_pwd': data.jarvis_pwd
                                })
            db.session.commit()
            responseObject = {
                'status': 'success',
                'profiles': results
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error while Profile fetch'
            }
            return make_response(jsonify(responseObject)), 500

    def delete(self):
        data = request.args
        profile_id = data['profile_id']
        try:
            NickelProfile.query.filter_by(profile_id=profile_id).delete()
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'profile delete success',
                'profile_id': profile_id
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Error while Profile delete'
            }
            return make_response(jsonify(responseObject)), 500


class NickelExecution(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            db.session.add_all(post_data)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully Added Nickel Execution.'
            }
            return make_response(jsonify(responseObject)), 201
        except:
            responseObject = {
                'status': 'Fail',
                'message': 'Could not save your profile.'
            }
            return make_response(jsonify(responseObject)), 500


oap_nickel_blueprint = Blueprint('oap_nickel', __name__)
nickel_project_view = NickelProjectAPI.as_view('nickel_project_view')
nickel_profile_view = NickelProfileAPI.as_view('nickel_profile_view')
nickel_profile_project_mapping_view = NickelProjectProfileMapAPI.as_view('nickel_profile_project_mapping_view')
nickel_execution_view = NickelExecution.as_view('nickel_execution_view')
nickel_result_view = NickelResultAPI.as_view('nickel_result_view')
oap_nickel_blueprint.add_url_rule(
    '/oap/nic/project',
    view_func=nickel_project_view,
    methods=['GET', 'POST', 'DELETE']
)
oap_nickel_blueprint.add_url_rule(
    '/oap/nic/project-profile-map',
    view_func=nickel_profile_project_mapping_view,
    methods=['GET', 'POST', 'DELETE']
)
oap_nickel_blueprint.add_url_rule(
    '/oap/nic/profile',
    view_func=nickel_profile_view,
    methods=['GET', 'POST', 'PATCH', 'DELETE']
)
oap_nickel_blueprint.add_url_rule(
    '/oap/nic/execution',
    view_func=nickel_execution_view,
    methods=['GET', 'POST']
)
oap_nickel_blueprint.add_url_rule(
    '/oap/nic/result',
    view_func=nickel_result_view,
    methods=['GET', 'POST', 'PATCH']
)
