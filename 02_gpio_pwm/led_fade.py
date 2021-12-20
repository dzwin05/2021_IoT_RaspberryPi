import RPi.GPIO as GPIO
import time

LED_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 50)
pwm.start(0)

try:
  for i in range(3):
    for j in range(0, 101, 1):
      pwm.ChangeDutyCycle(j)
      time.sleep(0.01)
    
    for j in range(100, -1, -1):
      pwm.ChangeDutyCycle(j)
      time.sleep(0.01)

finally:
  pwm.stop()
  GPIO.cleanup()                  