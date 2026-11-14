import pytest

from src.aeroplane import Aeroplane


def test_init(plane):
    assert plane.icao24 == "abc123"
    assert plane.callsign == "AFL1"
    assert plane.speed == 230.5
    assert plane.altitude == 10000.0


def test_none_values():
    plane = Aeroplane("abc", None, "Canada", None, None)
    assert plane.callsign == "Не указан"
    assert plane.speed == 0.0
    assert plane.altitude == 0.0


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("speed", -1, ValueError),
        ("speed", "fast", TypeError),
        ("speed", True, TypeError),
        ("altitude", "high", TypeError),
        ("icao24", "   ", ValueError),
        ("origin_country", "", ValueError),
        ("on_ground", "yes", TypeError),
    ],
)
def test_invalid_value(plane, field, value, error):
    with pytest.raises(error):
        setattr(plane, field, value)


def invalid_constructor():
    with pytest.raises(ValueError):
        Aeroplane("abc", "x", "canada", -5, 100)


def test_compare_speed(plane):
    slow = Aeroplane("s1", "S", "Canada", 100, 5000)
    assert plane.compare_speed(slow) is True
    assert slow.compare_speed(plane) is False


def test_compare_with_wrong_type(plane):
    with pytest.raises(TypeError):
        plane.compare_speed(100)


def test_compare_height(plane):
    low = Aeroplane("l1", "L", "Canada", 100, 500)
    assert plane.compare_height(low) is True
    assert low.compare_height(plane) is False


def test_from_opensky():
    state = [
        "abc123",
        "AFL1  ",
        "Russia",
        1,
        2,
        37.6,
        55.7,
        10000.0,
        False,
        230.0,
        90,
        0,
        None,
        10100.0,
        "1234",
        False,
        0,
    ]
    plane2 = Aeroplane.plane_from_opensky(state)
    assert plane2.callsign == "AFL1"
    assert plane2.speed == 230.0
    assert plane2.altitude == 10000.0


def test_from_opensky_short_record():
    with pytest.raises(ValueError):
        Aeroplane.plane_from_opensky(["abc", "X"])


def test_str(plane):
    assert "AFL1" in str(plane)
    assert "abc123" in str(plane)


def test_to_dict_from_dict(plane):
    copy = Aeroplane.from_dict(plane.to_dict())
    assert copy.to_dict() == plane.to_dict()
