import RPi.GPIO as GPIO
import time

RED_PIN = 4
YLW_PIN = 5
GRN_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YLW_PIN, GPIO.OUT)
GPIO.setup(GRN_PIN, GPIO.OUT)

GPIO.output(RED_PIN, GPIO.HIGH)
print("red led on")
time.sleep(1)
GPIO.output(RED_PIN, GPIO.LOW)
print("red led off")
time.sleep(1)

GPIO.output(YLW_PIN, GPIO.HIGH)
print("yellow led on")
time.sleep(1)
GPIO.output(YLW_PIN, GPIO.LOW)
print("yellow led off")
time.sleep(1)

GPIO.output(GRN_PIN, GPIO.HIGH)
print("green led on")
time.sleep(1)
GPIO.output(GRN_PIN, GPIO.LOW)
print("green led off")
time.sleep(1)

GPIO.cleanup()