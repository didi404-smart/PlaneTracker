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

MENU = (
    '\n1. Запросить самолёты над страной\n'
    '2. Топ N самолётов по высоте\n'
    '3. Самолёты по стране регистрации\n'
    '0. Выход\n'
)

def menu(adapter: APIAdapter, storage: BaseStorage) -> None:
    """Главное меню"""
    planes = []
    print(MENU)
    while True:
        choice = input("Введите номер выбранного пункта: ").strip()

        if choice == "1":
            res = load_planes(adapter, storage)
            if res is not None:
                planes = res
        elif choice in ("2", "3"):
            if not planes:
                print("Сначала запросить самолёты над страной (пункт 1)")
            elif choice == "2":
                n = ask_number("Сколько самолётов показать? Введите число: ")
                print_aeroplanes(get_top_altitude(planes, n))
            else:
                country = input("Введите страну регистации: ")
                print_aeroplanes(filter_country(planes, country))
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Такого пункта нет. Пожалуйтса, выберите 1, 2, 3 или 0")
