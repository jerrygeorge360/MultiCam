from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Stream, User
from wowza.wowzaclient import WowzaFacade

viewer = Blueprint('viewer', __name__, template_folder='templates/viewer', static_folder='static')


@viewer.route('/view')
@login_required
def index():
    button_captions = ['live', 'following', 'registered']
    active_users = db.session.query(User).join(Stream).filter(Stream.active == True).all()
    print(active_users)
    return render_template('viewer.html', button_captions=button_captions, active_users=active_users)


@viewer.route('/watch', methods=['GET', 'POST'])
@login_required
def watch():
    user_id = int(request.args.get('userId'))
    obj = WowzaFacade(user_id=user_id)
    user_streams = obj.get_user_instances(user_id=user_id)
    user_streams_data = [instance.to_dict() for instance in user_streams]
    print(user_streams_data,'helelo')
    return render_template('watch.html',user_streams_data=user_streams_data)
