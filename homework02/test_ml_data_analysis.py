from ml_data_analysis import (
    calculate_max_mass,
    calculate_min_mass,
    calculate_avg_latitude_longitude,
    calculate_distance_between_sites,
)

import pytest

sample_data = [
    {'mass (g)': '100'},
    {'mass (g)': '200'},
    {'mass (g)': '300'},
    {'mass (g)': '400'},
]

def test_calculate_max_mass():
    assert calculate_max_mass(sample_data, 'mass (g)') == 400.0

def test_calculate_max_mass_empty():
    assert calculate_max_mass([], 'mass (g)') == 0.0

def test_calculate_min_mass():
    assert calculate_min_mass(sample_data, 'mass (g)') == 100.0

def test_calculate_min_mass_empty():
    assert calculate_min_mass([], 'mass (g)') == 0.0

def test_calculate_avg_latitude_longitude():
    data = [{'reclat': '10', 'reclong': '20'}, {'reclat': '30', 'reclong': '40'}]
    assert calculate_avg_latitude_longitude(data) == (20.0, 30.0)

def test_calculate_avg_latitude_longitude_empty():
    assert calculate_avg_latitude_longitude([]) == (0.0, 0.0)

def test_calculate_distance_between_sites():
    site1 = {'reclat': '10', 'reclong': '20'}
    site2 = {'reclat': '30', 'reclong': '40'}
    assert calculate_distance_between_sites(site1, site2) == pytest.approx(2225.885)
