"""
Base class implementing observer pattern.
"""

class Observable:

    def __init__(self):
        self.signals = {}

    def register_signal(self, signal_name):
        if not self.signals.has_key(signal_name):
            self.signals[signal_name] = []

    def add_observer(self, signal_name, observer):
        if not self.signals.has_key(signal_name):
            raise NoSuchSignalException
        signal_observers = self.signals[signal_name]
        if signal_observers.count(observer) == 0:
            self.signals[signal_name].append(observer)

    def emit_signal(self, signal_name):
        observers = self.signals[signal_name]
        for observer in observers:
            observer.notify(self)

class NoSuchSignalException(Exception):
    pass
