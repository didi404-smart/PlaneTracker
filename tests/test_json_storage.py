import pytest

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


def test_read_missing_file(tmp_path):
    empty = JSONStorage(str(tmp_path / "none.json"))
    assert empty.get_aeroplane() == []


def test_get_country_ignores_case(storage):
    res = storage.get_aeroplane(origin_country="canada")
    assert {p.icao24 for p in res} == {"b2", "c3"}


def test_get_several_criteria(storage):
    res = storage.get_aeroplane(origin_country="Canada", on_ground=True)
    assert [p.icao24 for p in res] == ["c3"]


def test_unknown_criterion(storage):
    with pytest.raises(ValueError):
        storage.get_aeroplane(color="red")


def test_adding_plane(storage):
    storage.add_aeroplane(Aeroplane("a1", "AFL1", "Russia", 999, 1))
    assert len(storage.get_aeroplane()) == 3
    assert storage.get_aeroplane(icao24="a1")[0].speed == 999.0


def test_delete(storage):
    assert storage.delete_aeroplane(origin_country="Canada") == 2
    assert len(storage.get_aeroplane()) == 1


def test_delete_criteria_is_forbidden(storage):
    with pytest.raises(ValueError):
        storage.delete_aeroplane()
    assert len(storage.get_aeroplane()) == 3


def test_connect_and_close(storage):
    storage.connect()
    storage.close()
