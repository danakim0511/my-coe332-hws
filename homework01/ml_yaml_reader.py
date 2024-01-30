import yaml
import math
import argparse
from pprint import pprint

def compute_average_mass(a_list_of_dicts):
    total_mass = 0
    count = 0

    for item in a_list_of_dicts:
        # Check if 'GeoLocation' key is present and non-empty
        if 'GeoLocation' in item and item['GeoLocation']:
            # Extract latitude and longitude from the 'GeoLocation' string
            geo_location = item['GeoLocation']
            reclat, reclong = map(float, geo_location.strip('()').split(','))
            # Check if latitude and longitude are not zero
            if reclat != 0 or reclong != 0:
                # Access 'mass (g)' from the current dictionary
                if 'mass (g)' in item:
                    total_mass += float(item['mass (g)'])
                    count += 1

    return total_mass / count if count > 0 else 0

def compute_geolocation_range(a_list_of_dicts):
    latitudes = [float(item['GeoLocation'].split(',')[0].strip('()')) for item in a_list_of_dicts if 'GeoLocation' in item and item['GeoLocation']]
    longitudes = [float(item['GeoLocation'].split(',')[1].strip('()')) for item in a_list_of_dicts if 'GeoLocation' in item and item['GeoLocation']]

    if not latitudes or not longitudes:
        return {'latitude_range': (0, 0), 'longitude_range': (0, 0)}

    return {
        'latitude_range': (min(latitudes), max(latitudes)),
        'longitude_range': (min(longitudes), max(longitudes))
    }

def compute_geographical_std_deviation(a_list_of_dicts):
    latitudes = [float(item['GeoLocation'].split(',')[0].strip('()')) for item in a_list_of_dicts if 'GeoLocation' in item and item['GeoLocation']]
    longitudes = [float(item['GeoLocation'].split(',')[1].strip('()')) for item in a_list_of_dicts if 'GeoLocation' in item and item['GeoLocation']]

    if not latitudes or not longitudes:
        return 0

    mean_latitude = sum(latitudes) / len(latitudes) if len(latitudes) > 0 else 0
    mean_longitude = sum(longitudes) / len(longitudes) if len(longitudes) > 0 else 0

    deviation_sum = sum((lat - mean_latitude)**2 + (lon - mean_longitude)**2 for lat, lon in zip(latitudes, longitudes))

    return math.sqrt(deviation_sum / len(latitudes)) if len(latitudes) > 0 else 0

def count_recclass_occurrences(a_list_of_dicts):
    results = {}

    for item in a_list_of_dicts:
        if 'recclass' in item:
            recclass = item['recclass']
            if recclass in results:
                results[recclass] += 1
            else:
                results[recclass] = 1

    return results

# Main function to execute the script
def main():
    # Setup argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Compute summary statistics for meteorite data.')
    parser.add_argument('input_file', help='Path to the YAML file containing meteorite data.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Open the YAML file containing meteorite data
    with open(args.input_file, 'r', encoding='utf-8') as yamlfile:
        # Use yaml.safe_load to load the YAML file into a list of dictionaries
        ml_data = yaml.safe_load(yamlfile)

    # Compute average mass
    average_mass = compute_average_mass(ml_data['meteorite_landings'])

    # Print average mass
    print(f"Average Mass: {average_mass:.2f}")

    # Print geolocation range
    geolocation_range = compute_geolocation_range(ml_data['meteorite_landings'])
    print("Geolocation Range:")
    pprint(geolocation_range)

    # Print geographical standard deviation
    geographical_std_deviation = compute_geographical_std_deviation(ml_data['meteorite_landings'])
    print(f"Geographical Standard Deviation: {geographical_std_deviation:.2f}")

    # Count occurrences of 'recclass'
    recclass_occurrences = count_recclass_occurrences(ml_data['meteorite_landings'])

    # Print summary statistics of 'recclass' occurrences
    print("Recclass Occurrences:")
    for recclass, count in recclass_occurrences.items():
        print(f'{recclass} , {count}')

# Check if the script is being run as the main module
if __name__ == "__main__":
    main()
