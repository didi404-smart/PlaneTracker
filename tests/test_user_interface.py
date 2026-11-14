import pytest
from requests import RequestException

from src.user_interface import filter_country, get_top_altitude, load_planes, menu, parse_aeroplanes


class FakeAdapter:
    """Подделка APIAdapter"""

    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error
        self.aeroplanes = None

    def get_aeroplanes(self, country):
        if self.error:
            raise self.error
        self.aeroplanes = self.data


class FakeStorage:
    """Подделка хранилища"""

    def __init__(self):
        self.saved = []

    def add_aeroplanes(self, planes):
        self.saved.extend(planes)


def set_inputs(monkeypatch, answers):
    """Подставляет 'ответы пользователя' на вызовы input() по очереди."""
    iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(iterator))


def make_state(icao, callsign, country, altitude, speed=200.0):
    return [icao, callsign, country, 0, 0, 0.0, 0.0, altitude, False, speed, 0, 0, None, None, None, False, 0]


STATES = [
    make_state("a1", "LOW", "Canada", 1000.0),
    make_state("b2", "HIGH", "Russia", 11000.0),
    make_state("c3", "MID", "Canada", 5000.0),
]


def test_parse_valid_and_broken():
    planes = parse_aeroplanes(STATES + [["short"], make_state("d4", "X", "", 1)])
    assert len(planes) == 3


def test_top_altitude_order():
    top = get_top_altitude(parse_aeroplanes(STATES), 2)
    assert [p.callsign for p in top] == ["HIGH", "MID"]


def test_top_n_bigger():
    assert len(get_top_altitude(parse_aeroplanes(STATES), 10)) == 3


def test_filter_country_ignores_case_and_spaces():
    assert len(filter_country(parse_aeroplanes(STATES), "  canada ")) == 2


def test_filter_country_nothing_found():
    assert filter_country(parse_aeroplanes(STATES), "Peru") == []


def test_load_planes_success(monkeypatch):
    set_inputs(monkeypatch, ["Canada"])
    storage = FakeStorage()
    planes = load_planes(FakeAdapter({"states": STATES}), storage)
    assert len(planes) == 3
    assert len(storage.saved) == 3


def test_load_planes_no_aeroplanes(monkeypatch):
    set_inputs(monkeypatch, ["Canada"])
    assert load_planes(FakeAdapter({"states": None}), FakeStorage()) == []


def test_load_planes_empty_country(monkeypatch, capsys):
    set_inputs(monkeypatch, ["   "])
    assert load_planes(FakeAdapter(), FakeStorage()) is None
    assert "не может быть пустым" in capsys.readouterr().out


@pytest.mark.parametrize("error", [ValueError("нет страны"), RequestException("сеть")])
def test_load_planes_api_errors(monkeypatch, capsys, error):
    set_inputs(monkeypatch, ["Canada"])
    assert load_planes(FakeAdapter(error=error), FakeStorage()) is None
    assert "Не удалось получить данные" in capsys.readouterr().out


def test_menu_exit(monkeypatch, capsys):
    set_inputs(monkeypatch, ["0"])
    menu(FakeAdapter(), FakeStorage())
    assert "До свидания" in capsys.readouterr().out


def test_menu_unknown_item(monkeypatch, capsys):
    set_inputs(monkeypatch, ["9", "0"])
    menu(FakeAdapter(), FakeStorage())
    assert "Такого пункта нет" in capsys.readouterr().out


def test_menu_top_before_loading(monkeypatch, capsys):
    set_inputs(monkeypatch, ["2", "0"])
    menu(FakeAdapter(), FakeStorage())
    assert "Сначала запросите" in capsys.readouterr().out


def test_menu_full_scenario(monkeypatch, capsys):
    set_inputs(
        monkeypatch,
        [
            "1",
            "Canada",
            "2",
            "abc",
            "1",
            "3",
            "russia",
            "0",
        ],
    )
    menu(FakeAdapter({"states": STATES}), FakeStorage())
    out = capsys.readouterr().out
    assert "Введите целое положительное число" in out
    assert "1. HIGH" in out
    assert out.count("HIGH") == 2


def test_menu_nothing_found(monkeypatch, capsys):
    set_inputs(monkeypatch, ["1", "Canada", "3", "Peru", "0"])
    menu(FakeAdapter({"states": STATES}), FakeStorage())
    assert "Ничего не найдено" in capsys.readouterr().out
