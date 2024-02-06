#!/usr/bin/env python3
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple

def calculate_great_circle_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two sets of latitude and longitude coordinates.

    Args:
        lat1, lon1, lat2, lon2 (float): Latitude and longitude of two points.

    Returns:
        float: Great-circle distance between the two points.
    """
    R = 6371  # Radius of the Earth in kilometers
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == '__main__':
    # Example usage of the great-circle distance calculation
    distance = calculate_great_circle_distance(40.7128, -74.0060, 34.0522, -118.2437)
    print(f'Great-circle distance: {distance} km')
