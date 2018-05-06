import os
import sys
from collections import deque
from time import sleep
from time import time

# Not included in path during boot, manually including it
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')

currentPath = os.path.dirname(__file__)

sys.path.append(os.path.join(currentPath, 'sensors'))
import lid
import camera

sys.path.append(os.path.join(currentPath, 'output'))
import light
import trapdoor

sys.path.append(os.path.join(currentPath, 'api'))
import s3
import database
import image_recognition
import prediction
import local_weather
import notification


class ICan:
    """
    Main class of the iCan application that packages the high level logic of the device.

    Public Methods:
        checkOrientation()
    """

    # SENSORS
    lidSensor = lid.Lid()
    cameraSensor = camera.Camera('/tmp/trash.jpg')

    # ACTUATORS/OUTPUT
    lightOutput = light.Light(21)
    trapdoorOutput = trapdoor.Trapdoor()

    # CLOUD SERVICES AND APIs
    storageService = s3.S3()
    databaseService = database.ICanItems()
    weatherService = local_weather.LocalWeather()
    recognitionService = image_recognition.ImageRecognition()
    predictionService = prediction.Prediction()
    notificationService = notification.Notification()

    # How long to wait to be in "steady" state (seconds)
    WAIT_TIME = 3
    
    # How often readings are taken from the accelerometer (seconds)
    READING_INTERVAL = 0.2

    recentOpenStates = None

    # Take a photo only after the can was just opened and closed (and in steady state)
    photoRecentlyTaken = True

    def __init__(self):
        # Store recent history of states in tuples (horizontal, vertical)
        initialState = (False, False)
        maxLength = int(self.WAIT_TIME / self.READING_INTERVAL)
        self.recentOpenStates = deque(maxLength * [initialState], maxLength)

    def checkOrientation(self):
        """
        Checks the current orientation of the lid, take a photo and process it.
        :return:
        """
        horizontal = self.lidSensor.isHorizontal()
        vertical = self.lidSensor.isVertical()
        print 'H: ', horizontal
        print 'V: ', vertical

        self.recentOpenStates.append((horizontal, vertical))

        if self.isReadyToTakePhoto() and not self.photoRecentlyTaken:
            print 'Taking photo now . . . '
            fileName = self.getFileName()
            self.cameraSensor.setImagePath(fileName)
            self.cameraSensor.takePhoto()
            link = self.uploadPhoto(fileName)

            identifiers = self.recognitionService.getImageIdentifiers(fileName)
            targetPrediction = self.predictionService.getTrashPrediction(identifiers)
            print identifiers
            print targetPrediction

            # Fallback in case nothing is recognized in the image by recognition service
            if len(identifiers) == 0:
                identifiers = ['trash']
                targetPrediction = 'trash'

            self.saveToDatabase(identifiers, targetPrediction, link)
            self.respondToPrediction(identifiers, targetPrediction)
            self.photoRecentlyTaken = True

        if vertical and not horizontal:
            # Lid is open
            self.lightOutput.turnOn()
            self.photoRecentlyTaken = False
        else:
            self.lightOutput.turnOff()

    def saveToDatabase(self, identifiers, targetPrediction, link):
        """
        Save the record of identification to the database.
        :param identifiers: List of identifier strings from the image recognition service
        :param targetPrediction: String prediction from the prediction service
        :param link: Public URL to the image
        :return: Response to save request from the database
        """
        return self.databaseService.addRecord({
            'item_name': ", ".join(identifiers),
            'recyclable': (targetPrediction == 'recyclable'),
            'compostable': (targetPrediction == 'compostable'),
            'timestamp': int(time()),
            'temperature': self.weatherService.getCurrentTemperature(),
            'image': link,
            'user_feedback': False,
        })

    def getFileName(self):
        """
        Return the pseudo unique filename of the next photo to be taken.
        :return: Absolute path to the file as a string
        """
        timestamp = time()
        name = 'trash_' + str(timestamp) + '.jpg'
        path = '/tmp/'
        return path + name

    def isReadyToTakePhoto(self):
        """
        Return if the iCan is ready to take a photo based on current state and previous states.

        If the lid as been closed for the entire duration of the waiting period, then it is
        time to take a photo.

        :return: Boolean on whether the iCan is ready to take a photo
        """
        # Check if the queue of states shows it has been closed
        # for the entire waiting period
        closedState = (True, False)
        return self.recentOpenStates.count(closedState) == self.recentOpenStates.maxlen

    def uploadPhoto(self, fileName):
        """
        Upload given file to cloud storage, write the link to a file and return it
        :param fileName: Absolute path to file
        :return: URL to the file on cloud storage
        """

        # Write the public link to a local file
        link = self.storageService.uploadData(fileName)
        with open('/tmp/photos.txt', 'a') as photosFile:
            photosFile.write(link + "\n")
        print 'URL: ' + link
        return link

    def respondToPrediction(self, identifiers, targetPrediction):
        """
        React to the prediction by either opening the trapdoor or sending a notification.
        :param identifiers: List of string identifiers from Image Recognition Service
        :param targetPrediction: Prediction of 'trash', 'compostable', 'recyclable', etc. from the ML model
        :type targetPrediction: str
        """
        if targetPrediction == 'trash':
            print 'Down the hatch!'
            self.trapdoorOutput.open()
            print 'Waiting . . . '
            sleep(2)
            self.trapdoorOutput.close()
        else:
            print 'Sending Notification'
            identifiersList = ', '.join(identifiers[:3])
            message = 'iCan has detected an item that is: ' + identifiersList
            message = message + "\nCategory " + targetPrediction.upper()
            self.notificationService.sendNotification(message)

    def cleanUp(self):
        """
        Clean up any used I/O pins and close any connections if needed.
        :return: None
        """
        self.trapdoorOutput.cleanUp()
        self.lightOutput.cleanUp()


iCan = ICan()

try:
    while True:
        iCan.checkOrientation()
        sleep(iCan.READING_INTERVAL)
except KeyboardInterrupt:
    print "Cleaning up"
    iCan.cleanUp()
    print "Exiting iCan . . . "
    exit()
