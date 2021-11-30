from abc import ABC, abstractmethod


class SuperServices(ABC):

    @abstractmethod
    def lookup(self):
        pass

    @abstractmethod
    def format_document(self):
        pass

    @abstractmethod
    def find_by(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def find_all(self):
        pass
