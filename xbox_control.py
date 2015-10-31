import time
from threading import Thread
import xbox_read
from Adafruit_PWM_Servo_Driver import PWM

pwm = PWM(0x40)
pwm.setPWMFreq(60)

class ServoControl:
    def __init__(self, min_pos, max_pos, start_pos, channel):
        self.min = min_pos
        self.max = max_pos
        self.pos = start_pos
        self.channel = channel
        pwm.setPWM(channel, 0, start_pos)        

    def setPos(self, pos):
        self.pos = self.pos + pos
        if self.pos > self.max:
            self.pos = self.max
        elif self.pos < self.min:
            self.pos = self.min
        pwm.setPWM(self.channel, 0, self.pos) 

Base = ServoControl(180, 650, 411, 0)
Lower = ServoControl(350, 600, 411, 4)
Upper = ServoControl(250, 500, 411, 1)
Jaws = ServoControl(200, 600, 200, 5)
time.sleep(1)

class NonBlockingXboxEvent:

    def __init__(self):
        self.base = xbox_read.Event('X2', 0, 0)
        self.lower = xbox_read.Event('X1', 0, 0);
        self.upper = xbox_read.Event('Y1', 0, 0);
        self.jaws = xbox_read.Event('T', 0, 0);

        def _read_stream():
            print("Started reading")
            for event in xbox_read.event_stream(deadzone=12000):
                if event.key == 'X2':
                    self.base = event
                if event.key == 'X1':
                    self.lower = event
                if event.key == 'Y1':
                    self.upper = event
                if event.key == 'LT':
                    self.jaws = event
                    self.jaws.value = -1 * self.jaws.value
                if event.key == 'RT':
                    self.jaws = event

        self._thread = Thread(target = _read_stream)
        self._thread.daemon = True
        self._thread.start()

reader = NonBlockingXboxEvent()
while (True):
    time.sleep(0.02)
    Base.setPos(reader.base.value / 12000)
    Lower.setPos(reader.lower.value / 12000)
    Upper.setPos(reader.upper.value / 12000)
    Jaws.setPos(reader.jaws.value / 60)

    
        
