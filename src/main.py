import tinyweb
import uasyncio
from lights import colors, lights, alert
from utils import read_credentials, write_credentials, connect_to_wifi
import network

status = {
            'red':'off',
            'yellow': 'off',
            'green': 'off' 
         }

async def blink_controller():
    while True:
        for color in colors:
            if status[color] == 'blink':
                lights[color].off()
        await uasyncio.sleep(0.5)
        for color in colors:
            if status[color] == 'blink':
                lights[color].on()
        await uasyncio.sleep(0.5)

class Wifi():

    def get(self, data):

        sta_if = network.WLAN(network.STA_IF)
        ssid, _ = read_credentials()

        return {'ssid': ssid,
                'status': 'connected' if sta_if.isconnected() else 'not connected'}
    
    def put(self, data):

        ssid = data.get('ssid', None)
        password = data.get('password', None)

        if (not ssid) or (not password):
            return {''}

        try:
            connect_to_wifi(force_reconnection=True, ssid = ssid, password = password)
            if network.WLAN(network.STA_IF).isconnected():
                write_credentials(ssid = ssid, password = password)
                alert('green')
        except Exception:
            alert('red')
            alert('yellow')
            connect_to_wifi(force_reconnection=True)
        
        return {''}

class Semaforo():

    def update_lights(self):
        for color in colors:
            if status[color] == 'on':
               lights[color].off()
            if status[color] == 'off':
               lights[color].on()
            if status[color] == 'blink':
                # Already managed by blink_controller
                pass
        return 

    def status_parser(self, data):
        for color in colors:
            color_status = data.get(color, None)
            if color_status in ['on', 'off', 'blink']:
                status[color] = color_status
            else:
                raise ValueError
        return 

    def get(self, data):
        return status

    def put(self, data):
        data.get('status', None)
        if not data:
            return {'message': 'Error, no status pass',
                    'status': status}

        try:
            self.status_parser(data)
        except Exception:
            return {'message': 'wrong status',
                    'status': status}
        self.update_lights()
        return {'message': 'status updated',
                'status': status}

app = tinyweb.webserver()

# Index page
@app.route('/')
@app.route('/index.html')
async def index(req, resp):
    # Just send file
    await resp.send_file('index.html')

@app.route('/settings.html')
async def settings(req, resp):
    # Just send file
    await resp.send_file('settings.html')

app.add_resource(Semaforo, '/semaforo/')
app.add_resource(Wifi, '/wifi/')
app.run(host='0.0.0.0', port=80, loop_forever=False)
loop = uasyncio.get_event_loop() 
loop.create_task(blink_controller())
loop.run_forever()

