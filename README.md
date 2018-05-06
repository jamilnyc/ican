# iCan
### IoT Final Project Set Up Instructions
#### Original Designers and Contributors
```
Murshed J. Ahmed      (mja2196 at columbia.edu)
Shijun "Scott" Hou    (sh3658 at columbia.edu)
Robert Fea            (rf2638 at columbia.edu)
```

## Initial Platform Setup
* This project uses a `Raspberry Pi 3 Model B`.
* The operating system is `Raspbian`, installed with the NOOBS installer.
* An HDMI Cable and HDMI capable monitor is recommended for initial setup and debugging.
* Configure a wireless network connection.
  * Edit the file `/etc/wpa_supplicant/wpa_supplicant.conf`
  
    ```
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    
    network={
        ssid="My Unsecured WiFi Network"
        key_mgmt=NONE
    }
    ```

## Required Python Packages
* Generally they can be installed with `sudo pip install package_name_here`
* Adafruit packages require manual setup with [instructions here](https://github.com/adafruit/Adafruit_Python_ADXL345).
```
Package Name      Version
----------------- -------
Adafruit-ADXL345  1.0.1
Adafruit-GPIO     1.0.3
Adafruit-PureIO   0.2.1
boto3             1.6.18
botocore          1.9.18
gpiozero          1.4.1
numpy             1.12.1
picamera          1.13
pip               9.0.1
requests          2.18.4
RPi.GPIO          0.6.3
simplejson        3.10.0
urllib3           1.22
weather-api       1.0.2
```


## Project Directories
Can be found after cloning this repository

### `lambda`
* Contains deployment pacakge for AWS Lambda function that generates nutrition reports.
* Files in this directory should be imported into AWS Lambda.

### `test_scripts`
* Contains throwaway or one-time use only scripts
  * Testing API Calls
  * Hardware Interfacing Examples
  * Experimenting with component configurations and settings

### `src`
* Contains _proper_ project source code for running the main program.
  * `src/sensors` contains modules that abstract functionality for sensor inputs
  * `src/output` contains modules that abstract functionality for outputs
  * `src/api` contains modules that interact with third party APIs
  * `config.txt` should be updated with AWS keys

## Detailed Project Setup Instructions

### Parts List
* [Raspberry Pi Board](https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_3)
* [Accelerometer](https://www.ebay.com/itm/SunFounder-Digital-Accelerometer-ADXL345-Module-for-Arduino-and-Raspberry-Pi/322648202255?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* [Camera](https://www.ebay.com/itm/Camera-Module-Board-5MP-Webcam-Video-1080p-720p-for-Raspberry-Pi-3-US-Seller/222538791275?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* [Trash Can](https://www.amazon.com/dp/B0013CKQDK)
* [Breadboard](https://www.ebay.com/itm/Elegoo-3pcs-MB-102-Breadboard-830-Point-Solderless-Prototype-PCB-Board-Kit-fo/302605224255?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* [Dupont Breadboard Wires](https://smile.amazon.com/gp/product/B01MU0IMFF/ref=oh_aui_search_detailpage?ie=UTF8&psc=1)
* [Board Mounting Plate](https://www.ebay.com/itm/Arduino-Raspberry-Pi-Holder-Breadboard-SunFounder-RAB-5-in-1-Base-Plate-Case-3/273060258858?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649)
* [Servo Motors (two)](https://www.amazon.com/LewanSoul-LD-27MG-Standard-Digital-Aluminium/dp/B07569WJ1M/ref=sr_1_1_sspa?s=electronics&ie=UTF8&qid=1520664264&sr=1-1-spons&keywords=servo+motor&psc=1)


### Main Program Startup
* Edit the `/etc/rc.local` file to run commands at start up.
* You may wish to include one for emailing Raspberry Pi's IP address at boot time
* Assuming you have cloned the repository to `/home/pi/Documents/ican-project`
  * Add the following line to `/etc/rc.local` to begin executing the main program on boot and dump the output to a file:
  * `/usr/bin/python /home/pi/Documents/ican-project/src/ican.py &> /tmp/ican.txt`

### Accelerometer Setup
* Refer to the `src/sensors/lid.py` module.
* Connect the following pins from the Raspberry Pi to the ADXL345 Accelerometer

  ```
  Raspberry Pi      ADXL345
  3.3 V             3.3 V
  GND               GND
  SCL1 (Pin 5)      SCL
  SDA1 (Pin 3)      SDA
  3.3 V             CS
  GND               SDO
  -                 INT1
  -                 INT2
  ```
* Look for an LED lighting up when connected.

### Camera Setup
* Using the ribbon connector tape connector, insert one end to the Pi Camera
* Insert the other end to the Raspberry Pi's Camera port
  * This is between the HDMI connector and the audio jack
  * Labelled on the PCB as `CAMERA`

### Open Indicator LED Setup
* This is simply and LED to indicate if the Lid is open or not
* Positive lead goes to Raspberry Pi GPIO 21 (Pin 40)
* Negative lead is connected to a small resistor (approx 100 ohms)
* Resistor is connected in series to common `GND`

### Servo and Trapdoor Setup
* Servos are mounted and screwed down on the back of the trash can, using the mounting flanges.
* A wide hole must be drilled for the output axis into the trash can.
* Two flaps made of corrugated plastic sheets must be cut for the trapdoor.
* The `GND` wires of both servos must go to common ground (of the Raspberry Pi)
* The `VCC` wires of both servos must go to an external battery source providing approximately 7 volts
* The signal wires of each servo must go a GPIO pin on the Raspberry Pi.
  * Refer to `src/output/trapdoor.py`.
  * GPIO 18 (Pin 12) and GPIO 24 (Pin 18)
  
### Trash Can Setup
* Mount the Raspberry Pi, Breadboard, Accelerometer and Camera to Board Holder.
* Screw the Board Holder into the lid of the trash can.
* Insert USB Power Cable through the back of the trash can (or create your own hole).
* Once powered on, the board should begin running the main program.
  * You can tell the program is running by the Camera LED being on

### Nutritionix API Setup
* [Sign up](https://developer.nutritionix.com/signup) for a developer account with Nutritionix.
* Replace your API keys in `lambda/nutrition.py`

### AWS Setup
* Sign up for an [AWS Account](https://aws.amazon.com). Free Tier is sufficient.
* Create a Role with Cognito and IAM
* Replace the `COGNITO_ID` in `src/api/aws.py`
* In the file `src/config.txt` place your keys from your AWS account.
  * The values should be one per line
    * Account ID
    * Identity Pool ID
    * Role ARN

#### S3 Setup
* Simply create a new bucket for the project and update the information in `src/api/s3.py`

#### Machine Learning Setup
* Create a new classification model in AWS ML
* Use the training data format in `test_scripts/training_data_ican.csv`
* Create a realtime endpoint and update the file in `src/api/prediction.py`

#### DynamoDB Setup
* Create a new database table
* Update the name in `src/api/database.py`

#### SNS Setup
* Create a new topic in SNS.
* Add yourself (your cell phone number) as a subscriber.
* Update the information in `src/api/notification.py`

#### Lambda Setup
* Create a new Lambda function making sure that it has a role with full access to
  * DynamoDB
  * SNS
  * S3
* Import the deployment package files in the `lambda` directory



## Useful commands

### Image Viewing on the Command Line
* Run the command `feh /path/to/my/image.jpg`
* Can also use wildcards to view multiple images
 * `feh pic*`
 * Would match `pic`, `picture`, `pic_001`, etc.
 * Use left/right arrow keys to navigate
 * Images are generally loaded in alphabetical order

### Troubleshooting
* Under normal circumstances, with a stable network, the iCan should immediately start running once plugged in
 * You can tell the program is running if the red camera light is on and the "Open Indicator" LED responds to movement
* If the program is not running _but_ you know the IP address
 * SSH into the Raspberry Pi
 * Clear the `/tmp` directory of all text files
 * Run the main iCan program `python /home/pi/Documents/ican-project/src/ican.py`
* If the program is not running _and_ you don't know the IP address
 * Connect the portable monitor via HDMI
 * Open a terminal and run the same commands above
 * Alternatively you can get the IP address of the `wlan0` interface (use the command `ifconfig`)
  * Once you have the IP address you can SSH with the credentials above