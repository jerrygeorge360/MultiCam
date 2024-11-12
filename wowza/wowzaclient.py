import http.client
from abc import ABC, abstractmethod
import json
import os
from dotenv import load_dotenv
from typing import Optional
import logging
from time import sleep



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
key_path_hls ='live_stream.hls_playback_url'
key_path_created_at = 'live_stream.created_at'





def get_nested_value(data: json, key_path):
    keys = key_path.split('.')
    value = json.loads(data)
    for key in keys:
        print('hit', key)
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
        self.stream_id: Optional[str] = None
        self.stream_name: Optional[str] = None
        self.stream_state: bool = False
        self.state: str = ''
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.embed_code: Optional[str] = None
        self.hls:Optional[str] = None
        self.primary_server:Optional[str] = None
        self.created_at: str = ''

        self.cam_angle:Optional[str] = None
        self.cam_label:Optional[str] = None

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
        # data = mock_data()
        self.data.stream_id = get_nested_value(data, key_path_id)
        self.data.state = get_nested_value(data, key_path_state)
        self.data.stream_name = get_nested_value(data, key_path_stream_name)
        self.data.username = get_nested_value(data, key_path_username)
        self.data.password = get_nested_value(data, key_path_password)
        return self.data

    # This ensures the embed code attribute is set after the creation of the stream instead of showing processing.
    def initialize_live_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}'
        self.data.payload = ''
        self.conn.request("GET", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        # data = mock_data()
        self.data.embed_code = get_nested_value(data, key_path_embed_code)
        self.data.hls = get_nested_value(data,key_path_hls)
        self.data.primary_server = get_nested_value(data,key_path_primary_server)
        return self.data

    def start_listening_to_stream(self, stream_id):
        self.data.api = f'/api/v2.0/live_streams/{stream_id}/start'
        self.data.payload = ''
        self.conn.request("PUT", self.data.api, self.data.payload, self.data.header)
        data = self.url_construct()
        # data = mock_data1()
        self.data.stream_state = get_nested_value(data, key_path_state)
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
        # data = mock_data1()
        self.data.stream_state = get_nested_value(data, key_path_state)
        return self.data

    def url_construct(self):
        res = self.conn.getresponse()
        data = res.read()
        return data.decode('utf-8')


class MultiUserStreamMeta(type):
    # this ensures that each stream of a user has it own instance,which can be accessed if it already exists, hence maximizing resources
    _instances = {}

    def __call__(cls, *args, **kwargs):
        user_id = kwargs.get('user_id') or args[0]
        object_id = kwargs.get('object_id') or args[1]

        if user_id is None:
            raise ValueError("user_id must be provided")
        if object_id is None:
            raise ValueError("object_id must be provided")
        if user_id =='default' and object_id == 'default':
            return super().__call__(*args, **kwargs)
        key = (user_id, object_id)
        if key not in cls._instances:
            logger.info('key not found\nAdding Instance...')
            cls._instances[key] = super().__call__(*args, **kwargs)
        logger.info(f'\ninstances:{MultiUserStreamMeta._instances} ')
        return cls._instances[key]


class WowzaFacade(metaclass=MultiUserStreamMeta):
    def __init__(self, user_id: int or str = None, object_id: str = None, cam_angle=None, cam_label=None):
        self.user_id = user_id
        self.object_id = str(object_id)
        self.client = WowzaClient()
        self.client.data.cam_label = cam_label
        self.client.data.cam_angle = cam_angle
        self.initialized = False

    def setup(self):
        if self.initialized:
            return {
                'object_id': self.object_id,
                'stream_id':self.client.data.stream_id,
                'stream_name': self.client.data.stream_name,
                'stream_state': self.client.data.stream_state,
                'username': self.client.data.username,
                'password': self.client.data.password,
                'embed_code': self.client.data.embed_code,
                'hls':self.client.data.hls,
                'primary_server':self.client.data.primary_server,
                'cam_angle': self.client.data.cam_angle,
                'cam_label': self.client.data.cam_label
            }
        try:
            start_stream = self.client.create_live_stream()
            self.client.data.stream_id = start_stream.stream_id
            self.client.data.stream_name = start_stream.stream_name
            self.client.data.stream_state = start_stream.state
            self.client.data.username = start_stream.username
            self.client.data.password = start_stream.password
            self.client.data.embed_code = start_stream.embed_code
            self.client.data.hls = start_stream.hls
            self.client.data.primary_server = start_stream.primary_server
        except Exception as e:
            logger.error(f"Problem with creating live stream: {str(e)}")
            return 'failed'
        try:
            initialize_stream = self.client.initialize_live_stream(stream_id=self.client.data.stream_id)
            embed_code = initialize_stream.embed_code

            retries:int = 0
            while embed_code == 'in_progress':
                # takes a while to get initialized in the wowza server
                sleep(2)
                print('Waiting for stream to initialize...')
                initialize_stream = self.client.initialize_live_stream(stream_id=self.client.data.stream_id)

                # embed_code = get_nested_value(initialize_stream, key_path_embed_code)
                embed_code = initialize_stream.embed_code
                retries += 1
                if retries > 10:
                    logger.error("Max retries reached while waiting for stream initialization")
                    return 'failed'


            self.client.data.embed_code = embed_code
            self.initialized = True
            logger.info(f"Stream initialized with embed code: {self.client.data.embed_code}")
            return {
                'object_id': self.object_id,
                'stream_id':self.client.data.stream_id,
                'stream_name': self.client.data.stream_name,
                'stream_state': self.client.data.stream_state,
                'username': self.client.data.username,
                'password': self.client.data.password,
                'embed_code': self.client.data.embed_code,
                'hls':self.client.data.hls,
                'primary_server':self.client.data.primary_server,
                'cam_angle': self.client.data.cam_angle,
                'cam_label': self.client.data.cam_label
            }
        except Exception as e:
            logger.error(f"Error during stream initialization: {str(e)}")
            return 'failed'

    def listen_to_stream(self):
        try:
            listen = self.client.start_listening_to_stream(stream_id=self.client.data.stream_id)
            stream_state = listen.stream_state
            print(stream_state)
            if stream_state == 'starting':
                self.client.data.stream_state = True
                return {'state': self.client.data.stream_state}
            # raise a custom error
        except Exception:
            ...

    def stop_stream(self):
        try:
            stop = self.client.stop_listening_to_stream(stream_id=self.client.data.stream_id)
            stream_state = stop.stream_state
            if stream_state == 'stopped':
                self.client.data.stream_state = False
                return {'state': self.client.data.stream_state}
        except Exception:
            ...

    @classmethod
    def delete_instance(cls,user_id,object_id):
        key = (user_id,object_id)
        if key in MultiUserStreamMeta._instances:
            del MultiUserStreamMeta._instances[key]
        return {'status': 'deleted'}

    @classmethod
    def get_unique_user_ids(cls)-> set[str]:
        # Returns a set of unique user IDs
        return {uid for (uid, _) in MultiUserStreamMeta._instances.keys()}

    @classmethod
    def get_users_with_active_streams(cls) -> set:
        return {uid for (uid, _), instance in MultiUserStreamMeta._instances.items() if
                instance.client.data.stream_state == True}

    @classmethod
    def get_instances_by_stream_state(cls, state):
        return [instance for instance in MultiUserStreamMeta._instances.values() if instance.stream_state == state]

    @classmethod
    def get_user_instances(cls, user_id):
        # returns different facade instances
        # facade_instances_list[index].method/property

        return [instance for (uid, _), instance in MultiUserStreamMeta._instances.items() if uid == user_id]

    def to_dict(self):
        return {
            'object_id': self.object_id,
            'stream_id': self.client.data.stream_id,
            'stream_name': self.client.data.stream_name,
            'stream_state': self.client.data.stream_state,
            'username': self.client.data.username,
            'password': self.client.data.password,
            'embed_code': self.client.data.embed_code,
            'hls':self.client.data.hls,
            'primary_server':self.client.data.primary_server,
            'cam_angle': self.client.data.cam_angle,
            'cam_label': self.client.data.cam_label
        }