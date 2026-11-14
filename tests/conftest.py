import pytest

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


@pytest.fixture
def plane():
    return Aeroplane(" ABC123 ", " AFL1 ", "Russia", 230.5, 10000, False)


@pytest.fixture
def storage(tmp_path):
    storage = JSONStorage(str(tmp_path / "data" / "planes.json"))
    storage.add_aeroplanes(
        [
            Aeroplane("a1", "AFL1", "Russia", 230, 10000, False),
            Aeroplane("b2", "ACA2", "Canada", 210, 9000, False),
            Aeroplane("c3", "DLH3", "Canada", 0, 0, True),
        ]
    )
    return storage
