from datetime import datetime
import json
from flask import Blueprint, jsonify, request
import numpy as np
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.config.database import db
import os
from src.models.RecordsDetection import RecordsDetection, predict_image
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app
from google.cloud import storage

from src.services.FileService import FileService

record = Blueprint("record", __name__, url_prefix="/api/v1/record")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return filename in ALLOWED_EXTENSIONS


@record.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_record():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        try:
            name = request.form.get("name", '')
            dateOfBirth = request.form.get("dateOfBirth", '')
            file = request.form.get('file')
            fileSvc = FileService(file)
            image = fileSvc.openImage()
            result = predict_image(image)
            if file and allowed_file(image.format.lower()):
                dt = datetime.today()
                filename = str(round(dt.timestamp())) + '.' + image.format.lower()
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                if(os.environ.get("FLASK_ENV") == 'production'):
                    try:
                        bucket_name = "scoliosis-detection"
                        source_file_name = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        destination_blob_name = f"tmp/{(filename)}"

                        storage_client = storage.Client()
                        bucket = storage_client.bucket(bucket_name)
                        blob = bucket.blob(destination_blob_name)

                        blob.upload_from_filename(source_file_name)
                    except:
                        return jsonify({
                            'error': True,
                            'message': 'Internal Server Error',
                        }), HTTP_500_INTERNAL_SERVER_ERROR    
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            record = RecordsDetection(name=name, image=filename, dateOfBirth=dateOfBirth,
                                      detection=result['category'], description=result['description'],
                                      user_id=current_user)
            db.session.add(record)
            db.session.commit()

            return jsonify({
                'error': False,
                'message': 'Successfully Created',
            }), HTTP_201_CREATED
        except:
            return jsonify({
                'error': True,
                'message': 'Internal Server Error',
            }), HTTP_500_INTERNAL_SERVER_ERROR
    else:
        # page = request.args.get('page', 1, type=int)
        # per_page = request.args.get('per_page', 5, type=int)

        # records = RecordsDetection.query.filter_by(
        #     user_id=current_user).paginate(page=page, per_page=per_page)
        records = RecordsDetection.query.filter_by(
            user_id=current_user)
        data = []

        for item in records:
            data.append({
                'id': item.id,
                'name': item.name,
                'image': 'https://storage.googleapis.com/scoliosis-detection/tmp/' + item.image,
                'dateOfBirth': item.dateOfBirth,
                'detection': item.detection,
                'description': item.description,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
            })

        # meta = {
        #     "page": records.page,
        #     "pages": records.pages,
        #     "total_count": records.total,
        #     "prev_page": records.prev_num,
        #     "next_page": records.next_num,
        #     "has_next": records.has_next,
        #     "has_prev": records.has_prev,
        # }

        # return jsonify({'data': data, "meta": meta}), HTTP_200_OK
        return jsonify({'data': data}), HTTP_200_OK


@record.get("/<int:id>")
@jwt_required()
def get_record(id):
    current_user = get_jwt_identity()
    record = RecordsDetection.query.filter_by(
        user_id=current_user, id=id).first()

    if not record:
        return jsonify({'message': "Item not found"})

    return jsonify({
        'data': {
            'id': record.id,
            'name': record.name,
            'image': record.image,
            'dateOfBirth': record.dateOfBirth,
            'detection': record.detection,
            'description': record.description,
            'created_at': record.created_at,
            'updated_at': record.updated_at,
        }
    }), HTTP_200_OK

@record.delete("/<int:id>")
@jwt_required()
def delete_record(id):
    current_user = get_jwt_identity()

    record = RecordsDetection.query.filter_by(user_id=current_user, id=id).first()

    if not record:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(record)
    db.session.commit()

    return jsonify({
        'message' : 'successfully deleted'
        }), HTTP_200_OK
