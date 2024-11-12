import logging
from flask import Blueprint, request, session, jsonify
from oauth.twitchclass import OauthFacade, extract_twitch_info, TwitchUserService
from flask_login import current_user, login_required
from auth.auth import _login_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth = Blueprint("oauth", __name__, template_folder='templates/oauth')
oauth_obj = OauthFacade(response_type="code",
                        scope=["user:read:email", "user:read:broadcast", "moderator:read:followers",
                               "user:read:follows"])


@oauth.route('/api/v1/callback')
def callback():
    """
       OAuth callback for handling the authentication response
       ---
       description: This endpoint processes the OAuth callback, handling the returned code or error, and managing user authentication and getting the access token.
       parameters:
         - name: code
           in: query
           description: The OAuth authorization code received from the OAuth provider.
           required: false
           schema:
             type: string
         - name: state
           in: query
           description: The state parameter returned from the OAuth provider, to ensure the request is valid.
           required: false
           schema:
             type: string
         - name: scope
           in: query
           description: The scope of access requested during OAuth authentication.
           required: false
           schema:
             type: string
         - name: error
           in: query
           description: Error message if the authentication fails.
           required: false
           schema:
             type: string
         - name: error_description
           in: query
           description: Description of the error returned by the OAuth provider.
           required: false
           schema:
             type: string
       responses:
         301:
           description: Successfully authenticated and logged in the user and redirects to the home page.
           content:
             text/html:
               schema:
                 type: string
                 example: "Redirecting to the homepage..."
         401:
           description: Authentication failed due to invalid or missing data.
           content:
             text/html:
               schema:
                 type: string
                 example: "Authentication failed"
         400:
           description: Invalid callback request with no valid parameters.
           content:
             text/html:
               schema:
                 type: string
                 example: "Invalid request"
       """

    code = request.args.get('code', default=None)
    state = request.args.get('state', default=None)
    scope = request.args.get('scope', default=None)
    error = request.args.get('error', default=None)
    error_description = request.args.get('error_description', default=None)
    if code:
        data = {'code': code, 'state': state, 'scope': scope}
        try:
            access_token = oauth_obj.get_access_token(data=data)
            session['oauth_token_data'] = access_token
            return _login_user()
        except Exception as e:
            logger.error(f'failed token handling: {e}')
            return jsonify('Failed Authentication'), 401

    elif error:
        data = {'error': error, 'error_description': error_description, 'state': state}
        try:
            oauth_obj.get_access_token(**data)
            return jsonify('Failed Authentication'), 401
        except Exception as e:
            logger.error(e)
            return jsonify('error'), 400
    else:
        return jsonify('invalid'), 400


# TODO : properly write this status codes.

@oauth.get('/api/v1/get_followed')
@login_required
def get_followed():
    """
        Get the list of followed users on Twitch.
        ---
        description: This endpoint retrieves the list of users that the currently authenticated user is following on Twitch.
        security:
          - oauth2: []
        responses:
          200:
            description: A list of followed users.
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        description: The Twitch ID of the followed user.
                        example: "123456789"
                      name:
                        type: string
                        description: The name of the followed user.
                        example: "gamer123"
          401:
            description: Unauthorized. The user is not authenticated.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Unauthorized"
          500:
            description: Internal server error. Something went wrong while retrieving followed data.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Failed to retrieve followed users."
        """
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    following_data = twitch_user.get_followed(user_id)
    return following_data


# TODO :change the database schema or find a way to access the access token


@oauth.get('/api/v1/get_followers')
@login_required
def get_followers():
    """
      Get the list of followers on Twitch.
      ---
      description: This endpoint retrieves the list of users who follow the currently authenticated user on Twitch.
      security:
        - oauth2: []
      responses:
        200:
          description: A list of followers.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: string
                      description: The Twitch ID of the follower.
                      example: "987654321"
                    name:
                      type: string
                      description: The name of the follower.
                      example: "streamer456"
        401:
          description: Unauthorized. The user is not authenticated.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Unauthorized"
        500:
          description: Internal server error. Something went wrong while retrieving follower data.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: "Failed to retrieve followers."
      """
    user_id = current_user.id
    access_token = current_user.access_token
    twitch_user = TwitchUserService(access_token=access_token)
    followers_data = twitch_user.get_followers(user_id)
    return followers_data
# TODO : change the database schema or find a way to access the access token
# TODO: write an endpoint for token validation.
