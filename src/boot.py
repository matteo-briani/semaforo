# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import esp
esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()


from lights import alert, test_lights
from utils import connect_to_wifi, activate_ap

test_lights()
try:
    connect_to_wifi()
    alert('green')
except Exception:
    alert('red')
    activate_ap()

