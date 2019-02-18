
import RPi.GPIO as gpio
import picamera
import time

m11 = 17
m12 = 27
led = 5
buz = 26

button = 19

RS = 18
EN = 23
D4 = 24
D5 = 16
D6 = 20
D7 = 21

HIGH = 1
LOW = 0

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(RS, gpio.OUT)
gpio.setup(EN, gpio.OUT)
gpio.setup(D4, gpio.OUT)
gpio.setup(D5, gpio.OUT)
gpio.setup(D6, gpio.OUT)
gpio.setup(D7, gpio.OUT)
gpio.setup(led, gpio.OUT)
gpio.setup(buz, gpio.OUT)
gpio.setup(m11, gpio.OUT)
gpio.setup(m12, gpio.OUT)
gpio.setup(button, gpio.IN)
gpio.output(led, 0)
gpio.output(buz, 0)
gpio.output(m11, 0)
gpio.output(m12, 0)
data = ""


def capture_image():
    lcdcmd(0x01)
    lcdprint("Please Wait..");
    data = time.strftime("%d_%b_%Y\%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print
    data
    camera.capture('/home/pi/Desktop/Visitors/%s.jpg' % data)
    camera.stop_preview()
    lcdcmd(0x01)
    lcdprint("Image Captured")
    lcdcmd(0xc0)
    lcdprint(" Successfully ")
    time.sleep(2)


def gate():
    lcdcmd(0x01)
    lcdprint("    Welcome  ")
    gpio.output(m11, 1)
    gpio.output(m12, 0)
    time.sleep(1.5)
    gpio.output(m11, 0)
    gpio.output(m12, 0)
    time.sleep(3)
    gpio.output(m11, 0)
    gpio.output(m12, 1)
    time.sleep(1.5)
    gpio.output(m11, 0)
    gpio.output(m12, 0)
    lcdcmd(0x01);
    lcdprint("  Thank You  ")
    time.sleep(2)


def begin():
    lcdcmd(0x33)
    lcdcmd(0x32)
    lcdcmd(0x06)
    lcdcmd(0x0C)
    lcdcmd(0x28)
    lcdcmd(0x01)
    time.sleep(0.0005)


def lcdcmd(ch):
    gpio.output(RS, 0)
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x10 == 0x10:
        gpio.output(D4, 1)
    if ch & 0x20 == 0x20:
        gpio.output(D5, 1)
    if ch & 0x40 == 0x40:
        gpio.output(D6, 1)
    if ch & 0x80 == 0x80:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)

    # Low bits
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x01 == 0x01:
        gpio.output(D4, 1)
    if ch & 0x02 == 0x02:
        gpio.output(D5, 1)
    if ch & 0x04 == 0x04:
        gpio.output(D6, 1)
    if ch & 0x08 == 0x08:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)


def lcdwrite(ch):
    gpio.output(RS, 1)
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x10 == 0x10:
        gpio.output(D4, 1)
    if ch & 0x20 == 0x20:
        gpio.output(D5, 1)
    if ch & 0x40 == 0x40:
        gpio.output(D6, 1)
    if ch & 0x80 == 0x80:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)

    # Low bits
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
    if ch & 0x01 == 0x01:
        gpio.output(D4, 1)
    if ch & 0x02 == 0x02:
        gpio.output(D5, 1)
    if ch & 0x04 == 0x04:
        gpio.output(D6, 1)
    if ch & 0x08 == 0x08:
        gpio.output(D7, 1)
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)


def lcdprint(Str):
    l = 0;
    l = len(Str)
    for i in range(l):
        lcdwrite(ord(Str[i]))


begin()
lcdcmd(0x01)
lcdprint("Visitor Monitoring")
lcdcmd(0xc0)
lcdprint("    Using RPI     ")
time.sleep(3)
lcdcmd(0x01)
lcdprint("Circuit Digest")
lcdcmd(0xc0)
lcdprint("Saddam Khan")
time.sleep(3)
lcdcmd(0x01)
camera = picamera.PiCamera()
camera.rotation = 180
camera.awb_mode = 'auto'
camera.brightness = 55
lcdcmd(0x01)
lcdprint(" Please Press ")
lcdcmd(0xc0)
lcdprint("    Button      ")
time.sleep(2)
while 1:

    d = time.strftime("%d %b %Y")
    t = time.strftime("%H:%M:%S")
    lcdcmd(0x80)
    lcdprint("Time: %s" % t)
    lcdcmd(0xc0)
    lcdprint("Date:%s" % d)
    gpio.output(led, 1)
    if gpio.input(button) == 0:
        gpio.output(buz, 1)
        gpio.output(led, 0)
        time.sleep(0.5)
        gpio.output(buz, 0)
        capture_image()
        gate()
    time.sleep(0.5)