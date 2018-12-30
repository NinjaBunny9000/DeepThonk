import serial, time


try:
    led_strip = serial.Serial('COM24')
except:
    print('SERIAL FOR SFX NOT CONNECTED')