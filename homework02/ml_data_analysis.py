#!/usr/bin/env python3
import csv
import logging
from typing import List
from math import radians, sin, cos, sqrt, atan2


def calculate_great_circle_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two sets of latitude and longitude coordinates.

    Args:
        lat1, lon1, lat2, lon2 (float): Latitude and longitude of two points.

    Returns:
        distance (float): Great-circle distance between the two points.
    """
    R = 6371  # Radius of the Earth in kilometers
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_max_mass(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Calculate the maximum mass from a list of dictionaries.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        max_mass (float): Maximum mass value.
    """
    masses = [float(item[a_key_string]) for item in a_list_of_dicts if item[a_key_string] is not None]
    if masses:
        return max(masses)
    else:
        return 0.0

def calculate_min_mass(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Calculate the minimum mass from a list of dictionaries.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        min_mass (float): Minimum mass value.
    """
    masses = [float(item[a_key_string]) for item in a_list_of_dicts if item[a_key_string] is not None]
    if masses:
        return min(masses)
    else:
        return 0.0

def calculate_avg_latitude_longitude(a_list_of_dicts: List[dict]) -> tuple:
    """
    Calculate the average latitude and longitude from a list of dictionaries.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.

    Returns:
        avg_latitude (float): Average latitude value.
        avg_longitude (float): Average longitude value.
    """
    valid_coordinates = [(float(item['reclat']), float(item['reclong'])) for item in a_list_of_dicts
                         if item['reclat'] is not None and item['reclong'] is not None]

    if valid_coordinates:
        avg_latitude = sum(lat for lat, lon in valid_coordinates) / len(valid_coordinates)
        avg_longitude = sum(lon for lat, lon in valid_coordinates) / len(valid_coordinates)
        return avg_latitude, avg_longitude
    else:
        logging.warning('No valid coordinates found.')
        return 0.0, 0.0

def count_classes(a_list_of_dicts: List[dict], a_key_string: str) -> dict:
    """
    Iterates through a list of dictionaries, and pulls out the value associated
    with a given key. Counts the number of times each value occurs in the list of
    dictionaries and returns the result.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value.

    Returns:
        classes_observed (dict): Dictionary of class counts.
    """
    classes_observed = {}
    for item in a_list_of_dicts:
        if item[a_key_string] in classes_observed:
            classes_observed[item[a_key_string]] += 1
        else:
            classes_observed[item[a_key_string]] = 1
    return classes_observed

def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        with open('Meteorite_Landings.csv', 'r') as f:
            reader = csv.DictReader(f)
            ml_data = list(reader)
    except FileNotFoundError:
        logging.error('CSV file not found. Exiting.')
        return

    print(f'Average Mass: {compute_average_mass_new(ml_data, "mass (g)")} g')
    print(f'Maximum Mass: {calculate_max_mass(ml_data, "mass (g)")} g')
    print(f'Minimum Mass: {calculate_min_mass(ml_data, "mass (g)")} g')

    avg_latitude, avg_longitude = calculate_avg_latitude_longitude(ml_data)
    print(f'Average Latitude: {avg_latitude} degrees')
    print(f'Average Longitude: {avg_longitude} degrees')

    for row in ml_data:
        latitude, longitude = float(row['reclat']), float(row['reclong'])
        print(check_hemisphere(latitude, longitude))

    print(count_classes(ml_data, 'recclass'))

    # Example usage of great-circle distance calculation
    distance = calculate_great_circle_distance(40.7128, -74.0060, 34.0522, -118.2437)
    print(f'
