import pytest

from services.geocoding import get_coordinates
from shared import TEST_CITY, TEST_COUNTRY, TEST_COORDS


def test_get_coordinates():
    assert get_coordinates(TEST_CITY, TEST_COUNTRY) == TEST_COORDS

def test_get_coordinates_invalid_city():
    with pytest.raises(ValueError):
        get_coordinates("Fake City", "Imaginary Country")