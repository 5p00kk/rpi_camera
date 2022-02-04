from gpiozero import LED
from gpiozero import Button
from time import sleep
import picamera
import picamera.array
import os
import numpy as np

FILMROLL_PATH = "/home/pi/filmroll/"
FILMROLL_CAP = 100
# Define GPIOs
led_power = LED(26)
led_exposure = LED(6)
led_film = LED(5)
button_1 = Button(4, pull_up=None, active_state=False)

# Define app stat class
class application_status():
    def __init__(self):
        self.film_available, self.photo_id = self.check_filmroll()
        print("Extracted id", self.photo_id)
    def update_status(self): 
        self.film_available, self.photo_id = self.check_filmroll()
        print("Extracted id", self.photo_id)
    def check_filmroll(self):
        files = [f for f in os.listdir(FILMROLL_PATH) if os.path.isfile(os.path.join(FILMROLL_PATH, f))]
        if len(files) == 0:
            id = 0
        else:
            id=len(files)
        return len(files)<FILMROLL_CAP, id

# Create application status
status = application_status()
camera = picamera.PiCamera()
camera.framerate = 1
camera.resolution = (1280, 720)
camera.shutter_speed = 2000
#camera.brightness = 100
sleep(2)
camera.exposure_mode = "off"
print(camera.exposure_speed)
print(camera.iso)
print(camera.exposure_mode)

def take_picture():
    picture_name = os.path.join(FILMROLL_PATH, "photo_" + str(status.photo_id+1) + ".bmp")
    camera.capture(picture_name)

# Button stuff
def button_pressed():
    print("Trigger")
    if(status.film_available):
        led_exposure.on()
        take_picture()
        led_exposure.off()

def button_rel():
    print("Button rel")
    status.update_status()

button_1.when_pressed = button_pressed
button_1.when_released = button_rel

# Update powe led
led_power.on()
# Update film led
status.update_status()

while(True):
    if(status.film_available):
        led_film.off()
    else:
        led_film.on()
    sleep(1)
