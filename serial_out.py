import serial, time

serial_send = serial.Serial('COM24')

time.sleep(5)

serial_send.write(b'w')