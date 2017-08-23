from abc import ABCMeta, abstractmethod

from PIL import Image


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


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class FrameChangeObservable(Observable, object):
    pass


class FrameChangeObserver(Observer):
    def __init__(self):
        self.callback = None

    def notify(self, *args, **kwargs):
        print 'received event:', args[0]

        image_stream = kwargs['image_stream']

        image_stream.seek(0)

        image = Image.open(image_stream)

        image.verify()

        print 'Image verified. Size:', image.size

        print 'Foo: ', self.callback()


observable = FrameChangeObservable()

nm = 'andy'


def callback():
    return nm + ' was here'


observer = FrameChangeObserver()

observer.callback = callback

observable.register_observer(observer)

image_stream = open('/Users/andrhahn/1.jpg', 'rb')

observable.notify_observers('New image to process', image_stream=image_stream)
