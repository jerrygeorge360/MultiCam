from flask import Blueprint, render_template, request
from flask_login import login_required
from wowza.wowzaclient import WowzaFacade
from models import User,db

viewer = Blueprint('viewer', __name__, template_folder='templates/viewer', static_folder='static')


@viewer.route('/api/v1/view')
@login_required
def index():
    """
        Get a list of active streamers (users) who are currently broadcasting.
        ---
        description: This endpoint retrieves a list of users with active streams and returns them with associated button captions. The user must be logged in to access this endpoint.
        responses:
          200:
            description: A list of active streamers, rendered on the viewer page with associated button captions.
            content:
              text/html:
                schema:
                  type: string
                  example: "HTML page containing button captions and active users"
          401:
            description: Unauthorized. The user is not logged in.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: "Unauthorized"
        security:
          - oauth2: []  # Assumes OAuth2 security for this route
        """

    button_captions = ['live', 'following', 'registered']
    wowza_service:WowzaFacade = WowzaFacade('default','default')
    active_users:set = wowza_service.get_users_with_active_streams()
    active_users_list:list = list(active_users)
    streamer_obj_list:list[User] = db.session.query(User).filter(User.id.in_(active_users_list)).all()
    print(active_users_list)
    return render_template('viewer.html', button_captions=button_captions, active_users=streamer_obj_list)


@viewer.route('/api/v1/watch', methods=['GET', 'POST'])
@login_required
def watch():
    """
       Watch a specific stream based on the given user ID.
       ---
       description: This endpoint allows users to watch a specific stream. The user ID is passed as a query parameter (`userId`). The endpoint fetches the stream data and renders it on the 'watch' page.
       parameters:
         - name: userId
           in: query
           description: The ID of the user whose stream the viewer wants to watch.
           required: true
           schema:
             type: integer
             example: 123
       responses:
         200:
           description: Successfully retrieved stream data for the user.
           content:
             text/html:
               schema:
                 type: string
                 example: "HTML page showing stream data"
         401:
           description: Unauthorized. The user must be logged in to view the stream.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   error:
                     type: string
                     example: "Unauthorized"
         404:
           description: Not Found. The requested stream data could not be found.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   error:
                     type: string
                     example: "Stream not found"
       security:
         - oauth2: []  # Assumes OAuth2 security for this route
       """

    streamer_id = int(request.args.get('userId'))
    wowza_service = WowzaFacade('default','default')
    instances:list[WowzaFacade] = wowza_service.get_user_instances(user_id=streamer_id)
    serialized_instances:list[[dict]] = [instance.to_dict() for instance in instances]
    return render_template('watch.html',user_streams_data = serialized_instances)
