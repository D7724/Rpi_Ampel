from machine import Pin
from utime import sleep

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


class TrafficLight:
    def __init__(self, red_pin, yellow_pin, green_pin, pin):
        self.red = pin(red_pin, pin.OUT) 
        self.yellow = pin(yellow_pin, pin.OUT) 
        self.green = pin(green_pin, pin.OUT) 
        self.red.off()
        self.yellow.off()
        self.green.off()
        self.current_state = Red()
        self.current_state.show(self)
        self.previous_state = None

    def change(self):
        if not isinstance(self.current_state, Yellow):
            self.previous_state = self.current_state
        self.current_state.change(self)
        self.current_state.show(self)


def main():
    traffic_light1 = TrafficLight(6, 7, 8, Pin)
    traffic_light2 = TrafficLight(18,19,20, Pin)
    traffic_light1.change()
    while True:
        traffic_light1.change()
        traffic_light2.change()
        sleep(1)

if __name__ == "__main__":
    main()