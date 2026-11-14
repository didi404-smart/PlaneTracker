from src.aeroplane import Aeroplane



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