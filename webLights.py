from flask import Flask
from time import sleep
from threading import Timer
from datetime import time, datetime
import RPi.GPIO as GPIO
relay = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
state = {"lights": True}
GPIO.output(relay, state["lights"])
alarmTime = time(10)

app = Flask(__name__)

@app.route('/')
def login():
        return '<button style=" width: 25%; height: 25%; font-size: 300%;" onclick="var req = (new XMLHttpRequest());req.open(\'GET\', \'lights\');req.send();" type="button">Light</button>'

@app.route("/lights")
def lights():
        state["lights"] = not state["lights"]
        GPIO.output(relay, state["lights"])
        return "all good in the hood"

def setAlarm():
        for i in range(10):
                state["lights"] = True
                GPIO.output(relay, state["lights"])
                sleep(0.15)
                state["lights"] = False
                GPIO.output(relay, state["lights"])
                sleep(0.15)
        state["lights"] = True
        GPIO.output(relay, state["lights"])
        timeUntilAlarm = datetime.combine(datetime.now(), alarmTime) - datetime.now()
        secondsUntilAlarm = timeUntilAlarm.total_seconds()
        if secondsUntilAlarm < 0:
                secondsUntilAlarm += 86400
        alarmThread = Timer(secondsUntilAlarm, setAlarm)
        alarmThread.start()
        print secondsUntilAlarm


if __name__ == "__main__":
        timeUntilAlarm = datetime.combine(datetime.now(), alarmTime) - datetime.now()
        secondsUntilAlarm = timeUntilAlarm.total_seconds()
        if secondsUntilAlarm < 0:
                secondsUntilAlarm += 86400
        alarmThread = Timer(secondsUntilAlarm, setAlarm)
        alarmThread.start()
        print secondsUntilAlarm
        app.run(host='0.0.0.0')
