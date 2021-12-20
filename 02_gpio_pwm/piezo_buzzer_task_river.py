import RPi.GPIO as GPIO
import time

BUZZER_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(10) #duty cycle (0~100)

#주파수 : 도(262Hz) 레(294Hz) 미(330Hz) 파(349Hz) 솔(392Hz) 라(440Hz) 시(494Hz) 도(523Hz)
melody = [262, 294, 330, 349, 392, 440, 494, 523]
piano1 = [440, 415, 440, 415, 440, 330, 440, 294]

try:
  for i in piano1:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.start(0)
  time.sleep(4)
  pwm.start(10)
  pwm.ChangeFrequency(220)
  time.sleep(0.25)
  pwm.ChangeFrequency(277)
  time.sleep(0.25)
  for i in piano1:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.start(0)
  time.sleep(4)
  pwm.start(10)
  pwm.ChangeFrequency(220)
  time.sleep(0.25)
  pwm.ChangeFrequency(277)
  time.sleep(0.25)
finally:
    pwm.stop()
    GPIO.cleanup() 