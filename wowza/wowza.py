from flask import Blueprint, redirect, url_for, request, jsonify
from wowza.wowzaclient import WowzaFacade, logger
from models import Stream, db
from flask_login import current_user
from uuid import uuid4, UUID

wowza = Blueprint("wowza", __name__)


def update_stream(stream_id, new_values):
    stream = Stream.query.get(stream_id)
    if stream:
        for key, value in new_values.items():
            setattr(stream, key, value)

        try:
            db.session.commit()
            return stream
        except Exception as e:
            db.session.rollback()
            print(f"Error updating stream: {e}")
            return None
    else:
        print("Stream not found")
        return None


@wowza.post('/initialize_stream')
def initialize_stream():
    if current_user:
        data = request.get_json()
        user_id = current_user.id
        object_id = str(uuid4())
        cam_angle = data.get('camAngle')
        cam_label = data.get('camLabel')
        wowza_service = WowzaFacade(user_id=user_id, object_id=object_id, cam_angle=cam_angle, cam_label=cam_label)
        setup_info = wowza_service.setup()
    #     new_stream = Stream(object_id=object_id, embed_code=embed_code, stream_name=stream_name, cam_angle=cam_angle,
    #                         cam_label=cam_label,
    #                         user_id=current_user.id, password=setup_info.get('password'),
    #                         user_name=setup_info.get('username'), stream_id=stream_id)
    #     current_user.streams.append(new_stream)
    #     try:
    #         db.session.add(current_user)
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         print(e)
    #     return jsonify({**setup_info, 'object_id': str(UUID(object_id))}), 201
    # return jsonify({'error': 'not authorized'}), 401



@wowza.put('/listen_to_stream')
def listen_to_stream():
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    listen_data = wowza_service.listen_to_stream()
    return jsonify(listen_data), 200


@wowza.post('/stop_stream')
def stop_stream():
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    stop_data = wowza_service.stop_stream()
    delete_instance_data = wowza_service.delete_instance(user_id, object_id)
    logger.info(delete_instance_data)
    return jsonify(stop_data), 200


@wowza.delete('/delete_instance')
def delete_instance():
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    delete_instance_data = wowza_service.delete_instance(user_id, object_id)
    return jsonify(delete_instance_data), 200


@wowza.get('/get_specific_instances')
def get_instances():
    data = request.get_json()
    user_id = data['user_id']
    user_instances = WowzaFacade.get_user_instances(user_id)

    if len(user_instances)>0:
        return jsonify(user_instances), 200
    return jsonify({'error': 'No instances found for this user'}), 404


# @wowza.get('/get_instance')
# def get_instance():
#     data = request.get_json()
#     user_id = 1178104625
#     object_id = data.get('objectId')
#
#     if not object_id:
#         return jsonify({'error': 'objectId is required'}), 400
#
#     # Get the specific instance for the user_id and object_id
#     user_instance = [
#         instance.to_dict()
#         for (uid, oid), instance in WowzaFacade._instances.items()
#         if uid == user_id and oid == object_id
#     ]
#
#     if user_instance:
#         return jsonify(user_instance), 200
#     return jsonify({'error': 'Instance not found'}), 404
