import network
import time

def read_credentials():
    with open('credentials', 'rb') as f:
        credentials = f.readlines()
    return credentials[0].rstrip(), credentials[1].rstrip()

def write_credentials(ssid, password):
    with open('credentials', 'wb') as f:
        f.write(''.join([ssid, '\n']))
        f.write(password)

def connect_to_wifi(force_reconnection=False, ssid=None, password=None):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.config(dhcp_hostname="semaforo")

    if force_reconnection:
        sta_if.disconnect()
        sta_if.active(False)

    sta_if.active(True)

    if (ssid is None) or (password is None):
        # Get credentials from file
        ssid, password = read_credentials()
    sta_if.connect(ssid, password)
    begin_connection_t = time.time()
    while not sta_if.isconnected():
        if (time.time() - begin_connection_t) > 10:
            raise Exception

    return

def activate_ap():

    # Set AP
    ssid = 'Semaforo'
    password = '$emaforo'
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
        pass
    # print('network config:', sta_if.ifconfig())