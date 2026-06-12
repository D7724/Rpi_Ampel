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
# ==========================================
# Configuration
# ==========================================
SSID = "Rpi_Ampel"
PASSWORD = "12345678"
ROUTES = {
    "GET /auto ": (EventType.CAR, "🚗 Auto hat geklickt!"),
    "GET /fussgaenger ": (EventType.PEDESTRIAN, "🚶 Fußgänger hat geklickt!"),
}

# ==========================================
# Hardware
# ==========================================
led = machine.Pin("LED", machine.Pin.OUT)

# ==========================================
# HTML Page
# ==========================================
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


# ==========================================
# Access Point Setup
# ==========================================
def start_access_point():
    ap = network.WLAN(network.AP_IF)

    ap.config(
        essid=SSID,
        password=PASSWORD
    )

    ap.active(True)

    print("Starting Access Point...")

    while not ap.active():
        time.sleep(0.1)

    print("Access Point ready")
    print("IP configuration:", ap.ifconfig())

    return ap


# ==========================================
# HTTP Response
# ==========================================
def send_html(client):
    client.send(
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    client.send(HTML)


# ==========================================
# Request Handler
# ==========================================
def handle_request(request, event_manager):
    first_line = request.split("\r\n")[0]

    for route, (event_type, message) in ROUTES.items():
        if route in first_line:
            print(message)
            if event_manager.lastEventType != event_type:
                event_manager.notify(event_manager.lastEventType)  # currently green → red, first
                event_manager.notify(event_type)                   # the other one → green, second
                event_manager.lastEventType = event_type
            return

    print("Unknown request:", first_line)


# ==========================================
# Main
# ==========================================
ap = start_access_point()

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(5)

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

    except Exception as e:
        print("Error:", e)

    finally:
        if client:
            client.close()

        led.off()
