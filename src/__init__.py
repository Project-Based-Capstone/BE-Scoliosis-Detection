import datetime
from PIL import Image
from flask import Flask, redirect, jsonify
import os

from src.routes.auth import auth
from src.routes.recorddetection import record
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.config.database import db
from flask_jwt_extended import JWTManager
from flask import current_app

PASSWORD = os.environ.get("DB_PASSWORD")
PUBLIC_IP_ADDRESS =os.environ.get("DB_IP_ADDRESS")
DBNAME =os.environ.get("DB_NAME")
PROJECT_ID =os.environ.get("PROJECT_ID")
INSTANCE_NAME =os.environ.get("INSTANCE_NAME")

if os.environ.get("FLASK_ENV") == "development":
    SQLALCHEMY_DATABASE_URI= os.environ.get("SQLALCHEMY_DB_URI")
else:
    SQLALCHEMY_DATABASE_URI= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APP_CREDENTIALS")
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI= SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER"),
            JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(minutes=120)
        )
        
    else:
        app.config.from_mapping(test_config)

    
    db.app = app
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        current_app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI= SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER"),
            JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(minutes=120)
        )
        
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(record)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR
    
    return app
