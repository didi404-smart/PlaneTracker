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

class OpenSkyAPI(BaseAPI):
    """Класс для работы с api OpenSky"""

    def __init__(self):
        super().__init__("https://opensky-network.org/api/states/all")

    def get_data(self, query: list) -> dict:
        """Возвращает самолеты в области [south, north, west, east]"""
        res = self.request({'lamin': query[0], 'lamax': query[1], 'lomin': query[2], 'lomax': query[3]})
        return res

class APIAdapter:
    """Объединяет оба API"""

    def __init__(self, geo_api: BaseAPI | None = None, aeroplane_api: BaseAPI | None = None):
        self.geo_api = geo_api or NominatimAPI()
        self.aeroplane_api = aeroplane_api or OpenSkyAPI()
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> None:
        """Полчаем самолеты в заданной стране"""
        box = self.geo_api.get_data(country)
        self.aeroplanes = self.aeroplane_api.get_data(box)
