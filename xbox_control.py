import time
from threading import Thread
import xbox_read
from Adafruit_PWM_Servo_Driver import PWM

pwm = PWM(0x40)
pwm.setPWMFreq(60)

servoMin = 180
servoMax = 650

pos = 411
pwm.setPWM(0, 0, pos)
time.sleep(1)

class NonBlockingXboxEvent:

    def __init__(self):
        self.event = xbox_read.Event('X2', 0, 0)

        def _read_stream():
            print("Started reading")
            for event in xbox_read.event_stream(deadzone=12000):
                print(event)
                if event.key == 'X2':
                    self.event = event

        self._thread = Thread(target = _read_stream)
        self._thread.daemon = True
        self._thread.start()

reader = NonBlockingXboxEvent()
while (True):
    time.sleep(0.02)
    event = reader.event
    pos = pos + (event.value / 12000)
    if pos > servoMax:
        pos = servoMax
    elif pos < servoMin:
        pos = servoMin
    pwm.setPWM(0, 0, pos)


    
        
