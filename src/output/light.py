import RPi.GPIO as GPIO


class Light:
    """
    Class to control output LED.

    Public Methods:
        turnOn()
        turnOff()
    """

    pinNumber = None

    def __init__(self, pinNumber):
        """
        Initialize the given pin as an output.
        :param pinNumber: Board pin number as an integer
        """
        # Set the mode if not already set
        mode = GPIO.getmode()
        if mode != GPIO.BCM:
            GPIO.setmode(GPIO.BCM)

        # Set the LED pin to be an output
        GPIO.setup(pinNumber, GPIO.OUT)
        self.pinNumber = pinNumber

    def turnOn(self):
        """
        Turn on the LED.
        :return: None
        """
        GPIO.output(self.pinNumber, GPIO.HIGH)

    def turnOff(self):
        """
        Turn off the LED.
        :return: None
        """
        GPIO.output(self.pinNumber, GPIO.LOW)

    def cleanUp(self):
        """
        Returns all pin configurations to their default (safe) state and stops outputting.
        :return: None
        """
        self.turnOff()
        GPIO.cleanup()
