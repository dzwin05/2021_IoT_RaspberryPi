import spidev
import time

#SPI 인스턴트 생성 
spi = spidev.SpiDev()

#SPI 통신 시작
spi.open(0, 0) #bus : 0, dev(장치 번호):0  (CE0:0, CE1:1)

#SPI 통신 최대 속도 설정
spi.max_speed_hz = 1000000

# 0~7까지 채널에서 SPI 데이터 읽기
def analog_read(channel):
  # [byte_1, byte_2, byte_3]
  # byte_1 : 1
  # byte_2 : channel config, 1000 000 : channel 0
  # byte_3 : 0(ignored)
  ret = spi.xfer2([1, (8 + channel) << 4, 0])
  adc_out = ((ret[1] & 3) << 8) + ret[2]
  return adc_out

try:
    while True:
      ldr_value = analog_read(0)
      print("LDR Value : %d" % ldr_value )
      time.sleep(0.05)
finally : 
    spi.close()