from great_circle_distance import calculate_great_circle_distance
import pytest

def test_calculate_great_circle_distance():
    # Example coordinates and their correct expected distances
    test_cases = [
        ((40.7128, -74.0060, 34.0522, -118.2437), pytest.approx(3935.746, abs=1.0e-03)),
        ((0, 0, 0, 0), pytest.approx(0, abs=1.0e-03)),  # Distance between the same point should be 0
        ((45.0, 0.0, -45.0, 180.0), pytest.approx(20015.086796020572, abs=1.0e-03)),  # Opposite points on the globe
    ]

    for coordinates, expected_distance in test_cases:
        lat1, lon1, lat2, lon2 = coordinates
        obtained_distance = calculate_great_circle_distance(lat1, lon1, lat2, lon2)
        assert obtained_distance == expected_distance

if __name__ == '__main__':
    # Run the tests using pytest
    pytest.main(['-v', 'test_great_circle_distance.py'])
