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
    sen, pin = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    now = datetime.datetime.now()
    if sen is not None and pin is not None:
      display.lcd_display_string(now.strftime("%x%X"), 1)
      display.lcd_display_string('%.1f*c, %.1f%%' % (pin, sen), 2)

finally :
    print("Cleaning up!")
    display.lcd_clear()