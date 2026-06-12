class EventType:
    PEDESTRIAN = 1
    CAR = 2


class EventListener:
    def update(self, event_type):
        pass


class EventManager:
    def __init__(self):
        self.last_event_type = EventType.CAR
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners:
            if listener in self.listeners[event_type]:
                self.listeners[event_type].remove(listener)

    def notify(self, event_type):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener.update(event_type)
