import csv
import logging
from typing import List
from math import radians, sin, cos, sqrt, atan2
# Importing the great-circle distance function
from great_circle_distance import calculate_great_circle_distance 
import matplotlib.pyplot as plt
# Set the Matplotlib logging level to WARNING
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
    masses = [float(item[a_key_string]) for item in a_list_of_dicts if item[a_key_string] is not None]
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
        max_mass (float) : Maximum mass value
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
    latitudes = [float(site['reclat']) for site in meteorite_data]
    longitudes = [float(site['reclong']) for site in meteorite_data]

    plt.scatter(longitudes, latitudes, marker='o', color='blue', alpha=0.5)
    plt.title('Meteorite Landing Sites')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig('meteorite_landing_sites.png')
    plt.show()


def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        with open('Meteorite_Landings.csv', 'r') as f:
            reader = csv.DictReader(f)
            ml_data = list(reader)
    except FileNotFoundError:
        logging.error('CSV file not found. Exiting.')
        return

    print(f'Maximum Mass: {calculate_max_mass(ml_data, "mass (g)")} g')
    print(f'Minimum Mass: {calculate_min_mass(ml_data, "mass (g)")} g')

    avg_latitude, avg_longitude = calculate_avg_latitude_longitude(ml_data)
    print(f'Average Latitude: {avg_latitude} degrees')
    print(f'Average Longitude: {avg_longitude} degrees')

    # Example usage of great-circle distance calculation
    site1 = ml_data[0]
    site2 = ml_data[1]
    
    distance = calculate_distance_between_sites(site1, site2)
    print(f'Great-circle distance between landing sites: {distance} km')
    
    plot_landing_sites(ml_data)
    
if __name__ == '__main__':
    main()

