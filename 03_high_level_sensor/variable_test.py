#pin 번호

#초록 LED : 4
#빨강 LED : 5

# 피에조 오른쪽 : 6
# 피에조 왼쪽 : 13

# PIR 오른쪽 : 18
# PIR 왼쪽 : 19

# 7segment A, b, c, d, e, f, g : 20, 21, 22, 23, 24, 25, 26

import RPi.GPIO as GPIO
import time

GLED_PIN = 4
RLED_PIN = 5

RBUZZER_PIN = 6
LBUZZER_PIN = 13

RPIR_PIN = 18
LPIR_PIN = 19

SEGMENT_PINS = [20, 21, 22, 23, 24, 25, 26]

GPIO.setmode(GPIO.BCM)

GPIO.setup(GLED_PIN, GPIO.OUT)
GPIO.setup(RLED_PIN, GPIO.OUT)
GPIO.setup(RBUZZER_PIN, GPIO.OUT)
GPIO.setup(LBUZZER_PIN, GPIO.OUT)
GPIO.setup(RPIR_PIN, GPIO.IN)
GPIO.setup(LPIR_PIN, GPIO.IN)
for segment in SEGMENT_PINS:
  GPIO.setup(segment, GPIO.OUT)
  GPIO.output(segment, GPIO.LOW)


Rpwm = GPIO.PWM(RBUZZER_PIN, 262)
Lpwm = GPIO.PWM(LBUZZER_PIN, 300)
Rpwm.start(50) #duty cycle (0~100)
Lpwm.start(50) #duty cycle (0~100)
data = [[1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 1, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 1, 0, 1, 1]]  # 9

try :
  GPIO.output(GLED_PIN, GPIO.HIGH)
  GPIO.output(RLED_PIN, GPIO.HIGH)
  time.sleep(1)
  GPIO.output(GLED_PIN, GPIO.LOW)
  GPIO.output(RLED_PIN, GPIO.LOW)
  time.sleep(1)
  Rpwm.ChangeDutyCycle(0)
  Lpwm.ChangeDutyCycle(0)

  whileOut = 0

  for i in range(10):
    for j in range(len(SEGMENT_PINS)):
      GPIO.output(SEGMENT_PINS[j], data[i][j])
      time.sleep(0.05)
    time.sleep(0.3)
  for i in range(len(SEGMENT_PINS)):
    GPIO.output(SEGMENT_PINS[i], 0)
    time.sleep(0.05)

  while True:
    RPIR_val = GPIO.input(RPIR_PIN)
    LPIR_val = GPIO.input(LPIR_PIN)
    if LPIR_val == GPIO.HIGH:
      print("왼쪽 PIR")
    else: print("인식 안됨")
    # if RPIR_val == GPIO.HIGH:
    #   print("오른쪽 PIR")
    #   if LPIR_val == GPIO.HIGH:
    #     print("왼쪽 PIR 인식됐다")
    #   else :
    #     print("인식됐다")
    # else:
    #   if LPIR_val == GPIO.HIGH:
    #     print("왼쪽 PIR 인식됐다")
    #   else:
    #     print("인식 안됌")

finally:
  GPIO.cleanup()
  Rpwm.stop()
  Lpwm.stop()