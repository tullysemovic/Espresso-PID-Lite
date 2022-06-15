# Imports
import os
from flask import Flask, render_template, send_from_directory  # Import flask
from pathlib import Path
import time
from flask_socketio import SocketIO, emit
import Adafruit_MAX31855.MAX31855 as MAX31855
import RPi.GPIO as GPIO
from simple_pid import PID
import threading
import json
import math
from datetime import datetime
from atexit import register

print("FLASK SERVER STARTING")

# Directory path setup
file_path = Path(os.path.realpath(__file__))
directory_path = file_path.parent.absolute()

# Webserver setup
app = Flask(__name__,
            static_folder=directory_path / "dist/static",
            template_folder=directory_path / "dist")
app.config['SECRET_KEY'] = 'secretkey'

socketio = SocketIO(app, logger=False, cors_allowed_origins="*")

temperature = 0
dataArray = []
userConnected = False
settingsPID = ""

# PID setup (default settings)
P = 1
I = 0.02
D = 3
pid = PID(P, I, D)
pid.sample_time = 0.01
pid.output_limits = (-10, 10)
pid.setpoint = 90

# MAX3188 setup
CLK = 4
CS = 3
DO = 2
sensor = MAX31855.MAX31855(CLK, CS, DO)

# SSR setup
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)


# read PID settings from settings.json
def readPIDSettings():

    # read settings file
    with open(directory_path / "settings_PID.json", 'r') as f:
        data = f.read()
    jsonData = json.loads(data)

    global P
    global I
    global D
    global pid
    global settingsPID

    P = (jsonData['PID']['P'])
    I = (jsonData['PID']['I'])
    D = (jsonData['PID']['D'])
    targetTemperature = jsonData['TargetTemperature']

    settingsPID = {"PID":   {"P": P, "I": I, "D": D},
                   "TargetTemperature": targetTemperature}

    pid = PID(P, I, D)
    pid.sample_time = 0.01
    pid.output_limits = (-10, 10)
    pid.setpoint = targetTemperature

    print("Updated PID settings to: " + str(jsonData))


# readSettings called once at startup to get previously saved PID configuration and global settings
readPIDSettings()

# Webserver Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(directory_path / "dist/favicon.ico")
    
# SOCKET: connect
@socketio.on('connect')
def connect():
    global userConnected
    userConnected = True
    print('user connected to websocket')

# SOCKET: disconnect
@socketio.on('disconnect')
def disconnect():
    global userConnected
    userConnected = False
    print('user disconnected to websocket')

# SOCKET: send temperature to socket connection
@socketio.on('send_temperature')
def temperature_give():
    socketio.emit('recieve_temperature', dataArray)

# SOCKET: update settings file and re-instantiate PID settings
@socketio.on('send_PID')
def PID_update(data):
    writeSettings(data)
    readPIDSettings()
    socketio.emit('give_PID', settingsPID)
    print("SENDING CURRENT SETTINGS")
    print(settingsPID)

# SOCKET: Send PID settings
@socketio.on('get_PID')
def PID_update():
    print("EMIT: give_PID " + str(settingsPID))
    socketio.emit('give_PID', settingsPID)
    print("SENDING CURRENT SETTINGS")
    print(settingsPID)

# function to write data to settings.json file
def writeSettings(data):
    P = data["P"]
    I = data["I"]
    D = data["D"]
    targetTemperature = data["targetTemperature"]

    dictionary = {"PID":   {"P": float(P), "I": float(I), "D": float(D)},
                  "TargetTemperature": float(targetTemperature)}

    # write settings file
    with open(directory_path / "settings_PID.json", 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)

    print("Written settings to file: " + str(dictionary))


# Main PID function
def espresso():
    print("THREAD STARTING")
    global temperature
    global temperatureArray
    global timestampArray

    while(True):

        temperature = sensor.readTempC()
        #internal = sensor.readInternalC()

        date = math.trunc(datetime.today().timestamp() * 1000)

        if (len(dataArray) >= 60):
            dataArray.pop(0)

        dataArray.append({"x": date, "y": temperature})

        output = pid(temperature)
        if(output > 0):
            GPIO.output(21, GPIO.HIGH)
        else:
            GPIO.output(21, GPIO.LOW)

        print("TEMPERATURE: " + str(temperature) +
              " |  PID OUTPUT: " + str(output))

        time.sleep(0.5)

# If the application is termiated (turon off SSR)
@register
def terminate():
    GPIO.output(21, GPIO.LOW)
    print("Goodbye!")

# If the script that was run is this script (we have not been imported)
if __name__ == '__main__':
           
    # Run flask and espresso controller on seperate threads
    threading.Thread(target=lambda: socketio.run(
        app, host="0.0.0.0", port="5000", debug=False)).start()
    threading.Thread(target=espresso).start()
