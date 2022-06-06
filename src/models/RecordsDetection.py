
import numpy as np
from src.config.database import db 
from datetime import datetime
from googleapiclient import discovery
import os
from google.api_core.client_options import ClientOptions


IMAGE_WIDTH=128
IMAGE_HEIGHT=128
IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)

class RecordsDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.Text, nullable=False)
    dateOfBirth = db.Column(db.Integer, nullable=False)
    detection = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
def predict_json(model, instances, version=None):
    endpoint = 'https://asia-southeast1-ml.googleapis.com'
    client_options = ClientOptions(api_endpoint=endpoint)
    service = discovery.build('ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(os.environ.get("PROJECT_ID"), model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def predict_image(image):
    category={
        1: {
            'category': 'Normal / Tidak Berisiko Scoliosis',
            'description': 'Tetap Jaga kesehatan anda'
        },
        0: {
            'category': 'Berisiko Scoliosis',
            'description': 'Segera hubungi dokter tulang belakang terdekat!!'
        }
    }
    new_image=image.resize(IMAGE_SIZE)
    new_image=np.expand_dims(new_image,axis=0)
    new_image=np.array(new_image)/255
    new_image=new_image.tolist()
    result = predict_json(model='scoliosis', instances=new_image)
    
    
    
    return category[result[0][0]]