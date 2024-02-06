from great_circle_distance import calculate_great_circle_distance
import pytest

def test_calculate_great_circle_distance():
    # Example coordinates and their expected distances
    test_cases = [
        ((40.7128, -74.0060, 34.0522, -118.2437), 3964.686),
        ((0, 0, 0, 0), 0),  # Distance between the same point should be 0
        ((45.0, 0.0, -45.0, 180.0), 10007.543),  # Opposite points on the globe
        # Add more test cases as needed
    ]

    for coordinates, expected_distance in test_cases:
        lat1, lon1, lat2, lon2 = coordinates
        obtained_distance = calculate_great_circle_distance(lat1, lon1, lat2, lon2)
        assert obtained_distance == pytest.approx(expected_distance, abs=1e-3)

if __name__ == '__main__':
    # Run the tests using pytest
    pytest.main(['-v', 'test_great_circle_distance.py'])