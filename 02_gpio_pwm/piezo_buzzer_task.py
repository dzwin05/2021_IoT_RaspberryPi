import RPi.GPIO as GPIO
import time

BUZZER_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(10) #duty cycle (0~100)

#주파수 : 도(262Hz) 레(294Hz) 미(330Hz) 파(349Hz) 솔(392Hz) 라(440Hz) 시(494Hz) 도(523Hz)
melody = [262, 294, 330, 349, 392, 440, 494, 523]
schoolbell1 = [392, 392, 440, 440, 392, 392]
schoolbell2 = [392, 392, 330, 330]
schoolbell3 = [392, 330, 294, 330]

try:
  for i in schoolbell1:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.ChangeFrequency(330)
  time.sleep(1)
  for i in schoolbell2:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.ChangeFrequency(294)
  time.sleep(2)
  for i in schoolbell1:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.ChangeFrequency(330)
  time.sleep(1)
  for i in schoolbell3:
    pwm.ChangeFrequency(i)
    time.sleep(0.5)
  pwm.ChangeFrequency(262)
  time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup() 