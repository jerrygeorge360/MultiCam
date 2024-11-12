from flask import Blueprint, render_template, jsonify,request
from flask_login import login_required
from streamer.utils import camera_angles
from wowza.wowzaclient import WowzaFacade

streamer = Blueprint("streamer", __name__, template_folder="templates/streamer", static_folder="static")


@streamer.route('/api/v1/streamer')
@login_required
def home():

    """
        Get the home page for the streamer with available camera angles.
        ---
        description: This endpoint renders the home page where the streamer can see available camera angles for their stream.
        security:
          - oauth2: []
        responses:
          200:
            description: The home page with available camera angles.
            content:
              text/html:
                schema:
                  type: string
                  example: '<html>...</html>'  # Simplified example of the response type
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
        """

    return render_template('index.html',  camera_angles=camera_angles )


@streamer.get('/api/v1/get_streamers')
@login_required
def get_streamers():
    """
       Get the list of unique streamers.
       ---
       description: This endpoint returns a list of unique user IDs of active streamers. The user must be logged in to access this endpoint.
       security:
         - oauth2: []  # Assumes OAuth2 security for this route
       responses:
         200:
           description: A list of unique streamers who are currently active.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   data:
                     type: array
                     items:
                       type: string
                       description: A unique user ID for a streamer
                     example: ['user1', 'user2', 'user3']  # Example of the returned data
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
       """

    wowza_service:WowzaFacade = WowzaFacade('default','default')
    data:set = wowza_service.get_unique_user_ids()
    data:list = list(data)
    return jsonify({'data':data}),200


@streamer.get('/api/v1/get_user_streams')
@login_required
def get_user_streams():

    """
    Get the list of streams for a specific user (streamer).
    ---
    description: This endpoint returns a list of streams for a given streamer identified by their user ID. The user must be logged in to access this endpoint.
    parameters:
      - in: query
        name: streamer_id
        required: true
        description: The unique ID of the streamer for whom streams are being requested.
        schema:
          type: string
    security:
      - oauth2: []  # Assumes OAuth2 security for this route
    responses:
      200:
        description: A list of streams for the specified streamer, serialized into a dictionary.
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    type: object
                    description: A stream object, serialized as a dictionary.
                  example:
                    - { "stream_name": "Stream 1", "stream_state": "active", "cam_angle": "front" }
                    - { "stream_name": "Stream 2", "stream_state": "inactive", "cam_angle": "side" }
      400:
        description: Bad request. Missing or invalid streamer ID.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing or invalid streamer_id"
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
    """

    data = request.get_json()
    streamer_id:str = data.get('streamer_id')
    wowza_service:WowzaFacade = WowzaFacade('default','default')
    instances:list[WowzaFacade] = wowza_service.get_user_instances(user_id=streamer_id)
    serialized_instances:list[[dict]] = [instance.to_dict() for instance in instances]
    return jsonify({'data':serialized_instances}),200