from gpiozero import LED
from time import sleep
from  collections import deque
import picamera

# Import the ADXL345 module.
import Adafruit_ADXL345

# Create an ADXL345 instance.
accel = Adafruit_ADXL345.ADXL345()


def signalOpen():
    led.on()

def signalClosed():
    led.off()

def getAccelerometerValues():
    x, y, z = accel.read()
    print ('x:{0}\ty:{1}\tz:{2}'.format(x,y,z))
    return x, y, z

def isHorizontal(x, y, z):
    """Return if the board is horizontal (flat)
    """
    # x value is close to zero, leaving some tolerance
    return abs(x) < 30

def isVertical(x, y, z):
    """Return if the board is vertical (standing up)
    """
    # x value is near the maximum, with some tolerance
    return abs(x) > 200

def printOrientation():
    global photoRecentlyTaken
    
    x, y, z = getAccelerometerValues()
    horizontal = isHorizontal(x,y,z)
    vertical = isVertical(x,y,z)
    print 'H: ', horizontal
    print 'V: ', vertical
    
    recentOpenStates.append((horizontal, vertical))
    
    if isReadyToTakePhoto(recentOpenStates) and not photoRecentlyTaken:
        takePhoto()
        photoRecentlyTaken = True;        
    
    if not horizontal and vertical:
         signalOpen()
         photoRecentlyTaken = False
    else:
        signalClosed()

def isReadyToTakePhoto(states):
    # Check if the queue of states shows it has been closed
    # for the entire waiting period
    closedState = (True, False)
    return states.count(closedState) == states.maxlen
    
def takePhoto():
    print "Taking a photo now"
    camera.capture(imagePath + 'trash.jpg')
    return

led = LED(21)

# How long to wait to be in "steady" state (seconds)
waitTime = 3

# How often readings are taken from the accelerometer (seconds)
readingInterval = 0.2

# Store recent history of states in tuples (horizontal, vertical)
initialState = (False, False)
maxLength = int(waitTime/readingInterval)
recentOpenStates = deque( maxLength * [initialState], maxLength)

# Take a photo only after the can was just opened and closed (and in steady state)
photoRecentlyTaken = True

camera = picamera.PiCamera()
camera.rotation = 270
camera.sharpness = 100
camera.brightness = 50
imagePath = '/tmp/'

try:
    while (True):
        printOrientation()
        sleep(readingInterval)
except KeyboardInterrupt:
    exit()

