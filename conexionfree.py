import signal
import sys

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import pyupm_i2clcd as lcd
import dweepy


# create the button object using GPIO pin 0
button = grove.GroveButton(8)

# create the TTP223 touch sensor object using GPIO pin 0
touch = ttp223.TTP223(7)

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

myLcd.setCursor(0,0)
# RGB Blue
#myLcd.setColor(53, 39, 249)

# Read the input and print, waiting one second between readings
count = 0
while 1:
    if button.value():
      count = count +1
    if touch.isPressed():
      count = count - 1
    myLcd.setCursor(1,2)
    myLcd.write("%6d"%count)
    dato={}
    dato["envio1"]=count
    dweepy.dweet_for("OscarOrdaz",dato)

    time.sleep(.5)

# Delete the button object
del button
# Delete the touch sensor object
del touch

