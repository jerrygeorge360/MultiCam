from flask import Blueprint,request, jsonify
from wowza.wowzaclient import WowzaFacade, logger
from flask_login import current_user, login_required
from uuid import uuid4

wowza = Blueprint("wowza", __name__)


@wowza.post('/api/v1/initialize_stream')
@login_required
def initialize_stream():
    """
       Initialize a stream with specific camera settings.
       ---
       description: This endpoint initializes a stream for the user, requiring camera angle (`camAngle`) and label (`camLabel`) as parameters. It generates a unique object ID and sets up the stream.
       requestBody:
         required: true
         content:
           application/json:
             schema:
               type: object
               properties:
                 camAngle:
                   type: string
                   description: The angle of the camera for the stream.
                   example: "45"
                 camLabel:
                   type: string
                   description: The label or name for the camera.
                   example: "Front Camera"
       responses:
         200:
           description: Stream successfully initialized.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   data:
                     type: object
                     description: The setup information of the stream.
                     example: {"streamId": "abc123", "status": "success"}
         400:
           description: Missing required parameters (`camAngle` or `camLabel`).
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   status:
                     type: string
                     example: "failed"
                   error:
                     type: string
                     example: "Missing required parameters: camAngle, camLabel"
         500:
           description: Server error while initializing the stream.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   status:
                     type: string
                     example: "failed"
                   error:
                     type: string
                     example: "Error initializing stream"
       security:
         - oauth2: []  # Assumes OAuth2 is being used for authentication
       """
    data = request.get_json()
    user_id = current_user.id
    object_id = str(uuid4())

    cam_angle = data.get('camAngle')
    cam_label = data.get('camLabel')

    if not cam_angle or not cam_label:
        return jsonify({'status': 'failed', 'error': 'Missing required parameters: camAngle, camLabel'}), 400

    wowza_service = WowzaFacade(user_id=user_id, object_id=object_id, cam_angle=cam_angle, cam_label=cam_label)
    try:
        setup_info = wowza_service.setup()
        return jsonify({'data':setup_info}),200
    except Exception as e:
        logger.error(f"Error initializing stream for user {user_id}: {str(e)}")
        return jsonify({'status':'failed','error':str(e)}),500



@wowza.put('/api/v1/listen_to_stream')
def listen_to_stream():
    """
        Listen to a stream based on the user and object ID.
        ---
        description: This endpoint allows the user to start listening to a stream by providing the object ID. The user must be authenticated to access this endpoint.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  objectId:
                    type: string
                    description: The ID of the stream object to listen to.
                    example: "abc123"
        responses:
          200:
            description: Stream listening successfully started.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    data:
                      type: object
                      description: The data related to the stream listening process.
                      example: {"status": "listening", "message": "Successfully started listening to stream"}
          400:
            description: Missing or invalid parameters in the request body.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "failed"
                    error:
                      type: string
                      example: "Missing objectId"
          500:
            description: Server error while trying to start stream listening.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "failed"
                    error:
                      type: string
                      example: "Error starting to listen to stream"
        security:
          - oauth2: []  # Assumes OAuth2 is being used for authentication
        """
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    listen_data = wowza_service.listen_to_stream()
    return jsonify({'data':listen_data}), 200


@wowza.post('/api/v1/stop_stream')
def stop_stream():
    """
       Stop a stream and delete the associated instance.
       ---
       description: This endpoint allows the user to stop a stream and delete its associated instance. The user must be authenticated to access this endpoint.
       requestBody:
         required: true
         content:
           application/json:
             schema:
               type: object
               properties:
                 objectId:
                   type: string
                   description: The ID of the stream object to stop.
                   example: "abc123"
       responses:
         200:
           description: Stream successfully stopped and instance deleted.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   data:
                     type: object
                     description: The data related to stopping the stream.
                     example: {"status": "stopped", "message": "Successfully stopped the stream and deleted the instance."}
         400:
           description: Missing or invalid parameters in the request body.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   status:
                     type: string
                     example: "failed"
                   error:
                     type: string
                     example: "Missing objectId"
         500:
           description: Server error while trying to stop the stream or delete the instance.
           content:
             application/json:
               schema:
                 type: object
                 properties:
                   status:
                     type: string
                     example: "failed"
                   error:
                     type: string
                     example: "Error stopping the stream or deleting the instance"
       security:
         - oauth2: []  # Assumes OAuth2 is being used for authentication
       """
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    stop_data = wowza_service.stop_stream()
    delete_instance_data = wowza_service.delete_instance(user_id, object_id)
    logger.info(delete_instance_data)
    return jsonify({'data':stop_data}), 200


@wowza.delete('/api/v1/delete_instance')
def delete_instance():
    """
        Delete a stream instance.
        ---
        description: This endpoint allows the user to delete a specific stream instance by providing the objectId of the stream. The user must be authenticated to access this endpoint.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  objectId:
                    type: string
                    description: The ID of the stream object to delete.
                    example: "abc123"
        responses:
          200:
            description: Stream instance successfully deleted.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    data:
                      type: object
                      description: The data related to the deletion of the instance.
                      example: {"status": "deleted", "message": "Stream instance deleted successfully."}
          400:
            description: Missing or invalid parameters in the request body.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "failed"
                    error:
                      type: string
                      example: "Missing objectId"
          500:
            description: Server error while trying to delete the stream instance.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "failed"
                    error:
                      type: string
                      example: "Error deleting the instance"
        security:
          - oauth2: []  # Assumes OAuth2 is being used for authentication
        """
    data = request.get_json()
    user_id = current_user.id
    object_id = data.get('objectId')
    wowza_service = WowzaFacade(user_id, object_id)
    delete_instance_data = wowza_service.delete_instance(user_id, object_id)
    return jsonify({'data':delete_instance_data}), 200