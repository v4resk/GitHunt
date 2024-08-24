from abc import ABC, abstractmethod

class Auditor(ABC):
    def __init__(self):
        pass

    """Return YES if valide"""
    @abstractmethod
    def is_valide(self):
         pass
