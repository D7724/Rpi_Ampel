import machine

for pin_number in range(29):
    try:
        pin = machine.Pin(pin_number, machine.Pin.OUT)
        pin.value(0)
    except Exception as e:
        pass
