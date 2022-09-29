#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
    This files implements a service to access
    Intel IAM WS-I API

    re:
        [IAM Web Services User Community](https://soco.intel.com/groups/iam-ws)
        [IAM WS-I API Contract](http://goto.intel.com/iamws)
"""

from collections import namedtuple

import requests
from requests.auth import HTTPBasicAuth

# endpoint for the internal development instance of the IAM WS
BASE_URL_IAMWS_INT_DEV = "https://iamws-i.intel.com/api/v1"

# namedtuple subclass to return access tokens
Access_token = namedtuple('Access_token', ['access_token', 'expires_in', 'status', 'message'])


class Iamws(object):
    ENDP_WINDOWS_AUTH = '/windows/auth'
    ENDP_TOKEN = '/token'
    ENDP_AUTHORIZATIONS = '/Authorizations'

    def __init__(self, base_url=BASE_URL_IAMWS_INT_DEV):
        self._base_url = base_url

    def get_windows_auth_endp(self):
        """ return the endpoint to redirect not yet authorized requests """
        return self._base_url + self.ENDP_WINDOWS_AUTH

    def get_access_token(self, client_id, client_secret, scope='Token_WindowsAuth Authorization User_Read'):
        """ get a token that can be used to retrieve user data or validate scope entitlements (authorizations) """

        payload = {
            'grant_type': 'client_credentials',
            'scope': scope
        }

        # Setting 'verify=False' because otherwise the request fails on
        # certificate verification:
        # SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
        response = requests.post(
            self._base_url + self.ENDP_TOKEN,
            auth=HTTPBasicAuth(client_id, client_secret),
            data=payload,
            verify=False
        )
        print('get_access_token response: ', response.text)
        if response.status_code == requests.codes.ok:
            response_obj = response.json()
            access_token = Access_token(response_obj['access_token'], response_obj['expires_in'], response.status_code,
                                        'OK')
        else:
            access_token = Access_token(None, 0, response.status_code, 'response.text:' + response.text)
        return access_token

    def get_user_data(self, user_token, access_token):
        """ get descriptive data for the user sending requests to the app """
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        payload = {
            'token': user_token
        }

        # Setting 'verify=False' because otherwise the request fails on
        # certificate verification:
        # SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
        response = requests.post(
            self._base_url + self.ENDP_WINDOWS_AUTH,
            headers=headers,
            json=payload,
            verify=False
        )
        if response.status_code == requests.codes.ok:
            user_data = response.json()['IntelUserExtension']
        else:
            user_data = {"response.status_code": response.status_code, "response.text": + response.text}

        return user_data

    def verify_memberships(self, user_id, access_token, memberships=[]):
        """ verify authorizations fo the user sending requests to the app """
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        payload = {
            'enterpriseId': user_id,
            'memberships': memberships,
            'schemas': ['urn:scim:schemas:extension:intelauthorization:1.0']
        }

        # Setting 'verify=False' because otherwise the request fails on
        # certificate verification:
        # SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
        response = requests.post(
            self._base_url + self.ENDP_AUTHORIZATIONS,
            headers=headers,
            json=payload,
            verify=False
        )

        # print('verify_memberships response:\n', pp.pformat(response.text))
        if response.status_code == requests.codes.ok:
            verifications = response.json()['memberships']
        else:
            verifications = {"response.status_code": response.status_code, "response.text": response.text}

        return verifications
