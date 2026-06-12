import sys
from unittest.mock import MagicMock

sys.modules['machine'] = MagicMock()
sys.modules['utime'] = MagicMock()

from traffic_light import TrafficLight, Red, Yellow, Green

class MockPin:
    OUT = 1

    def __init__(self, pin_number, mode):
        self.pin_number = pin_number
        self.mode = mode
        self.state = False

    def on(self):
        self.state = True

    def off(self):
        self.state = False


def test_initial_state():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    #assert
    assert isinstance(testee.current_state, Red)

def test_previous_state():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    #assert
    assert isinstance(testee.previous_state, Red)

def test_state_yellow():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    #assert
    assert isinstance(testee.current_state, Yellow)

def test_state_green():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    testee.change()
    #assert
    assert isinstance(testee.current_state, Green)

def test_show_red_and_yellow():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    #assert
    print(testee.red.state)
    print(testee.yellow.state)
    assert testee.red.state == True
    assert testee.yellow.state == True
    assert testee.green.state == False

def test_show_green():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    testee.change()
    #assert
    assert testee.green.state == True
    assert testee.red.state == False
    assert testee.yellow.state == False

def test_show_only_yellow():
    #arrange
    testee = TrafficLight(6, 7, 8, MockPin, Red())
    #act
    testee.change()
    testee.change()
    testee.change()
    #assert
    assert testee.red.state == False
    assert testee.green.state == False
    assert testee.yellow.state == True