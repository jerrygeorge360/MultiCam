from flask import Blueprint, render_template, jsonify
import os
from flask_login import login_required, current_user
from streamer.utils import camera_angles
from models import Stream

streamer = Blueprint("streamer", __name__, template_folder="templates/streamer", static_folder="static")


@streamer.route('/streamer')
@login_required
def home():
    return render_template('index.html', user=current_user, camera_angles=camera_angles, )


@streamer.get('/check_streams')
@login_required
def check_user_streams():
    user_streams = Stream.query.filter_by(user_id=current_user.id).all()
    streams_data = [
        {
            'object_id': stream.object_id,
            'cam_angle': stream.cam_angle,
            'cam_label': stream.cam_label,
            'stream_name': stream.stream_name,
            'user_name': stream.user_name,
            'password': stream.password,
            'active': stream.active
        }
        for stream in user_streams
    ]

    return jsonify(
        {'has_streams': len(user_streams) > 0, 'streams': streams_data}), 200
