from observer.event_manager import EventManager, EventListener, EventType
from time import sleep

CYCLE_STEPS = 2
CHANGE_INTERVAL_SEC = 1


class Red:
    def change(self, traffic_light):
        traffic_light.current_state = Yellow()

    def show(self, traffic_light):
        traffic_light.red.on()


class Green:
    def change(self, traffic_light):
        traffic_light.green.off()
        traffic_light.current_state = Yellow()

    def show(self, traffic_light):
        traffic_light.green.on()


class Yellow:
    def change(self, traffic_light):
        traffic_light.yellow.off()
        traffic_light.red.off()
        if isinstance(traffic_light.previous_state, Red):
            traffic_light.current_state = Green()
        else:
            traffic_light.current_state = Red()

    def show(self, traffic_light):
        traffic_light.yellow.on()

class TrafficLight(EventListener):
    def __init__(self, red_pin, yellow_pin, green_pin, pin, initial_state):
        self.red = pin(red_pin, pin.OUT) 
        self.yellow = pin(yellow_pin, pin.OUT) 
        self.green = pin(green_pin, pin.OUT) 
        self.red.off()
        self.yellow.off()
        self.green.off()
        self.current_state = initial_state
        initial_state.show(self)
        self.previous_state = None

    def change(self):
        if not isinstance(self.current_state, Yellow):
            self.previous_state = self.current_state
        self.current_state.change(self)
        self.current_state.show(self)

    def update(self, event_type):
        for _ in range(CYCLE_STEPS):
            self.change()
            sleep(CHANGE_INTERVAL_SEC)
