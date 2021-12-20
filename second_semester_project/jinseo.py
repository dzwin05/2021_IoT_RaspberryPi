import cv2
import RPi.GPIO as GPIO
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

#OLED
# Setting some variables for our reset pin etc.
RESET_PIN = digitalio.DigitalInOut(board.D4)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=RESET_PIN)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
#OLED 세팅 끝

body_cascade = cv2.CascadeClassifier("./xml/face.xml")
cam = cv2.VideoCapture(0)

bz_pin=16 
green_led_pin=5
red_led_pin=6
yellow_led_pin=13
power_bt_pin=23
reset_bt_pin=24
buzzer_bt_pin=25
last_cap_line1=" "
last_cap_line2=" "
cap_num=0
GPIO.setmode(GPIO.BCM)

bz=1
power=1
clock=1
captured=0

#gpio setup
GPIO.setup(bz_pin, GPIO.OUT)
GPIO.setup(yellow_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(power_bt_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reset_bt_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer_bt_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#기본값
GPIO.output(green_led_pin,GPIO.HIGH)
GPIO.output(red_led_pin,GPIO.HIGH)
GPIO.output(yellow_led_pin, GPIO.HIGH)
time.sleep(1)
GPIO.output(green_led_pin,GPIO.LOW)
GPIO.output(red_led_pin,GPIO.LOW)
GPIO.output(yellow_led_pin, GPIO.LOW)

def reset():
  cap_num=0
  pass

if not cam.isOpened():
  print('Camera open failed')
  exit()

while True:
  #스위치
  if GPIO.input(buzzer_bt_pin): # 부저 on/off 스위치
    if bz == 1: # bz가 1일때 on, -1일때 off
      GPIO.output(yellow_led_pin,GPIO.HIGH)
      bz*=-1
    elif bz == -1:
      GPIO.output(yellow_led_pin,GPIO.LOW)
      bz*=-1

  if GPIO.input(power_bt_pin): # 전체 on/off 스위치
    if power == 1: # power가 1일때 on, -1일때 off
      GPIO.output(green_led_pin,GPIO.HIGH)
      power*=-1
    elif power == -1:
      GPIO.output(green_led_pin,GPIO.LOW)
      power*=-1

  if GPIO.input(reset_bt_pin): # reset 스위치
    reset()
    GPIO.output(red_led_pin,GPIO.LOW)

  #카메라
  ret, frame = cam.read()
  if not ret:
    break
  if clock==0:
    if type(locations)==tuple:
      clock=1
  gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  
  locations=body_cascade.detectMultiScale(gray)
  for(x,y,w,h) in locations:
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
  tm = time.localtime(time.time())
  string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
  if type(locations)!=tuple and clock == 1:
    cv2.imwrite(string+".jpg",frame)
    captured=1
    clock=0
  cv2.imshow("cam", frame)
  #카메라 촬영후 액션
  if captured:
    cap_num+=1
    GPIO.output(red_led_pin,GPIO.HIGH)
    last_cap_line1=time.strftime('%Y-%m-%d ', tm)
    last_cap_line2=time.strftime('%I:%M:%S %p ', tm)
    # if bz:
    #   pwm=GPIO.PWM(bz_pin,262)
    #   pwm.start(10)
    #   time.sleep(2)
    #   pwm.ChangeDutyCycle(0)

  #OLED
  draw.text((0, 0), last_cap_line1, font=font, fill=255)
  draw.text((0, 25), last_cap_line2, font=font, fill=255)
  draw.text((0, 50), str(cap_num), font=font, fill=255)
  
  # Display image
  oled.image(image)
  oled.show()
  #부저
  
  
  if cv2.waitKey(10) == 13:
    break