class Observable(object):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.on_change(*args, **kwargs)


class A(Observable, object):
    def on_change(self, *args):
        print 'on change A:', args


class B(Observable, object):
    def on_change(self, *args):
        print 'on change B:', args


a = A()
b = B()

a.register_observer(b)
# b.register_observer(a.on_change)

a.notify_observers('Hello')
# b.notify_observers('World')
