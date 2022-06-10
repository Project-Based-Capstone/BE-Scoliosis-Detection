
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
import validators
from src.config.database import db
from src.models.User import User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    email = request.form.get("email", '')
    password = request.form.get("password", '')
    
    if len(password) < 6:
        return jsonify({
            'error':  True,
            'message': "Password is too short"
        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({
            'error':  True,
            'message': "Email is not valid"
        }), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': True,
            'message': "Email is taken"
        }), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'error': False,
        'message': "User succesfully created",
        'user': {
            "email": email
        }

    }), HTTP_201_CREATED

@auth.post('/login')
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'error': False,
                'message': "success",
                'user': {
                    'user_id': user.id,
                    'refresh_token': refresh,
                    'access_token': access,
                    'email': user.email
                }

            }), HTTP_200_OK
            
    return jsonify({
        'error': True,
        'message': 'Email or Password can not be found',
        'user': None
    }), HTTP_401_UNAUTHORIZED

@auth.get('/me')
@jwt_required()
def get_user_data():
    user_id = get_jwt_identity()
    
    user = User.query.filter_by(id=user_id).first()
    
    return jsonify({
        'email': user.email
    }), HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    
    return jsonify({
        'access_token': access
    }), HTTP_200_OK