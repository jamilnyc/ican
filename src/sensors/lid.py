# Import the ADXL345 (accelerometer) module.
import Adafruit_ADXL345


class Lid:
    """Class for getting the current state of the Lid"""

    # Numerical thresholds estimated through trial and error
    HORIZONTAL_THRESHOLD = 30
    VERTICAL_THRESHOLD = 175

    def __init__(self):
        self.accelerometer = Adafruit_ADXL345.ADXL345()

    def getAccelerometerValues(self):
        """Return the x, y and z values of the accelerometer"""
        x, y, z = self.accelerometer.read()
        return x, y, z

    def isHorizontal(self):
        """Return if the board is horizontal (flat)"""
        x, y, z = self.getAccelerometerValues()

        # x value is close to zero, leaving some tolerance
        return abs(x) < self.HORIZONTAL_THRESHOLD

    def isVertical(self):
        """Return if the board is vertical (standing up)"""
        x, y, z = self.getAccelerometerValues()

        # x value is near the maximum, with some tolerance
        return abs(x) > self.VERTICAL_THRESHOLD