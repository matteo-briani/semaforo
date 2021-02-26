# Semaforo
A remote controlled traffic light
## Some details

A "semaforo" (traffic-light) is attached to an ESP8266 running Micropython.
It connects to the local wifi and provides a web interface to interact with its lights.
Uses Micropython and TinyWeb library for Micropython. ```https://github.com/belyalov/tinyweb```

If it cannot connect to the network, it becomes an access point and provides a web pages to interact with the lights and/or set a new network.

Lights are accessible by REST, so no web interface is strictly needed.

Send a PUT request to port 80, endpoint ```/semaforo/``` with query parameters ```red```,```yellow``` and ```green``` each set on status ```on```,```off``` or ```blink```

Example PUT request is:
```
192.168.1.71:80/semaforo/?red=on&yellow=blink&green=off
```

you will get a response:

```
{
    "message": "status updated",
    "status": {
        "yellow": "blink",
        "green": "off",
        "red": "on"
    }
}
```

A GET request to the same endpoint ```/semaforo/``` will result in:

```
{
    "yellow": "blink",
    "green": "off",
    "red": "on"
}
```
## How to set it up in a very short an cryptic way

- Burn the firmware (the one from Tinyweb github page and also copied here) using esptool (use ```pipenv install esptool``` and give user the right permission to the interface)
- Upload all the content of ```src``` file using ampy ( again ```pipenv install ampy```). OR setup webREPL and upload from there
- Done
## TODO

A lot... first of all, change the query parameters to a JSON payload... well, it's a proof of concept.
