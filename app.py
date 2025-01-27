import os
from datetime import timedelta
from flask import Flask,jsonify,render_template
from flask_cors import CORS
from helpers import footer_data
from models import *
from flask_migrate import Migrate
from flask_login import LoginManager
from flasgger import Swagger
from main.main import main
from auth.auth import auth
from streamer.streamer import streamer
from viewer.viewer import viewer
from oauth.oauth import oauth
from wowza.wowza import wowza

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(streamer)
app.register_blueprint(viewer)
app.register_blueprint(oauth)
app.register_blueprint(wowza)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)
db.init_app(app)
migrate = Migrate(app, db, command='migrate')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_get'


@app.context_processor
def inject_globals():
    return {'footer_data': footer_data}


@login_manager.user_loader
def load_user(username):
    return db.session.execute(db.select(User).where(User.id == username)).scalar()

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'status': 'failed', 'error': 'You need to be logged in to access this resource'}), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

