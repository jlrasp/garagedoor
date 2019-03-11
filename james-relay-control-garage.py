'''
Alexa Custom Skill to control Garage Door using a relay
    - Uses the flask-ask library

Usage:
Alexa, tell garage door to open
Alexa, ask garage door to close


Last Modified: James Luna 1/22/2019
'''

from flask import Flask, render_template
from flask_ask import Ask, statement, question
import RPi.GPIO as GPIO #use GPIO library
import time #use time library
import datetime
import os
from picamera import PiCamera
from time import sleep

#initializing GPIO
GPIO.setwarnings(False)
outputPin = 11 #pin 11 is connected to the relay board
GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(outputPin, GPIO.OUT)   # Set pin's mode as output
GPIO.output(outputPin, GPIO.HIGH) # Set outputPin  high to turn off the device

#initializing flask ask
app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    welcome_text = render_template('welcome_text')
    return question(welcome_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    reprompt_text = render_template('command_reprompt')
    return question(reprompt_text)

@ask.intent('OpenCloseIntent')
def control(OpenClose):
    command = OpenClose
    if command is None:
        #no command was given
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)
    elif command == "open" or command == "close":
        #command1 = '/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Downloads/GarageDoor/*.jpg "/"'
        #command2 = "rm /home/pi/Downloads/GarageDoor/*.*"
        GPIO.output(outputPin, GPIO.LOW)  # Turn relay on
        time.sleep(.5) # Pause for 1 seconds
        GPIO.output(outputPin, GPIO.HIGH) # Turn relay off
        time.sleep(3) # Pause for 3 seconds
        #date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        #camera = PiCamera()
        #camera.resolution = (2560,1923)
        #camera.capture("/home/pi/Downloads/GarageDoor/"+ date + ".jpg") #Take Photo and place in folder
        #camera.close()
        response_text = render_template('command', OpenCloseCommand=command)
        #os.system(command1)
        #os.system(command2)
        return statement(response_text).simple_card('Command', response_text)
    else:
        #a valid command was not given
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)
    
@ask.intent('PictureIntent')
def control(PicturePhoto):
    command3 = PicturePhoto
    if command3 is None:
        #no command was given
        reprompt_text3 = render_template('command3_reprompt')
        return question(reprompt_text)
    elif command3 == "picture" or command3 == "photo":
        command1 = '/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Downloads/GarageDoor/*.jpg "/Photos/GarageDoor/"'
        command2 = "rm /home/pi/Downloads/GarageDoor/*.*"
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        camera = PiCamera()
        camera.resolution = (2560,1923)
        camera.capture("/home/pi/Downloads/GarageDoor/"+ date + ".jpg") #Take Photo and place in folder
        camera.close()
        response_text3 = render_template('command3', PicturePhotoCommand=command3)
        os.system(command1)
        os.system(command2)
        return statement(response_text3).simple_card('Command3', response_text3)
    else:
        #a valid command was not given
        reprompt_text3 = render_template('command3_reprompt')
        return question(reprompt_text3)
    
if __name__ == '__main__':
    app.run(debug=True)
