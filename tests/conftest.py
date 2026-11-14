import pytest

from src.aeroplane import Aeroplane

@pytest.fixture
def plane():
    return Aeroplane(' ABC123 ', ' AFL1 ', 'Russia', 230.5, 10000, False)