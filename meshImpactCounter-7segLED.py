import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# segments =(A, B,  C,  D,  E,  F,  G,  DP)
segments =  (5, 6,  13, 19, 26, 21, 20, 16) 
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# digits (1,    2,  3,  4)
digits = (4,    17, 27, 22)
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}

btnUp = 18
btnDown = 25
btnLeft = 23
btnRight = 24
btnHit = 12

GPIO.setup(btnUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnHit, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

btnPause =0.25
ledPause =0.0025
limit = 9999

meshimpacts = open("meshimpacts.txt","r")
n = int(meshimpacts.read())
meshimpacts.closed
print("Previous hit of "+str(n)+" restored")

try:
    while True:            
        if GPIO.input(btnLeft):
            #print("add/minus 10")
            if GPIO.input(btnRight):
                #print("add/minus 1000")
                if GPIO.input(btnUp):
                    n=n+1000
                    print("Count plus 1000, mesh hit is now "+str(n))
                    time.sleep(btnPause)
                if GPIO.input(btnDown):
                    n=n-1000
                    print("Count minus 1000, mesh hit is now "+str(n))
                    time.sleep(btnPause) 
            elif GPIO.input(btnUp): #print("add/minus 100")
                n=n+10
                print("Count plus 10, mesh hit is now "+str(n))
                time.sleep(btnPause)
            elif GPIO.input(btnDown):
                n=n-10
                print("Count minus 10, mesh hit is now "+str(n))
                time.sleep(btnPause)
        elif GPIO.input(btnRight):
            #print("add/minus 100")
            if GPIO.input(btnUp):
                n=n+100
                print("Count plus 100, mesh hit is now "+str(n))
                time.sleep(btnPause)
            if GPIO.input(btnDown):
                n=n-100
                print("Count minus 100, mesh hit is now "+str(n))
                time.sleep(btnPause)
        if GPIO.input(btnHit):
            n=n+1
            print("Mesh hit! "+str(n)+" times")
            meshimpacts = open("meshimpacts.txt","w")
            meshimpacts.write(str(n+1))
            meshimpacts.closed
            time.sleep(btnPause)
        if GPIO.input(btnUp):
            n=n+1
            print("Count plus 1, mesh hit is now "+str(n))
            time.sleep(btnPause)
        if GPIO.input(btnDown):
            n=n-1
            print("Count plus 1, mesh hit is now "+str(n))
            time.sleep(btnPause)
        if n <= -1 :
            print("Count below 0, min kept at 0 hit")
            n = 0
        if n >= limit:
            print("Count above limit, resets back to 0 hit")
            n = 0
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
            GPIO.output(digits[digit], 0)
            time.sleep(ledPause)
            GPIO.output(digits[digit], 1)
except KeyboardInterrupt:
    print("DONE!")
    GPIO.cleanup()
