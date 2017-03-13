#!/usr/bin/env python

import usb.core
import usb.util
import time

USB_VENDOR  = 0x045e # Microsoft
USB_PRODUCT = 0x0800 # Wireless Keyboard

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_LEFT  = 80
BTN_RIGHT = 79
BTN_DOWN  = 81
BTN_UP    = 82
BTN_SPACE  = 44 # Space
BTN_ESC  = 41 # ESC

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

meshimpacts = open("meshimpacts.txt","r")
#count=1
count = int(meshimpacts.read())
meshimpacts.closed
print(count)

limit = 9999

while True:
    control = None
    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        #print(control)
        if count <= -1 :
            print("Count below 0, min kept at 0 hit")
            count = 0
        if count >= limit:
            print("Count above limit, resets back to 0 hit")
            count = 0
    except:
        pass

    if control != None:
        if BTN_LEFT in control:
            print("add/minus 10")
            if BTN_RIGHT in control:
                print("add/minus 1000")
                if BTN_UP in control:             
                    count = count + 1000
                    print("add 1000 - mesh hit is now "+str(count))
                if BTN_DOWN in control:
                    count = count - 1000
                    print("minus 1000 - mesh hit is now "+str(count))       
            elif BTN_UP in control:                
                count = count + 10
                print("add 10 - mesh hit is now "+str(count))
            elif BTN_DOWN in control:
                count = count - 10
                print("minus 10 - mesh hit is now "+str(count))
        elif BTN_RIGHT in control:
            print("add/minus 100")
            if BTN_UP in control:             
                count = count + 100
                print("add 100 - mesh hit is now "+str(count))
            if BTN_DOWN in control:
                count = count - 100
                print("minus 100 - mesh hit is now "+str(count))
        elif BTN_ESC in control:
            meshimpacts = open("meshimpacts.txt","w")
            meshimpacts.write(str(count))
            meshimpacts.closed
            exit()
        elif BTN_SPACE in control:
            count = count + 1
            print("Mesh hit!!!: "+str(count)+" times")
        elif BTN_DOWN in control:
            count = count - 1
            print("minus 1 - mesh hit is now "+str(count))
        elif BTN_UP in control:
            count = count +1
            print("add 1 - mesh hit is now "+str(count))

time.sleep(0.02)
