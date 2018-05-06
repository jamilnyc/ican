import RPi.GPIO as GPIO


class Trapdoor:
    """
    Provides an interface to the trapdoor mechanism. Controls servos top open and close.

    Public Methods:
        open()
        close()
        cleanUp()
    """

    # CONSTANTS
    LEFT_SERVO_PIN = 18
    RIGHT_SERVO_PIN = 24
    PWM_FREQUENCY_HZ = 50
    CLOSE_DC = 7.5
    LEFT_OPEN_DC = 10.5
    RIGHT_OPEN_DC = 4.5

    leftPulse = None
    rightPulse = None

    def __init__(self):
        """
        Initializes the servo pins and closes the trapdoor.
        """
        # Set the mode if not already set
        mode = GPIO.getmode()
        if mode != GPIO.BCM:
            # Using the logical Broadcom numbering instead of the physical board
            GPIO.setmode(GPIO.BCM)

        # Set the servo pins as output
        GPIO.setup(self.LEFT_SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_SERVO_PIN, GPIO.OUT)

        # Initialize Pulse Width Modulation (PWM)
        self.leftPulse = GPIO.PWM(self.LEFT_SERVO_PIN, self.PWM_FREQUENCY_HZ)
        self.rightPulse = GPIO.PWM(self.RIGHT_SERVO_PIN, self.PWM_FREQUENCY_HZ)
        self.leftPulse.start(0)
        self.rightPulse.start(0)

    def open(self):
        """
        Send signal to open trapdoor.
        :return: None
        """
        print "Opening Trapdoor"
        self.leftPulse.ChangeDutyCycle(self.LEFT_OPEN_DC)
        self.rightPulse.ChangeDutyCycle(self.RIGHT_OPEN_DC)

    def close(self):
        """
        Send signal to close trapdoor.
        :return:
        """
        print "Closing Trapdoor"
        self.leftPulse.ChangeDutyCycle(self.CLOSE_DC)
        self.rightPulse.ChangeDutyCycle(self.CLOSE_DC)

    def cleanUp(self):
        """
        Returns all pin configurations to their default (safe) state and stops outputting.
        :return: None
        """
        self.leftPulse.stop()
        self.rightPulse.stop()
        GPIO.cleanup()

