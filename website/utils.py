"""Helpers."""


from abc import ABC, abstractmethod


class Subscriber(ABC):
    """Listener"""

    @abstractmethod
    def update(self, context) -> None:
        """
        Update subscribers/listeners

        Args:
            context: context used to update object

        """


class Publisher:
    """Observable object."""

    def __init__(self) -> None:

        self.subscriber_lst = []  # listener_lst
        self.state = None

    def add(self, subscriber: Subscriber) -> None:
        """
        Subscribe. Add a subscriber/listener to the list

        Args:
            subscriber: subscriber/listener to add to the list
        """
        self.subscriber_lst.append(subscriber)

    def remove(self, subscriber: Subscriber) -> None:
        """
        Unsubscribe. Remove a subscriber/listener from the list

        Args:
            subscriber: subscriber/listener to remove from the list
        """
        self.subscriber_lst.remove(subscriber)

    def notify(self, context=None) -> None:
        """Notify all subscribers/listeners

        Args:
            context: context to publish to subscribers/listeners
        """

        for subscriber in self.subscriber_lst:
            subscriber.update(context)

    def func(self) -> None:
        """_summary_"""


# class Observable:
#     def __init__(self):
#         self._observers = []

#     def register_observer(self, observer):
#         self._observers.append(observer)

#     def notify_observers(self, *args, **kwargs):
#         for obs in self._observers:
#             obs.notify(self, *args, **kwargs)


# class Observer:
#     def __init__(self, observable):
#         observable.register_observer(self)

#     def notify(self, observable, *args, **kwargs):
#         print("Got", args, kwargs, "From", observable)


# subject = Observable()
# observer = Observer(subject)
# subject.notify_observers("test", kw="python")

# # prints: Got ('test',) {'kw': 'python'} From <__main__.Observable object at 0x0000019757826FD0>
