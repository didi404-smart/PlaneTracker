class Aeroplane:
    """Класс для работы с самолетом"""

    __icao24: str  # уникальный идентификатор борта
    __callsign: str | None  # позывной рейса
    __origin_country: str  # Страна регистрации
    __speed: float | None  # скорость
    __altitude: float | None  # высота
    __on_ground: bool  # состояние самолета(воздух/земля)

    def __init__(self, icao24, callsign, origin_country, speed, altitude, on_ground=False):
        self.__icao24 = icao24
        self.__callsign = callsign
        self.__origin_country = origin_country
        self.__speed = speed
        self.__on_ground = on_ground

    def __str__(self) -> str:
        return (
            f"{self.callsign} ({self.icao24}), {self.origin_country}, "
            f"скорость {self.speed} м/с, высота {self.altitude} м"
        )

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
        if isinstance(value, bool) or not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} должно быть не пустой строкой")
        return value.strip()

    @staticmethod
    def check_other(other) -> None:
        """Проверяет, что other является классом Aeroplane"""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно толтко с другим Aeroplane")

    def compare_speed(self, other) -> int:
        """True, если этот самолёт летит быстрее другого"""
        self.check_other(other)
        return self.speed > other.speed

    def compare_height(self, other):
        """True, если этот самолёт летит выше другого"""
        self.check_other(other)
        return self.altitude > other.altitude

    @property
    def icao24(self):
        return self.__icao24

    @icao24.setter
    def icao24(self, value: str):
        self.__icao24 = self.check_text(value, "icao24").lower()

    @property
    def callsign(self):
        return self.__callsign

    @callsign.setter
    def callsign(self, value: str | None):
        if value is None or (isinstance(value, str) and not value.strip()):
            self.__callsign = "Не указан"
        else:
            self.__callsign = self.check_text(value, "callsign")

    @property
    def origin_country(self):
        return self.__origin_country

    @origin_country.setter
    def origin_country(self, value: str):
        self.__origin_country = self.check_text(value, "origin_country")

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value: float | None):
        num = self.check_number(value, "speed")
        if num < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self.__speed = num

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self, value: float | None):
        self.check_number(value, "altitude")

    @property
    def on_ground(self):
        return self.__on_ground

    @on_ground.setter
    def on_ground(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("on_ground должно быть True или False")
        self.__on_ground = value
