from abc import ABC, abstractmethod
from requests import get

class BaseAPI(ABC):
    """Абстрактный класс для классов с работой api(Nominatim и OpenSky)"""


    def __init__(self, url: str, headers: dict | None = None) -> None:
        self.url = url
        self.headers = headers or {}

    def request(self, params: dict):
        res = get(url=self.url, params=params, headers=self.headers)
        res.raise_for_status()
        return res.json()

    @abstractmethod
    def get_data(self, query):
        """Получение данных по запросу"""
