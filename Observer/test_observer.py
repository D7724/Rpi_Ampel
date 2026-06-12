from event_manager import EventManager, EventType, EventListener



class SubscriberMock(EventListener):
    def __init__(self, event_type):
        self.event_type = event_type
        self.messages = []

    def update(self, event_type):
        if event_type == self.event_type:
            self.messages.append("Hello Event!")



def test_notifies_subscribers():
    #arrange
    eventType = EventType.CAR
    eventManager = EventManager()
    subscriber = SubscriberMock(eventType)
    #act
    eventManager.subscribe(eventType, subscriber)
    eventManager.notify(eventType)
    #assert
    assert subscriber.messages == ["Hello Event!"]


def test_does_not_notify_unsubscribed():
    #arrange
    eventType = EventType.PEDESTRIAN
    eventManager = EventManager()
    subscriber = SubscriberMock(eventType)
    #act
    eventManager.subscribe(eventType, subscriber)
    eventManager.unsubscribe(eventType, subscriber)
    eventManager.notify(eventType)
    #assert
    assert subscriber.messages == []

def test_notifies_multiple_subscribers():
    #arrange
    eventType = EventType.CAR
    eventManager = EventManager()
    subscriber1 = SubscriberMock(eventType)
    subscriber2 = SubscriberMock(eventType)
    #act
    eventManager.subscribe(eventType, subscriber1)
    eventManager.subscribe(eventType, subscriber2)
    eventManager.notify(eventType)
    #assert
    assert subscriber1.messages == ["Hello Event!"]
    assert subscriber2.messages == ["Hello Event!"]