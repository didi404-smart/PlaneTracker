import json
import os

from src.aeroplane import Aeroplane
from src.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """Хранит самолеты в JSON"""

    filepath: str

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def connect(self) -> None:
        pass

    def close(self) -> None:
        pass

    def read(self) -> list[dict]:
        """Читает JSON"""
        try:
            with open(self.filepath, encoding="utf-8") as file:
                content = file.read().strip()
        except FileNotFoundError:
            return []
        else:
            return json.loads(content) if content else []

    def write(self, data: list[dict]) -> None:
        """Записыват в JSON"""
        folder = os.path.dirname(self.filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def matches(data: dict, criteria: dict) -> bool:
        """Проверяет подходит ли запись под все критерии"""
        for key, value in criteria.items():
            k = data.get(key)
            if isinstance(k, str) and isinstance(value, str):
                if k.casefold() != value.casefold():
                    return False
            elif k != value:
                return False
        return True

    def add_aeroplane(self, plane: Aeroplane) -> None:
        self.add_aeroplanes([plane])

    def add_aeroplanes(self, planes: list[Aeroplane]) -> None:
        data = {r["icao24"]: r for r in self.read()}
        for plane in planes:
            data[plane.icao24] = plane.to_dict()
        self.write(list(data.values()))

    def get_aeroplane(self, **criteria) -> list[Aeroplane]:
        self.check_criteria(criteria)
        return [Aeroplane.from_dict(r) for r in self.read() if self.matches(r, criteria)]

    def delete_aeroplane(self, **criteria) -> int:
        self.check_criteria(criteria)
        if not criteria:
            raise ValueError("Необходимо указать хотя бы 1 критерий удаления")
        data = self.read()
        res = [r for r in data if not self.matches(r, criteria)]
        self.write(res)
        return len(data) - len(res)
