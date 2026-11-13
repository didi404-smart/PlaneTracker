class Aeroplane:
    """Класс для работы с самолетом"""

    icao24: str
    callsign: str | None
    origin_country: str
    speed: float |None
    altitude: float | None
    on_ground: bool

    def __init__(self, icao24, callsign, origin_country, speed, altitude, on_ground = False):
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.speed = speed
        self.on_ground = on_ground

    @staticmethod
    def check_number(value, name: str) -> float:
        """Проверяет, что value число"""
        if value is None:
            return 0.0
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} должно быть числом")
        return float(value)

    @staticmethod
    def check_text(value, name: str) -> str:
        """Проверяет, что значение строка (не пустая)"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} должно быть не пустой строкой")
        return value.strip()
