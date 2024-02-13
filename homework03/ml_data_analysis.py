#!/usr/bin/env python

import argparse
import json
import csv
import logging
from typing import List
from math import radians, sin, cos, sqrt, atan2
from great_circle_distance import calculate_great_circle_distance 
import matplotlib.pyplot as plt
import sys
import os

logging.basicConfig(level=logging.WARNING)

def calculate_max_mass(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Calculate the maximum mass from the given list of dictionaries.

    Args:
        a_list_of_dicts (List[dict]): A list of dictionaries that each have the
                                        same set of keys.
        a_key_string (str): A key that appears in each dictionary associated with
                                        the desired value.

    Returns:
        max_mass (float) : Maximum mass value
    """
    masses = []
    for item in a_list_of_dicts:
        if a_key_string in item and item[a_key_string] is not None:
            try:
                masses.append(float(item[a_key_string]))
            except ValueError:
                print(f"Invalid value for key '{a_key_string}': {item[a_key_string]}")
    if masses:
        return max(masses)
    else:
        return 0.0

def calculate_min_mass(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Calculate the minimum mass from the given list of dictionaries.

    Args:
        a_list_of_dicts (List[dict]): A list of dictionaries that each have the
                                        same set of keys.
        a_key_string (str): A key that appears in each dictionary associated with
                                        the desired value.

    Returns:
        min_mass (float) : Minimum mass value
    """
    masses = []
    for item in a_list_of_dicts:
        if a_key_string in item and item[a_key_string] is not None:
            try:
                masses.append(float(item[a_key_string]))
            except ValueError:
                print(f"Invalid value for key '{a_key_string}': {item[a_key_string]}")
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
    valid_coordinates = []

    for item in a_list_of_dicts:
        try:
            if 'reclat' in item and 'reclong' in item and item['reclat'] is not None and item['reclong'] is not None:
                lat = float(item['reclat'])
                lon = float(item['reclong'])
                valid_coordinates.append((lat, lon))
            else:
                print(f"Skipped entry: {item}")
        except ValueError:
            print(f"Invalid latitude or longitude value: {item['reclat']}, {item['reclong']}")

    if valid_coordinates:
        avg_latitude = sum(lat for lat, lon in valid_coordinates) / len(valid_coordinates)
        avg_longitude = sum(lon for lat, lon in valid_coordinates) / len(valid_coordinates)
        return avg_latitude, avg_longitude
    else:
        logging.warning('No valid coordinates found.')
        return 0.0, 0.0

def calculate_distance_between_sites(site1: dict, site2: dict) -> float:
    """
    Calculate the great-circle distance between two landing sites.

    Args:
        site1 (dict): Dictionary representing the first landing site.
        site2 (dict): Dictionary representing the second landing site.

    Returns:
        float: Great-circle distance between the two landing sites.
    """
    lat1, lon1 = float(site1['reclat']), float(site1['reclong'])
    lat2, lon2 = float(site2['reclat']), float(site2['reclong'])

    distance = calculate_great_circle_distance(lat1, lon1, lat2, lon2)
    return distance

def plot_landing_sites(meteorite_data: List[dict]):
    """
    Plot the meteorite landing sites on a scatter plot and save it as an image.

    Args:
        meteorite_data (list): A list of dictionaries, each dict should have the
                               same set of keys.
    """
    latitudes = []
    longitudes = []

    for site in meteorite_data:
        if 'reclat' in site and 'reclong' in site and site['reclat'] is not None and site['reclong'] is not None:
            try:
                latitudes.append(float(site['reclat']))
                longitudes.append(float(site['reclong']))
            except ValueError:
                print(f"Invalid latitude or longitude value: {site['reclat']}, {site['reclong']}")

    if not latitudes or not longitudes:
        print("No valid coordinates found for plotting.")
        return

    plt.scatter(longitudes, latitudes, marker='o', color='blue', alpha=0.5)
    plt.title('Meteorite Landing Sites')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig('meteorite_landing_sites.png')
    plt.show()

def read_data_file(filename: str) -> List[dict]:
    """
    Read data from either CSV or JSON file based on the file extension.

    Args:
        filename (str): Path to the data file.

    Returns:
        List[dict]: A list of dictionaries representing the data.
    """
    if filename.lower().endswith('.csv'):
        return read_csv_file(filename)
    elif filename.lower().endswith('.json'):
        return read_json_file(filename)
    else:
        raise ValueError(f"Unsupported file format for {filename}. Only CSV and JSON are supported.")

def read_csv_file(filename: str) -> List[dict]:
    """
    Read data from a CSV file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        List[dict]: A list of dictionaries representing the data.
    """
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        logging.error('File not found. Exiting.')
        return []

def read_json_file(filename: str) -> List[dict]:
    """
    Read data from a JSON file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        List[dict]: A list of dictionaries representing the data.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            meteorite_landings = data.get('meteorite_landings', [])  # Extract the list from the nested structure
            return meteorite_landings
    except FileNotFoundError:
        logging.error('File not found. Exiting.')
        return []

def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        print("Current working directory:", os.getcwd())  # Add this line
        json_file_path = '/data/Meteorite_Landings.json'  # Correct the path
        ml_data = read_json_file(json_file_path)  # Use the correct path and function
    except FileNotFoundError:
        logging.error('JSON file not found. Exiting.')
        return

    if not ml_data:
        logging.warning('No data found in the JSON file. Exiting.')
        return

    print(f'Maximum Mass: {calculate_max_mass(ml_data, "mass (g)")} g')
    print(f'Minimum Mass: {calculate_min_mass(ml_data, "mass (g)")} g')

    avg_latitude, avg_longitude = calculate_avg_latitude_longitude(ml_data)
    print(f'Average Latitude: {avg_latitude} degrees')
    print(f'Average Longitude: {avg_longitude} degrees')

    if len(ml_data) >= 2:  # Check if there are at least two entries for site1 and site2
        site1 = ml_data[0]
        site2 = ml_data[1]

        distance = calculate_distance_between_sites(site1, site2)
        print(f'Great-circle distance between landing sites: {distance} km')
    else:
        logging.warning('Insufficient data for calculating distance between sites.')

    plot_landing_sites(ml_data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripty.py <filename>")
        sys.exit(1)
    main()

