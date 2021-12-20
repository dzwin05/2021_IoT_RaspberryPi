import RPi.GPIO as GPIO
import time

RBUZZER_PIN = 6
LBUZZER_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(RBUZZER_PIN, GPIO.OUT)
GPIO.setup(LBUZZER_PIN, GPIO.OUT)

#주파수 : 도(262Hz)
Rpwm = GPIO.PWM(RBUZZER_PIN, 262)
Lpwm = GPIO.PWM(LBUZZER_PIN, 262)
Rpwm.start(50) #duty cycle (0~100)
Lpwm.start(50) #duty cycle (0~100)

try:
    Rpwm.ChangeFrequency(330)
    Lpwm.ChangeFrequency(330)
    for i in range (2):
        time.sleep(0.4)
        Rpwm.start(0)
        Lpwm.start(0)
        time.sleep(0.4)
        Rpwm.start(50)
        Lpwm.start(50)

finally:
    Rpwm.stop()
    Lpwm.stop()
    GPIO.cleanup()