from gpiozero import LED, Button
from time import sleep
import os
from subprocess import check_output
from mpd import MPDClient
import re
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

volume = 0
current = "None"
client = MPDClient()
mpc = PCF8574_GPIO(0x27)
lcd = Adafruit_CharLCD(pin_rs=0,pin_e=2,pins_db=[4,5,6,7],GPIO=mpc)
status = "None"

def toggle():
	os.popen("mpc toggle")
	getPlayPause()
	printToScreen()

def volumeUp():
	lcd.clear()
	global volume
	v = int(volume)
	x = v % 10
	if x > 0: v += 10 - x
	else: v += 10
	if v <= 100:
		volume = v
		setVolume(volume)
		printToScreen()

def volumeDown():
	lcd.clear()
	global volume
	v = int(volume)
	x = v % 10
	if x > 0: v -= x
	else: v -= 10
	if v >= 0:
		volume = v
		setVolume(volume)
		printToScreen()

def nextTrack():
	os.popen("mpc next")
	getCurrentTrack()
	printToScreen()

def getInitialVolume():
	global volume
	c = str(client.status())
	x = re.search("volume': '\d*'",c)
	if x:
        	v = x.group().split(" ")[1].strip("'")
		volume = v

def getCurrentTrack():
	global current
	c = str(client.currentsong())
	x = re.search("name': '.*?'",c)
	if x:
        	current = x.group().split(": ")[1].strip("'")

def printToScreen():
	global current
	global volume
	lcd.clear()
	v = str(volume)
	s = current + "\nVol: " + v + " " + status
	lcd.setCursor(0,0)
	lcd.message(s)

def setVolume(vol):
	os.popen("mpc volume " + str(vol))

def getPlayPause():
	global status
	tmp = re.search("\[.*?\]", str(check_output(["mpc", "status"])))
	if tmp:
		status = tmp.group().strip("[]")
		if status == "playing":
			status = "Playing"
		else:
			status = "Paused"
	else:
		status = "None"
client.connect("localhost",6600)
client.repeat(1)

pause = Button(22)
pause.when_pressed = toggle

up = Button(17)
up.when_pressed = volumeUp

down = Button(27)
down.when_pressed = volumeDown

next = Button(21)
next.when_pressed = nextTrack

getInitialVolume()
getCurrentTrack()
getPlayPause()

mpc.output(3,1)
lcd.begin(16,2)

printToScreen()

while True:
	getCurrentTrack()
	getPlayPause()
