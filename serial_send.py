try:
   from serial_conf import led_strip
except ImportError:
   pass
import time


def led_fx(cmd_name, cmd_char):
   try:
      print('{} triggered!'.format(cmd_name))
      led_strip.write(cmd_char.encode())
   except:
      print('{} LED REACTION NOT TRIGGERED'.format(cmd_name))