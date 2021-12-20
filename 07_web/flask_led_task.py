from flask import Flask
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
def hello():
  return '''
    <p>Hello, Flask!!</p>
    <p>
        <a href="/led/red/on">RED LED ON</a>
        <a href="/led/red/off">RED LED OFF</a>
    </p>
    <p>
        <a href="/led/blue/on">BLUE LED ON</a>
        <a href="/led/blue/off">BLUE LED OFF</a>
    </p>

  '''

@app.route("/led/<op1>/<op2>")
def led_op(op1, op2):
    if op1 == "red":
        if op2 == "on":
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            return '''
                <p>RED LED ON</p>
                <a href="/">Go Home</a>
            '''
        elif op2 == "off":
            GPIO.output(RED_LED_PIN, GPIO.LOW)
            return '''
                <p>RED LED OFF</p>
                <a href="/">Go Home</a>
            '''
    elif op1 == "blue":
        if op2 == "on":
            GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
            return '''
                <p>BLUE LED ON</p>
                <a href="/">Go Home</a>
            '''
        elif op2 == "off":
            GPIO.output(BLUE_LED_PIN, GPIO.LOW)
            return '''
                <p>BLUE LED OFF</p>
                <a href="/">Go Home</a>
            '''

# @app.route("/led/on")
# def led_on():
#   return '''
#     <p>LED ON</p>
#     <a href="/">Go Home</a>
#   '''

# @app.route("/led/off")
# def led_off():
#   return '''
#     <p>LED OFF</p>
#     <a href="/">Go Home</a>
#   '''

# 터미널에서 직접 실행시킨 경우
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    finally:
        GPIO.cleanup()