from machine import Pin
from utime import sleep

red1 = Pin(6, Pin.OUT) 
yellow1 = Pin(7, Pin.OUT)
green1 = Pin(8, Pin.OUT)

class Red:
    def wechseln(self, ampel):
        ampel.zustand = Yellow()

    def anzeigen(self):
        red1.on()


class Green:
    def wechseln(self, ampel):
        green1.off()
        ampel.zustand = Yellow()

    def anzeigen(self):
        green1.on()


class Yellow:
    def wechseln(self, ampel):
        yellow1.off()
        red1.off()
        print(ampel.previous_state)
        if isinstance(ampel.previous_state, Red):
            ampel.zustand = Green()
        else:
            ampel.zustand = Red()

    def anzeigen(self):
        yellow1.on()


class TrafficLight:
    def __init__(self):
        red1.off()
        yellow1.off()
        green1.off()
        self.zustand = Red()

    def wechseln(self):
        if not isinstance(self.zustand, Yellow):
            self.previous_state = self.zustand
        self.zustand.wechseln(self)

    def status(self):
        return self.zustand.anzeigen()
    


def main():
    ampel = TrafficLight()
    while True:
        ampel.status()
        sleep(1)
        ampel.wechseln()

main()