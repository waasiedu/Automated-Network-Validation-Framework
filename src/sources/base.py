from abc import ABC, abstractmethod


class SourceOfTruth(ABC):
    @abstractmethod
    def get_sites(self):
        pass

    @abstractmethod
    def get_devices(self):
        pass

    