from abc import abstractmethod, ABC
import http.client
from http.client import HTTPException
from urllib.parse import quote, urlencode
from uuid import uuid4, UUID
from typing import Union, Dict, Any
import os
from dotenv import load_dotenv
import json

load_dotenv()


class TwitchOauthBase(ABC):
    @abstractmethod
    def validate_token(self, access_token):
        ...

    @abstractmethod
    def authorize(self, authorize_obj):
        ...

    @abstractmethod
    def get_redirect_data(self, code, scope, state):
        ...

    @abstractmethod
    def get_token(self, authorize_obj):
        ...

    @abstractmethod
    def refresh_access_token(self):
        ...


class Authorization:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, response_type: str, scope: list[str],
                 state: UUID = uuid4()):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._response_type = response_type
        self._scope = scope
        self._state = state.hex
        self._code = Union[str, None]
        self._error = Union[str, None]
        self._description = Union[str, None]
        self._grant_type = 'authorization_code'
        self._access_token = Union[str, None]

    @property
    def client_id(self) -> str:
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def client_secret(self) -> str:
        return self._client_secret

    @client_secret.setter
    def client_secret(self, value):
        self._client_secret = value

    @property
    def redirect_uri(self) -> str:
        return self._redirect_uri

    @redirect_uri.setter
    def redirect_uri(self, value):
        self._redirect_uri = value

    @property
    def response_type(self) -> str:
        return self._response_type

    @response_type.setter
    def response_type(self, value):
        self._response_type = value

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def scope(self) -> str:
        scope_string = ' '.join(self._scope)
        encoded_scope_string = quote(scope_string)
        return encoded_scope_string

    @scope.setter
    def scope(self, value):
        self._scope = value

    @property
    def code(self) -> Union[str, None]:
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def grant_type(self) -> str:
        return self._grant_type

    @grant_type.setter
    def grant_type(self, value):
        self._grant_type = value

    @property
    def error(self) -> Union[str, None]:
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def description(self) -> Union[str, None]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def access_token(self) -> Union[str, None]:
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value


class TwitchOauthAccessCode(TwitchOauthBase):
    base_url = 'id.twitch.tv'

    def __init__(self):
        self.conn = http.client.HTTPSConnection(TwitchOauthAccessCode.base_url)

    def validate_token(self, access_token: str):
        endpoint = 'oauth2/validate'
        header = {'Authorization': f'OAUTH {access_token}'}
        self.conn.request("GET", endpoint, headers=header)

    def authorize(self, authorize_obj: Authorization):
        endpoint = 'https://id.twitch.tv/oauth2/authorize'
        query = f'?response_type={authorize_obj.response_type}&client_id={authorize_obj.client_id}&redirect_uri={authorize_obj.redirect_uri}' \
                f'&scope={authorize_obj.scope}&state={authorize_obj.state}'
        return endpoint + query

    def get_redirect_data(self, authorize_obj: Authorization, **kwargs):
        try:
            access_code = kwargs['data']['code']
            state = kwargs['data']['state']
            authorize_obj.code = access_code
            authorize_obj.state = state

        except KeyError:
            error = kwargs['data']['error']
            error_description = kwargs['data']['error_description']
            state = kwargs['data']['state']
            authorize_obj.error = error
            authorize_obj.description = error_description
            authorize_obj.state = state

    def get_token(self, authorize_obj: Authorization):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        endpoint = '/oauth2/token'
        body = {'client_id': authorize_obj.client_id, 'client_secret': authorize_obj.client_secret,
                'code': authorize_obj.code, 'grant_type': authorize_obj.grant_type,
                'redirect_uri': authorize_obj.redirect_uri}
        encoded_params = urlencode(body)
        try:
            self.conn.request('POST', endpoint, body=encoded_params, headers=headers)
            res = self.conn.getresponse()

            if res.status != 200:
                raise HTTPException(f"Error {res.status}: {res.reason}")

            data = res.read()
            json_data = json.loads(data.decode('utf-8'))

            access_token = json_data.get('access_token')
            if access_token is None:
                raise ValueError("Access token not found in the response")

            authorize_obj.access_token = access_token
            return json_data

        except HTTPException as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

        # TODO: store access_token and refresh_token in database.

    def refresh_access_token(self, authorize_obj):
        # write a query to get the stored refresh token
        refresh_token = ...  # Retrieve from storage
        endpoint = '/oauth2/token'
        body = {
            'client_id': authorize_obj.client_id,
            'client_secret': authorize_obj.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        json_body = json.dumps(body)
        self.conn.request('POST', endpoint, body=json_body)
        res = self.conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode('utf-8'))
        access_token = json_data['access_token']
        authorize_obj.access_token = access_token
        return json_data


