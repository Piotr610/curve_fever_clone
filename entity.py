from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self):
        self.__color = None
        self.__track = None
        super().__init__()

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_track(self, track):
        pass
