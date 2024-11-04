import http.client
from abc import ABC, abstractmethod
import json
import os
from dotenv import load_dotenv
from typing import Optional
from uuid import uuid4

load_dotenv()
wowza_access_token = os.environ.get('WOWZA_STREAMING_CLOUD_TOKEN')

key_path_state = 'live_stream.state'
key_path_id = 'live_stream.id'
# source connection
key_path_primary_server = 'live_stream.source_connection_information.primary_server'
key_path_stream_name = 'live_stream.source_connection_information.stream_name'
key_path_username = 'live_stream.source_connection_information.username'
key_path_password = 'live_stream.source_connection_information.password'
# end connection
key_path_embed_code = 'live_stream.embed_code'
key_path_created_at = 'live_stream.created_at'


def get_nested_value(data: json, key_path):
    keys = key_path.split('.')
    value = json.loads(data)
    for key in keys:
        # print('hit', key)
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value


class WowzaAPIException(Exception):
    ...


class WowzaClientBase(ABC):
    @abstractmethod
    def create_live_stream(self):
        ...

    @abstractmethod
    def initialize_live_stream(self, stream_id):
        ...

    @abstractmethod
    def start_listening_to_stream(self, stream_id):
        ...

    @abstractmethod
    def get_state_of_stream(self, stream_id):
        ...

    @abstractmethod
    def stop_listening_to_stream(self, stream_id):
        ...


class WowzaClientConfig:
    def __init__(self):
        self._payload: str = ''
        self._headers: dict = {}
        self._base_api: str = 'api.video.wowza.com'
        self._api: str = ''
        self.stream_id: str = ''
        self.state: str = ''
        self.stream_name: str = ''
        self.username: str = ''
        self.password: str = ''
        self.embed_code: Optional[str] = None
        self.created_at: str = ''

    @property
    def payload(self) -> json:
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def header(self) -> dict:
        return self._headers

    @header.setter
    def header(self, value):
        self._headers = value

    @property
    def base_api(self) -> str:
        return self._base_api

    @base_api.setter
    def base_api(self, value):
        self._base_api = value

    @property
    def api(self) -> str:
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    def construct(self, name_of_stream='My streaming'):
        self.base_api = 'api.video.wowza.com'
        payload = {
            "live_stream": {"aspect_ratio_height": 720, "aspect_ratio_width": 1280, "billing_mode": "pay_as_you_go",
                            "broadcast_location": "us_west_oregon", "encoder": "other_rtmp", "name": name_of_stream,
                            "transcoder_type": "transcoded"}}
        self.payload = json.dumps(payload)
        self.header = {"Authorization": f"Bearer {wowza_access_token}", "Content-Type": "application/json"}


class WowzaClient(WowzaClientBase):
    def __init__(self, data: WowzaClientConfig = None):
        if data is None:
            data = WowzaClientConfig()
        self.data = data
        self.data.construct()
        self.conn = http.client.HTTPSConnection(self.data.base_api)

    def create_live_stream(self):
        self.data.api = '/api/v2.0/live_streams'
        self.conn.request("POST", self.data.api, body=self.data.payload, headers=self.data.header)
        data = self.url_construct()
        self.data.stream_id = get_nested_value(data, key_path_id)
        self.data.state = get_nested_value(data, key_path_state)
        self.data.stream_name = get_nested_value(data, key_path_stream_name)
        self.data.username = get_nested_value(data, key_path_username)
        self.data.password = get_nested_value(data, key_path_password)
        return self.data

    def initialize_live_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}'
        self.data.payload = ''
        self.conn.request("GET", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        self.data.embed_code = get_nested_value(data, key_path_embed_code)
        return self.data

    def start_listening_to_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}/start'
        self.data.payload = ''
        self.conn.request("PUT", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        self.data.state = get_nested_value(data, key_path_state)
        return self.data

    def get_state_of_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}/state'
        self.data.payload = ''
        self.conn.request("GET", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        self.data.state = get_nested_value(data, key_path_state)
        return self.data

    def stop_listening_to_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}/stop'
        self.data.payload = ''
        self.conn.request("PUT", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        self.data.state = get_nested_value(data, key_path_state)
        return self.data

    def url_construct(self):
        res = self.conn.getresponse()
        data = res.read()
        return data.decode('utf-8')


class MultiUserStreamMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        user_id = kwargs.get('user_id')
        object_id = kwargs.get('object_id')

        # if user_id is None:
        #     raise ValueError("user_id must be provided")

        key = (user_id, object_id)

        if key not in cls._instances:
            print('not here')
            cls._instances[key] = super().__call__(*args, **kwargs)
        print('here')
        return cls._instances[key]


class WowzaFacade(metaclass=MultiUserStreamMeta):
    def __init__(self, user_id: int = None, object_id: uuid4 = None, cam_angle=None, cam_label=None):
        self.user_id = user_id
        self.object_id = str(object_id)
        self.client = WowzaClient()
        self.embed_code: Optional[str] = None
        self.stream_id: Optional[str] = None
        self.stream_name: Optional[str] = None
        self.initialized = False
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.stream_state: bool = False
        self.cam_label = cam_label
        self.cam_angle = cam_angle

    def setup(self):
        if self.initialized:
            return {
                'id': self.stream_id,
                'stream_name': self.stream_name,
                'object_id': self.object_id,
                'stream_state': self.stream_state,
                'username': self.username,
                'password': self.password,
                'embed_code': self.embed_code,
                'initialized': True,
                'cam_angle': self.cam_angle,
                'cam_label': self.cam_label
            }
        start_stream = self.client.create_live_stream()
        self.stream_id = start_stream.stream_id
        self.stream_name = start_stream.stream_name
        self.stream_state = start_stream.state
        self.username = start_stream.username
        self.password = start_stream.password
        initialize_stream = self.client.initialize_live_stream(stream_id=self.stream_id)
        self.embed_code = initialize_stream.embed_code
        self.initialized = True
        return {'id': self.stream_id, 'stream_name': self.stream_name, 'stream_state': self.stream_state,
                'object_id': self.object_id, 'username': self.username,
                'password': self.password, 'cam_angle': self.cam_angle,
                'cam_label': self.cam_label, 'initialized': False}

    def get_embed_code(self) -> Optional[str]:
        return self.embed_code

    def get_stream_name(self) -> Optional[str]:
        return self.stream_name

    def get_strean_id(self):
        return self.stream_id

    def listen_to_stream(self):
        resp = self.client.start_listening_to_stream(stream_id=self.stream_id)
        stream_state = resp.state
        if resp:
            self.stream_state = True
        return {'state': resp.state}

    def stop_stream(self):

        resp = self.client.stop_listening_to_stream(stream_id=self.stream_id)
        if resp:
            self.stream_state = False
        return {'state': resp.state}

    def delete_instance(self):
        self.stop_stream()
        key = (self.user_id, self.object_id)
        if key in MultiUserStreamMeta._instances:
            del MultiUserStreamMeta._instances[key]
        return {'status': 'deleted', 'stream_id': self.stream_id}

    @classmethod
    def get_user_instances(cls, user_id):

        return [instance for (uid, _), instance in MultiUserStreamMeta._instances.items() if uid == user_id]

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'object_id': str(self.object_id),  # Convert UUID to a string
            'embed_code': self.embed_code,
            'stream_id': self.stream_id,
            'stream_name': self.stream_name,
            'stream_state': self.stream_state,
            'username': self.username,
            'password': self.password,
            'initialized': self.initialized,
            'cam_label': self.cam_label,
            'cam_angle': self.cam_angle
        }