class OauthFacade:
    twitch_client_id = os.getenv('TWITCH_CLIENT_ID')
    twitch_client_secret = os.getenv('TWITCH_CLIENT_SECRET_KEY')
    twitch_redirect_uri = os.getenv('TWITCH_REDIRECT_URI')
    if not all([twitch_client_id, twitch_client_secret, twitch_redirect_uri]):
        raise EnvironmentError("Missing required environment variables for Twitch OAuth.")

    def __init__(self, response_type: str = None, scope: list = None):
        self.response_type = response_type
        self.scope = scope
        self.authorize_obj = Authorization(
            client_id=OauthFacade.twitch_client_id,
            client_secret=OauthFacade.twitch_client_secret,
            redirect_uri=OauthFacade.twitch_redirect_uri,
            response_type=self.response_type,
            scope=scope
        )
        self.client = TwitchOauthAccessCode()

    def get_auth_link(self):
        authorization_url = self.client.authorize(authorize_obj=self.authorize_obj)
        return authorization_url

    def _get_access_code(self, **kwargs):
        self.client.get_redirect_data(authorize_obj=self.authorize_obj, data=kwargs['data'])

    def get_access_token(self, **kwargs):

        if kwargs['data'].get('code'):
            self._get_access_code(data=kwargs['data'])
            access_token_data = self.client.get_token(authorize_obj=self.authorize_obj)
            return access_token_data
        else:
            self._get_access_code(data=kwargs['data'])
            return {'msg': 'authorization failed'}

    def refresh_token(self):
        self.client.refresh_access_token(self.authorize_obj)


class TwitchUserBase(ABC):
    @abstractmethod
    def get_user_details(self):
        ...

    @abstractmethod
    def get_multiple_user_details(self):
        ...

    @abstractmethod
    def get_followers(self, user_id: str):
        ...

    @abstractmethod
    def get_followed(self, user_id: str):
        ...


class TwitchUserService(TwitchUserBase):
    base_url = 'api.twitch.tv'

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.conn = http.client.HTTPSConnection(TwitchUserService.base_url)
        self.headers = {'Authorization': f'Bearer {self.access_token}', 'Client-Id': os.environ.get('TWITCH_CLIENT_ID')}

    def get_user_details(self):
        endpoint = '/helix/users'
        self.conn.request('GET', endpoint, headers=self.headers)
        response = self.conn.getresponse()
        data = response.read()
        user_details = json.loads(data.decode('utf-8'))
        return user_details

    def get_multiple_user_details(self):
        ...

    def get_followers(self, user_id: str):
        endpoint = f'/helix/channels/followers?user_id={user_id}'
        self.conn.request('GET', endpoint, headers=self.headers)
        response = self.conn.getresponse()
        data = response.read()
        followers = json.loads(data.decode('utf-8'))
        return followers

    def get_followed(self, user_id: str):
        endpoint = f'/helix/channels/followed?user_id={user_id}'
        self.conn.request('GET', endpoint, headers=self.headers)
        response = self.conn.getresponse()
        data = response.read()
        followed = json.loads(data.decode('utf-8'))
        return followed


def extract_twitch_info(data: Dict[str, Any], key: str) -> Union[str, None]:
    user_info = None
    if "data" in data and len(data["data"]) > 0:
        user_data = data["data"][0]
        user_info = user_data.get(key)
        if user_info is None:
            print(f"Key '{key}' not found in user data.")
        return user_info
    return None


if __name__ == '__main__':
    ...
