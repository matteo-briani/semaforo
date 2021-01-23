import machine
from time import sleep

red     = machine.Pin(4 , machine.Pin.OUT)
yellow  = machine.Pin(16, machine.Pin.OUT)
green   = machine.Pin(5 , machine.Pin.OUT)

colors = ['red','yellow','green']

lights = {
            'red': red,
            'yellow': yellow,
            'green': green 
         }

for light in lights.values():
    light.on()

def test_lights():
    for color in colors:
        lights[color].off()
        sleep(0.2)
    for color in colors:
        lights[color].on()
        sleep(0.2)

def alert(color):
    
    if color in colors:
        light = lights[color]
        for _ in range(2):
            light.off()
            sleep(0.2)
            light.on()
            sleep(0.2)