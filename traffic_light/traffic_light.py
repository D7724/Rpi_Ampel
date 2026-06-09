from machine import Pin
from utime import sleep

class Red:
    def change(self, traffic_light):
        traffic_light.zustand = Yellow()

    def show(self, traffic_light):
        traffic_light.red.on()


class Green:
    def change(self, traffic_light):
        traffic_light.green.off()
        traffic_light.zustand = Yellow()

    def show(self, traffic_light):
        traffic_light.green.on()


class Yellow:
    def change(self, traffic_light):
        traffic_light.yellow.off()
        traffic_light.red.off()
        if isinstance(traffic_light.previous_state, Red):
            traffic_light.zustand = Green()
        else:
            traffic_light.zustand = Red()

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
        self.zustand = Red()

    def change(self):
        if not isinstance(self.zustand, Yellow):
            self.previous_state = self.zustand
        self.zustand.change(self)
        self.zustand.show(self)


def main():
    traffic_light1 = TrafficLight(6, 7, 8, Pin)
    traffic_light2 = TrafficLight(18,19,20, Pin)
    traffic_light1.change()
    while True:
        traffic_light1.change()
        traffic_light2.change()
        sleep(1)

main()