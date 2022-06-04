import base64
from io import BytesIO
from PIL import Image

class FileService:
  def __init__(self, img):
        self.img = img
        
  def decodeAndCoverted(self):
    b64 = base64.b64decode(self.img)
    b64 = BytesIO(b64)  
    return b64
 
  def openImage(self):
    img = Image.open(self.decodeAndCoverted())
    return img 
  