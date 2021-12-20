import Adafruit_DHT
from lcd import drivers
import time
import datetime

sensor = Adafruit_DHT.DHT11
DHT_PIN = 4

display = drivers.Lcd()

try:
  print("Writing to display")
  while True:
    h, t = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    now = datetime.datetime.now()
    if h is not None and t is not None:
      display.lcd_display_string(now.strftime("%x%X"), 1)
      display.lcd_display_string('%.1f*c, %.1f%%' % (t, h), 2)

finally :
    print("Cleaning up!")
    display.lcd_clear()