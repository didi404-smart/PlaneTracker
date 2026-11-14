from unittest.mock import MagicMock, patch

import pytest
from requests import HTTPError

from src.api import APIAdapter, NominatimAPI, OpenSkyAPI


class FakeResponse:
    """Подделывает ответ"""

    def __init__(self, data, ok=True):
        self.data = data
        self.ok = ok

    def raise_for_status(self):
        if not self.ok:
            raise HTTPError("429")

    def json(self):
        return self.data


def test_nominatim():
    box = ["41.6", "83.1", "-141.0", "-52.6"]
    response = FakeResponse([{"boundingbox": box}])
    with patch("src.base_api.get", return_value=response) as fake_get:
        result = NominatimAPI().get_data("Canada")
    assert result == box
    kwargs = fake_get.call_args.kwargs
    assert kwargs["params"]["country"] == "Canada"
    assert "User-Agent" in kwargs["headers"]


def test_nominatim_country_not_found():
    with patch("src.base_api.get", return_value=FakeResponse([])):
        with pytest.raises(ValueError):
            NominatimAPI().get_data("not country")


def test_http_error():
    with patch("src.base_api.get", return_value=FakeResponse({}, ok=False)):
        with pytest.raises(HTTPError):
            OpenSkyAPI().get_data([1, 2, 3, 4])


def test_opensky():
    with patch("src.base_api.get", return_value=FakeResponse({"states": []})) as fake_get:
        result = OpenSkyAPI().get_data([10, 20, 30, 40])
    assert result == {"states": []}
    assert fake_get.call_args.kwargs["params"] == {"lamin": 10, "lamax": 20, "lomin": 30, "lomax": 40}


def test_adapter():
    geo = MagicMock()
    geo.get_data.return_value = [1, 2, 3, 4]
    sky = MagicMock()
    sky.get_data.return_value = {"states": [["x"]]}
    adapter = APIAdapter(geo, sky)
    adapter.get_aeroplanes("Canada")
    geo.get_data.assert_called_once_with("Canada")
    sky.get_data.assert_called_once_with([1, 2, 3, 4])
    assert adapter.aeroplanes == {"states": [["x"]]}
