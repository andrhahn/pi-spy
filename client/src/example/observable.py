class Observable(object):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(*args, **kwargs)
