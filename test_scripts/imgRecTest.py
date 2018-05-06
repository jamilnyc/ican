import sys

sys.path.append('../src/api')
from s3 import S3
import image_recognition
import prediction

path = 'https://kolonial.no/media/uploads/public/0/218/12218-8919f-product_detail.jpg'


imgRec = image_recognition.ImageRecognition()
labels = imgRec.getImageIdentifiers(path)
print labels
text = imgRec.getTextIdentifiers(path)
print text

pred = prediction.Prediction()
ret = pred.getTrashPrediction(labels)
print ret