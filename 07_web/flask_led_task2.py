from flask import Flask, render_template
import RPi.GPIO as GPIO

RED_LED_PIN = 5
BLUE_LED_PIN = 6

# flask 객체 생성
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)


# 0.0.0.0:5000/
@app.route("/")
def home():
  return render_template('led2.html')

@app.route("/led/<color>/<op>")
def led_op(color, op):
    if color == "red":
        if op == "on":
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            return "RED LED ON"
            
        elif op == "off":
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            return "RED LED OFF"
            
    elif color == "blue":
        if op == "on":
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
            return "BLUE LED ON"
            
        elif op == "off":
            GPIO.output(BLUE_LED_PIN, GPIO.LOW)
            return "BLUE LED OFF"

# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    finally:
        GPIO.cleanup()