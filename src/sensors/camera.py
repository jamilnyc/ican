import picamera

class Camera:
    """Class for taking photos from the Raspberry Pi"""

    def __init__(self, imagePath):
        self.imagePath = imagePath

        # Initialize Pi Camera object
        self.camera = picamera.PiCamera()
        self.camera.rotation = 270
        self.camera.sharpness = 100
        self.camera.brightness = 50

    def getImagePage(self):
        return self.imagePath

    def setImagePath(self, newPath):
        """Set path (include file name) of where images will be saved."""
        self.imagePath = newPath

    def takePhoto(self):
        """Take a photo and save it to the file system."""
        self.camera.capture(self.imagePath)