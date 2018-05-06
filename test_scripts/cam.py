import picamera
import time

camera = picamera.PiCamera()
camera.rotation = 270
camera.sharpness = 100
camera.brightness = 50
path = '/tmp/camera/'

for i in range(0, 101, 20):
    camera.brightness = i
    fileName = 'image_brightness_' + str(i) + '.jpg'
    print "Taking picture " + fileName
    camera.capture(path + fileName)
    time.sleep(0.2)

