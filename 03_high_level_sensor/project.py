# pin 번호------------

# 초록 LED : 4
# 빨강 LED : 5

# 피에조 오른쪽 : 6
# 피에조 왼쪽 : 13

# PIR 오른쪽 : 18
# PIR 왼쪽 : 19

# 7segment A, b, c, d, e, f, g : 20, 21, 22, 23, 24, 25, 26

import RPi.GPIO as GPIO
import time

GLED_PIN = 4 #초록LED
RLED_PIN = 5 #빨강LED

RBUZZER_PIN = 6 #출구 알림
LBUZZER_PIN = 13 #입구 알림

RPIR_PIN = 18 #출구 센서
LPIR_PIN = 19 #입구 센서

SEGMENT_PINS = [20, 21, 22, 23, 24, 25, 26] #입구에 달 인원수 알리는 장치

# 센서 설정------------

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
Lpwm = GPIO.PWM(LBUZZER_PIN, 262)
Rpwm.start(0) #duty cycle (0~100)
Lpwm.start(0) #duty cycle (0~100)

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

#그외 변수 설정------------
cnt=0
num=cnt + 1 # 처음에 num값과 cnt값을 다르게하여 if문이 돌아가게 함


try :
  while True:
    for j in range(len(SEGMENT_PINS)):  # 7 segment로 방 만의 인원수를 표시한다
      GPIO.output(SEGMENT_PINS[j], data[cnt][j])
      time.sleep(0.05)
    
    if cnt != num:  #방 안의 인원 수가 변하면
      if 0 <= cnt < 5:  # 5명 이하일 때
        GPIO.output(RLED_PIN, GPIO.LOW) # 빨간 LED끄기
        GPIO.output(GLED_PIN, GPIO.HIGH) # 초록 LED켜기
        num=cnt # num 초기화
      if cnt >= 5:  # 5명 이상일 때
        GPIO.output(GLED_PIN, GPIO.LOW) # 초록 LED끄기
        GPIO.output(RLED_PIN, GPIO.HIGH) # 빨간 LED켜기

        for i in range (2): # buzzer 울리기 (경고음)
          Rpwm.start(50)
          Lpwm.start(50)
          time.sleep(0.4)
          Rpwm.start(0)
          Lpwm.start(0)
          time.sleep(0.4)
        num=cnt # num 초기화
    
    RPIR_val = GPIO.input(RPIR_PIN) # 출구 감지
    LPIR_val = GPIO.input(LPIR_PIN) # 입구 감지
    if LPIR_val == GPIO.HIGH: # 입구에 감지되면 인원수 + 1
      cnt+=1
      time.sleep(2)
    if RPIR_val == GPIO.HIGH: # 입구에 감지되면 인원수 - 1
      cnt-=1
      time.sleep(2)

   


finally: #  끝!!
  GPIO.cleanup()
  Rpwm.stop()
  Lpwm.stop()