from flask import Blueprint, render_template, redirect, url_for, request, session
from oauth.twitchclass import OauthFacade, extract_twitch_info, TwitchUserService
import json
from flask_login import current_user, login_required
from auth.auth import _login_user
oauth = Blueprint("oauth", __name__, template_folder='templates/oauth')
oauth_obj = OauthFacade(response_type="code",
                        scope=["user:read:email", "user:read:broadcast", "moderator:read:followers",
                               "user:read:follows"])


@oauth.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    scope = request.args.get('scope')
    error = request.args.get('error')
    error_description = request.args.get('error_description')
    if code:
        data = {'code': code, 'state': state, 'scope': scope}
        access_token = oauth_obj.get_access_token(data=data)
        session['oauth_token_data'] = access_token
        return _login_user()
    elif error:
        data = {'error': error, 'error_description': error_description, 'state': state}
        oauth_obj.get_access_token(**data)
        return 'Failed Authentication'


@oauth.get('/get_followed')
@login_required
def get_followed():
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    following_data = twitch_user.get_followed(user_id)
    return following_data


@oauth.get('/get_followers')
@login_required
def get_followers():
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    followers_data = twitch_user.get_followers(user_id)
    return followers_data
