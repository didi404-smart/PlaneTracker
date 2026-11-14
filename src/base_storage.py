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
    def get_aeroplane(self, **criteria) -> list[Aeroplane]:
        """Получить список самолетов по критериям"""

    @abstractmethod
    def delete_aeroplane(self, **criteria) -> int:
        """Удалить самолёты по критерию, вернуть количество удаленных"""

    @abstractmethod
    def add_aeroplanes(self, planes: list[Aeroplane]) -> None:
        """Добавляет самолёт в список с самолётами"""

    @staticmethod
    def check_criteria(criteria: dict) -> None:
        """Проверяет, что критерии известные нам поля"""
        for c in criteria:
            if c not in ("icao24", "callsign", "origin_country", "speed", "altitude", "on_ground"):
                raise ValueError(f"Неизвестный критерий {c}")
