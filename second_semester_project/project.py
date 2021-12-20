import cv2
import RPi.GPIO as GPIO
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# OLED
RESET_PIN = digitalio.DigitalInOut(board.D4)

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=RESET_PIN)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# 얼굴 인식 모듈 불러오기
face_cascade = cv2.CascadeClassifier("./xml/face.xml")

# 카메라 켜기
cam = cv2.VideoCapture(0)

# 변수 선언
buzzer_pin=16 
red_led_pin=6
yellow_led_pin=13
reset_bt_pin=24
buzzer_bt_pin=25
last_cap_line1=" "
last_cap_line2=" "

cap_num=0
buzzer=1
clock=1
captured=0 

GPIO.setmode(GPIO.BCM)


# GPIO setup
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(yellow_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(reset_bt_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer_bt_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

pwm=GPIO.PWM(buzzer_pin,262)

GPIO.output(red_led_pin,GPIO.HIGH)
GPIO.output(yellow_led_pin, GPIO.HIGH)
time.sleep(1)
GPIO.output(red_led_pin,GPIO.LOW)
GPIO.output(yellow_led_pin, GPIO.LOW)

# 카메라 확인
if not cam.isOpened():
  print('Camera open failed')
  exit()


while True:
  # 부저 전원 통제
  if GPIO.input(buzzer_bt_pin):
    if buzzer == 1:
      GPIO.output(yellow_led_pin,GPIO.HIGH) # 노란색 led 켜기
      buzzer*=-1
    elif buzzer == -1:
      GPIO.output(yellow_led_pin,GPIO.LOW) # 노란색 led 끄기
      buzzer*=-1

  # 리셋 스위치
  if GPIO.input(reset_bt_pin): 
    cap_num=0 # 사진 개수 초기화
    oled.fill(0) # OLED 초기화
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    GPIO.output(red_led_pin,GPIO.LOW) # 빨간 led 끄가

  # 카메라
  ret, frame = cam.read()
  if not ret:
    break
  if clock==0:
    if type(locations)==tuple: #현재 사진에 얼굴이 인식되지 않으면,
      clock=1 #다음에 사진을 찍을 수 있게 함
  gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  
  locations=face_cascade.detectMultiScale(gray) # 얼굴의 위치 받아오기
  for(x,y,w,h) in locations: # 얼굴에 직사각형 그리기
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
  tm = time.localtime(time.time())
  string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm) # 날짜, 시간 저장
  if type(locations)!=tuple and clock == 1: # 현재 사진에 직사각형이 있으며, 이전 프레임에 얼굴이 인식되지 않았다면
    cv2.imwrite(string+".jpg",frame) # 사진 저장
    captured=1
    clock=0 #연속해서 촬영되는 것을 방지 하기 위해 이전 프레임에 얼굴이 있었음을 알려주는 변수
  cv2.imshow("cam", frame)

  # 카메라 촬영후 동작
  if captured:
    cap_num+=1 # 사진 횟수 올리기
    GPIO.output(red_led_pin,GPIO.HIGH) # 빨간 led 켜기

    # OLED
    last_cap_line1=time.strftime('%Y-%m-%d ', tm) # 날짜 받아오기
    last_cap_line2=time.strftime('%I:%M:%S %p ', tm) # 시간 받아오기
    image = Image.new("1", (oled.width, oled.height)) # OLED 출력
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), last_cap_line1, font=font, fill=255)
    draw.text((0, 22), last_cap_line2, font=font, fill=255)
    draw.text((0, 44), str(cap_num), font=font, fill=255)
    oled.image(image)
    oled.show()
    captured = 0 # 사진 찍힘 변수 초기화

    if buzzer == -1: # 부저 알림 기능 켜져있을 때 부저 알리기
      pwm.start(10)
      time.sleep(2)
      pwm.ChangeDutyCycle(0)

  if cv2.waitKey(10) == 13: # enter 입력 기다리기
    pwm.stop()
    GPIO.cleanup()
    break