from abc import ABC, abstractmethod
import datetime

class EntityInterface(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_balance(self):
        pass
    
    @abstractmethod
    def get_transactions(self, time: datetime.datetime):
        pass