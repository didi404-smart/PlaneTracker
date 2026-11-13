from src.base_api import BaseAPI

class NominatimAPI(BaseAPI):
    """Класс для работы с API nominatim"""
    def __init__(self) -> None:
        super().__init__("https://nominatim.openstreetmap.org/search", {'User-Agent': 'test-api/1.0'})

    def get_data(self, query: str) -> list:
        """Возвращает координаты [south, north, west, east]"""
        data = self.request({"country": query, "format": "json", "limit": 1})
        if not data:
            raise ValueError(f'Страна {query} не найдена')
        return data[0]["boundingbox"]

