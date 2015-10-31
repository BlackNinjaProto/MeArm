#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
pwm.setPWMFreq(60)

BaseMin = 180
BaseMax = 650
UpperMin = 250
UpperMax = 500
LowerMin = 350
LowerMax = 575
LowerHalfRange = ((LowerMax - LowerMin) / 2) # 165
LowerMid = LowerMin + LowerHalfRange
FinalUpperMin = UpperMin
FinalUpperMax = UpperMax

def updateFinalUppers(lowerArmPos):
  global FinalUpperMin
  global FinalUpperMax

  FinalUpperMin = UpperMin
  FinalUpperMax = UpperMax
  if lowerArmPos > LowerMid:
    howMuchFurther = lowerArmPos - LowerMid    
    FinalUpperMax = UpperMax - ((howMuchFurther * 50) / LowerHalfRange)
  elif lowerArmPos < LowerMid:
    howMuchBack = LowerMid - lowerArmPos
    FinalUpperMin = (UpperMin + (howMuchBack * 90) / LowerHalfRange)
  print FinalUpperMax
  print FinalUpperMin

def fullTest():
  pwm.setPWM(0, 0, BaseMin)
  pwm.setPWM(4, 0, LowerMin)
  updateFinalUppers(LowerMin)
  pwm.setPWM(1, 0, FinalUpperMin) # Can got to 250 when lower arm is contracted
  time.sleep(1)
  pwm.setPWM(0, 0, 411)
  pwm.setPWM(1, 0, 411)
  pwm.setPWM(4, 0, 411)
  time.sleep(1)
  pwm.setPWM(0, 0, BaseMax)
  pwm.setPWM(4, 0, LowerMax)
  updateFinalUppers(LowerMax)
  pwm.setPWM(1, 0, FinalUpperMax) # Can go to 500 when lower arm not extended
  time.sleep(1)
  pwm.setPWM(0, 0, 411)
  pwm.setPWM(1, 0, 411)
  pwm.setPWM(4, 0, 411)
  time.sleep(1)

fullTest()

#for i in range(LowerMid, LowerMax):
#  pwm.setPWM(4, 0, i)
#  setUpperArmPos(UpperMax, i)
#  time.sleep(0.1)
  


