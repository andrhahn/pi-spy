from abc import ABCMeta, abstractmethod


class Observer(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.callback = None

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass
