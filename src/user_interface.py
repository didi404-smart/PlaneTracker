from src.aeroplane import Aeroplane
from src.api import APIAdapter
from src.base_storage import BaseStorage
from requests import RequestException

def parse_aeroplanes(states: list | None) -> list[Aeroplane]:
    """Превращет записи с OpenSky в объекты Aeroplane"""
    planes = []
    for state in states:
        try:
            planes.append(Aeroplane.plane_from_opensky(state))
        except (ValueError, TypeError):
            continue
    return planes

def get_top_altitude(planes: list[Aeroplane], n: int) -> list[Aeroplane]:
    """Возвращает топ n самолетов"""
    return sorted(planes, key=lambda p: p.altitude, reverse=True)[:n]

def filter_country(planes: list, country: str) -> list[Aeroplane]:
    """Оставляет самолеты по указанной стране"""
    country = country.strip().casefold()
    return [p for p in planes if p.origin_country.casefold() == country]

def ask_number(prompt: str) -> int:
    """Спрашивает число у пользователя"""
    while True:
        ans = input(prompt).strip()
        if ans.isdigit() and int(ans) > 0:
            return int(ans)
        print("Введите целое положительное число")

def print_aeroplanes(planes: list[Aeroplane]) -> None:
    """Выводит список самолетов"""
    if not planes:
        print("Ничего не найдено")
        return
    for num, plane in enumerate(planes, start=1):
        print(f'{num}. {plane}\n')

def load_planes(adapter: APIAdapter, storage: BaseStorage) -> list[Aeroplane] | None:
    """Запрашивает страну, получает самолёты и сохраняет их в хранилище"""
    country = input("Введите название страны: ").strip()
    if not country:
        print("Название страны не может быть пустым")
        return None
    try:
        adapter.get_aeroplanes(country)
    except (RequestException, ValueError) as e:
        print(f"Не удалось полчить данные: {e}")
        return None
    planes = parse_aeroplanes(adapter.aeroplanes.get('states'))
    storage.add_aeroplanes(planes)
    print(f"найдено самолётов: {len(planes)}. Успешно сохранены в файл.")
    return planes