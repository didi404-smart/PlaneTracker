from abc import ABC, abstractmethod
from src.aeroplane import Aeroplane

class BaseStorage(ABC):
    """Абстрактный класс для хранилища самолёта"""

    @abstractmethod
    def connect(self) -> None:
        """Подключение к хранилишу (для БД)"""

    @abstractmethod
    def close(self) -> None:
        """Закрыть соединение (для БД)"""

    @abstractmethod
    def add_aeroplane(self, plane: Aeroplane) -> None:
        """Добавить самолёт в хранилище"""

    @abstractmethod
    def get_aeroplane(self, **criteria) -> int:
        """Удалить самолёты по критерию, вернуть количество удаленных"""

