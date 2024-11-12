from email.policy import default
import logging
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from oauth.twitchclass import OauthFacade, extract_twitch_info, TwitchUserService
import json
from flask_login import current_user, login_required
from auth.auth import _login_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth = Blueprint("oauth", __name__, template_folder='templates/oauth')
oauth_obj = OauthFacade(response_type="code",
                        scope=["user:read:email", "user:read:broadcast", "moderator:read:followers",
                               "user:read:follows"])


@oauth.route('/callback')
def callback():
    code = request.args.get('code' ,default = None)
    state = request.args.get('state',default = None)
    scope = request.args.get('scope',default = None)
    error = request.args.get('error',default = None)
    error_description = request.args.get('error_description',default = None)
    if code:
        data = {'code': code, 'state': state, 'scope': scope}
        try:
            access_token = oauth_obj.get_access_token(data=data)
            session['oauth_token_data'] = access_token
            return _login_user()
        except Exception as e:
            logger.error(f'failed token handling: {e}')
            return jsonify('Failed Authentication'),401

    elif error:
        data = {'error': error, 'error_description': error_description, 'state': state}
        try:
            oauth_obj.get_access_token(**data)
            return 'Failed Authentication',200
        except Exception as e:
            logger.error(e)
            return 'Failed Authentication', 401
    else:
        return jsonify('invalid'),401
# TODO : properly write this status codes.

@oauth.get('/get_followed')
@login_required
def get_followed():
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    following_data = twitch_user.get_followed(user_id)
    return following_data
# TODO :change the database schema or find a way to access the access token


@oauth.get('/get_followers')
@login_required
def get_followers():
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    followers_data = twitch_user.get_followers(user_id)
    return followers_data
# TODO : change the database schema or find a way to access the access token