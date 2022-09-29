#!/usr/bin/env python

import os
import pprint as pp
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import redirect, request, session, url_for, Blueprint, make_response, jsonify

from project.common import iamws

# Load environmental variables
env_path = Path.cwd() / ".env"
load_dotenv(dotenv_path=env_path)

# IAM WS endpoint for internal app development
BASE_URL_IAMWS_INT_DEV = os.environ.get('IAMWS', '')

# generic account used to run the app -- see vars-template.yml file
SYS_APP = os.environ.get('SYS_APP', '')  # you can use a temporary developer sys_ account, like this one
SYS_PWD = os.environ.get('SYS_PWD', '')

# avoid InsecureRequestWarning warnings about Unverified HTTPS request
requests.packages.urllib3.disable_warnings()

# this is a service that we instantiate for use across the whole app
iamws_service = iamws.Iamws(BASE_URL_IAMWS_INT_DEV)

SSO_APP = Blueprint('authsso', __name__, url_prefix='/authsso')


@SSO_APP.route('/user', methods=['GET', 'POST'])
def getUserDetails():
    post_data = request.get_json()
    client_token = post_data.get('token')
    print(client_token)
    access_token_response = iamws_service.get_access_token(SYS_APP, SYS_PWD)
    access_token = access_token_response.access_token
    print(access_token)
    # Add Validation
    user_data = iamws_service.get_user_data(client_token, access_token)
    print('user_data:\n', pp.pformat(user_data))

    #
    user_displayname = user_data.get('displayName')
    if user_displayname is None:
        session['username'] = '''
                unidentified user. 
                The generic user managing this App could not get the displayName for the
                logged user.
                Please call for support.
            '''
        print('user_data:', user_data)  # this will have more detailed information
        response = jsonify({'user_data': user_data,
                            'message': 'unidentified user.The generic user managing this App could not get the '
                                       'displayName for the logged  user.Please call for support.'})
        return make_response(response
                             ), 500

    session['username'] = user_displayname

    user_id = user_data.get('id')
    if user_id is None:
        session['username'] = '''
                unidentified user. 
                The generic user managing this App could not get the id for the logged 
                user.Please call for support.
            '''
        print('user_data:', user_data)  # this will have more detailed information
        response = jsonify({'user_data': user_data,
                            'message': 'unidentified user.The generic user managing this App could not get the id for'
                                       'for the logged  user.Please call for support.'})
        return make_response(response
                             ), 500

    memberships = [
        {
            "name": "CN=O365Prog-Group creation,OU=Managed,OU=Groups,DC=amr,DC=corp,DC=intel,DC=com",
            "type": "CORPAD",
        },
        {
            "name": "CN=CCG Cloud Admin,OU=Managed,OU=Groups,DC=amr,DC=corp,DC=intel,DC=com",
            "type": "CORPAD",
        }
    ]

    user_memberships = iamws_service.verify_memberships(user_id, access_token, memberships)
    print('User Memberships : ', user_memberships)
    session['user_data'] = user_data
    session['memberships'] = user_memberships

    print('user_memberships:\n', pp.pformat(user_memberships))
    print('session membership :\n', session['memberships'])

    # return redirect(url_for('auth.index', _external=True))
    response = jsonify({'user_data': session.get('user_data'), 'memberships': session.get('memberships')})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return make_response(response
                         ), 200


@SSO_APP.route('/')
def index():
    if session.get('username'):
        # we have already authenticated and authorized the user
        # return {'user_data': session.get('user_data'), 'memberships': session.get('memberships')}
        response = jsonify({'user_data': session.get('user_data'), 'memberships': session.get('memberships')})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return make_response(response
                             ), 200
    else:
        # we need to identify and authenticate the user

        # first, we gather the URL that will be used to request a token representing the incoming, logged user
        win_auth_endp = iamws_service.get_windows_auth_endp()
        # print('win_auth_endp:', win_auth_endp)

        # we then form the redirect URL to request the user token
        # and have it sent back to us as a new http request onto our own /sso
        # endpoint
        sso_url = url_for('authsso.sso', _external=True)
        redirect_url = win_auth_endp + '?redirecturl=' + sso_url
        print('redirect_url:', redirect_url)

        # finally, we ask Flask to command the browser to navigate to the URL
        # where the request for the token will be made
        return redirect(redirect_url)


@SSO_APP.route('/sso')
def sso():
    # at this point, we should be receiving the (redirected) reply from the URL used
    # to request the user token
    # here we are hit with a POST http request, so we pull the token from its
    # arguments
    user_token = request.args.get('token')
    print('user_token:\n', user_token)

    # now we ask for a "bearer" or "access" token for the sys_app generic user used
    # to control access to this app
    # this token will convey the identification of the sys_app generic user
    # plus a confirmation of the authorized API endpoint scopes to be used
    # the get_access_token method has a default list of scopes
    # (scope='Token_WindowsAuth Authorization')
    # indicating that we want to use the bearer token to authenticate a user and to
    # check for his/her Authorizations
    access_token_response = iamws_service.get_access_token(SYS_APP, SYS_PWD)
    access_token = access_token_response.access_token
    print('access_token:', access_token)
    expires_in = access_token_response.expires_in
    print('expires_in:', expires_in)

    if access_token is None:
        session['username'] = '''
            unidentified user. 
            The generic user managing this App did not get an IAM access token.
            Please call for support.
        '''
        print('access_token:', access_token)  # this will have more detailed information
        return redirect(url_for('authsso.index', _external=True))

    # if all went well so far, we can now use the access_token
    # to retrieve descriptive data for the user sending us http requests
    user_data = iamws_service.get_user_data(user_token, access_token)
    print('user_data:\n', pp.pformat(user_data))

    #
    user_displayname = user_data.get('displayName')
    if user_displayname is None:
        session['username'] = '''
            unidentified user. 
            The generic user managing this App could not get the displayName for the
            logged user.
            Please call for support.
        '''
        print('user_data:', user_data)  # this will have more detailed information
        return redirect(url_for('authsso.index', _external=True))

    session['username'] = user_displayname

    user_id = user_data.get('id')
    if user_id is None:
        session['username'] = '''
            unidentified user. 
            The generic user managing this App could not get the id for the logged 
            user.Please call for support.
        '''
        print('user_data:', user_data)  # this will have more detailed information
        return redirect(url_for('authsso.index', _external=True))

    memberships = [
        {
            "name": "CN=O365Prog-Group creation,OU=Managed,OU=Groups,DC=amr,DC=corp,DC=intel,DC=com",
            "type": "CORPAD",
        },
        {
            "name": "CN=CCG Cloud Admin,OU=Managed,OU=Groups,DC=amr,DC=corp,DC=intel,DC=com",
            "type": "CORPAD",
        }
    ]

    user_memberships = iamws_service.verify_memberships(user_id, access_token, memberships)
    print('User Memberships : ', user_memberships)
    session['user_data'] = user_data
    session['memberships'] = user_memberships

    print('user_memberships:\n', pp.pformat(user_memberships))
    print('session membership :\n', session['memberships'])

    # return redirect(url_for('auth.index', _external=True))
    response = jsonify({'user_data': session.get('user_data'), 'memberships': session.get('memberships')})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return make_response(response
                         ), 200
