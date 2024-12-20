import json
import logging

from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, url_for, redirect, session, render_template
from flask_login import login_user, logout_user,current_user
from oauth.twitchclass import TwitchUserService, extract_twitch_info, OauthFacade
from models import User,db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__, template_folder="templates/auth", static_folder="static")
oauth_obj = OauthFacade(response_type="code",
                        scope=["user:read:email", "user:read:broadcast", "moderator:read:followers",
                               "user:read:follows"])


def _login_user():
    oauth_data = session.get('oauth_token_data')
    if not oauth_data:
        logger.error("No OAuth data found in session.")
        return redirect(url_for('auth.login_get'))

    access_token = oauth_data.get('access_token')
    refresh_token = oauth_data.get('refresh_token')

    try:
        twitch_user = TwitchUserService(access_token=access_token)
        twitch_user_data = twitch_user.get_user_details()
    except Exception as e:
        logger.error(f"Error fetching user details from Twitch: {e}")
        return redirect(url_for('auth.login_get'))

    user_id = extract_twitch_info(twitch_user_data, 'id')
    username = extract_twitch_info(twitch_user_data, 'display_name')
    email = extract_twitch_info(twitch_user_data, 'email')
    profile_image_url = extract_twitch_info(twitch_user_data, 'profile_image_url')

    logger.info(f"Fetched user details: {username}, {user_id}, {email}, {profile_image_url}")

    existing_user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()

    if existing_user:
        login_user(existing_user)
        session.permanent = True
        logger.info(f"User logged in: {existing_user.username}")
        logger.info(f"Current user: {current_user.username}")
        logger.info(f"Is authenticated: {current_user.is_authenticated}")
        return redirect(url_for('main.home'))

    new_user = User(
        id=user_id,
        username=username,
        email=email,
        token_data=json.dumps(oauth_data),
        profile_image_url=profile_image_url,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        session.permanent = True
    except SQLAlchemyError as e:
        logger.error(f"Database error while adding new user: {e}")
        db.session.rollback()
        return redirect(url_for('auth.login_get'))
    except Exception as e:
        logger.error(f"Unexpected error while adding new user: {e}")
        db.session.rollback()
        return redirect(url_for('auth.login_get'))

    return redirect(url_for('main.home'))


@auth.get('/api/v1/login')
def login_get():
    """
       Get the OAuth login link
       ---
       description: This endpoint generates an OAuth login link for user authentication.
       responses:
         200:
           description: Renders the signup page with the OAuth login link.
           content:
             text/html:
               schema:
                 type: string
                 example: "<html>...signup page content...</html>"
       """
    auth_instance = oauth_obj
    auth_link = auth_instance.get_auth_link()
    return render_template('signup.html', auth_link=auth_link)

#TODO : write refresh token route

@auth.route('/api/v1/logout')
def logout():
    """
        Logout the current user
        ---
        description: This endpoint logs out the current user by ending their session and redirecting to the login page.
        responses:
          302:
            description: Redirects the user to the login page after logging out.
            content:
              text/html:
                schema:
                  type: string
                  example: "Redirecting to /login..."
        """
    logout_user()
    return redirect(url_for('auth.login_get'))
