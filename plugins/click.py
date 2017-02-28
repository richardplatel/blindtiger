import RPi.GPIO as GPIO
import time

relay_to_pin = {
	1 : 17,
	2 : 18,
	3 : 27,
	4 : 22,
}

button_to_relay = {
  1 : 4,
  2 : 3,
  3 : 1,
  4 : 2,
}


delay = 0.075

def init():
	GPIO.setmode(GPIO.BCM)
	for pin in relay_to_pin.values():
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)

def buttontopin(button):
  return relay_to_pin[button_to_relay[button]]

def press(button):
	pin = buttontopin(button)
	GPIO.output(pin, GPIO.LOW)

def release(button):
	pin = buttontopin(button)
	GPIO.output(pin, GPIO.HIGH)

def click(button):
	press(button)
	time.sleep(delay)
	release(button)

def deinit():
	for pin in relay_to_pin.values():
		GPIO.cleanup(pin)
	

if __name__ == '__main__':
	init()
	for x in range(1, 5):
		click(x)
		time.sleep(0.5)
	deinit()

