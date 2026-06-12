import socket
import network
import time
import machine
from observer.event_manager import EventManager, EventType
from traffic_light.traffic_light import Green, Red, TrafficLight

manager = EventManager()
traffic_light1 = TrafficLight(6, 7, 8, machine.Pin, Green())
traffic_light2 = TrafficLight(18, 19, 20, machine.Pin, Red())
manager.subscribe(EventType.CAR, traffic_light1)
manager.subscribe(EventType.PEDESTRIAN, traffic_light2)

SSID = "Rpi_Ampel"
PASSWORD = "12345678"
ROUTES = {
    "GET /auto ": (EventType.CAR, "🚗 Auto hat geklickt!"),
    "GET /fussgaenger ": (EventType.PEDESTRIAN, "🚶 Fußgänger hat geklickt!"),
}

PEDESTRIAN_MAX_GREEN_SECONDS = 15
LOOP_TIMEOUT_SECONDS = 1

led = machine.Pin("LED", machine.Pin.OUT)
last_pedestrian_green_time = None

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Pico W Ampelsteuerung</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 50px;
    background-color: #f4f4f4;
}
h1 { color: #333; }

.btn {
    padding: 20px 40px;
    font-size: 20px;
    margin: 10px;
    cursor: pointer;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

.btn-auto {
    background-color: #3498db;
    color: white;
}

.btn-ped {
    background-color: #2ecc71;
    color: white;
}
</style>
</head>

<body>
<h1>Ampelsteuerung</h1>
<p>Wähle aus, wer die Ampel anfordert:</p>

<a href="/auto">
    <button class="btn btn-auto">Auto</button>
</a>

<a href="/fussgaenger">
    <button class="btn btn-ped">Fussgänger</button>
</a>

</body>
</html>
"""


def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)
    print("Starting Access Point...")
    while not ap.active():
        time.sleep(0.1)
    print("Access Point ready")
    print("IP configuration:", ap.ifconfig())
    return ap


def send_html(client):
    client.send(
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    client.send(HTML)


def switch_traffic_to(event_type, event_manager):
    global last_pedestrian_green_time
    
    if event_manager.last_event_type == event_type:
        return
    
    event_manager.notify(event_manager.last_event_type)
    event_manager.notify(event_type)
    event_manager.last_event_type = event_type
    
    if event_type == EventType.PEDESTRIAN:
        last_pedestrian_green_time = time.time()
    else:
        last_pedestrian_green_time = None


def handle_request(request, event_manager):
    first_line = request.split("\r\n")[0]
    
    for route, (event_type, message) in ROUTES.items():
        if route in first_line:
            print(message)
            switch_traffic_to(event_type, event_manager)
            return


def check_pedestrian_timeout(event_manager):
    global last_pedestrian_green_time
    
    if (
        event_manager.last_event_type == EventType.PEDESTRIAN
        and last_pedestrian_green_time is not None
        and (time.time() - last_pedestrian_green_time) >= PEDESTRIAN_MAX_GREEN_SECONDS
    ):
        print("⏱️ Fussgänger-Grünphase abgelaufen, wechsle zu Autos")
        switch_traffic_to(EventType.CAR, event_manager)

ap = start_access_point()
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(5)
server.settimeout(LOOP_TIMEOUT_SECONDS)

print("Listening on", addr)

while True:
    client = None
    try:
        client, client_addr = server.accept()
        client.settimeout(5)
        print("Client connected:", client_addr)
        led.on()
        request = client.recv(1024).decode("utf-8")
        handle_request(request, manager)
        send_html(client)
    except OSError:
        pass
    except Exception as e:
        print("Error:", e)
    finally:
        if client:
            client.close()
        led.off()
    
    check_pedestrian_timeout(manager)
