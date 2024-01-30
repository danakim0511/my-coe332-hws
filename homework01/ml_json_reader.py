import json
import math
import argparse

# Function to compute the average mass from a list of dictionaries
def compute_average_mass(a_list_of_dicts, a_key_string):
    total_mass = sum(float(item[a_key_string]) for item in a_list_of_dicts)
    return total_mass / len(a_list_of_dicts)

# Function to determine the hemisphere and location based on latitude and longitude
def check_hemisphere(latitude, longitude):
    location = 'Northern' if (latitude > 0) else 'Southern'
    location = f'{location} & Eastern' if (longitude > 0) else f'{location} & Western'
    return location

# Function to count occurrences of a specific key in a list of dictionaries
def count_occurrences(a_list_of_dict, a_key_string):
    results = {}
    for item in a_list_of_dict:
        if item[a_key_string] in results.keys():
            results[item[a_key_string]] += 1
        else:
            results[item[a_key_string]] = 1
    return results

# Function to compute the geolocation range (latitude and longitude) from a list of dictionaries
def compute_geolocation_range(a_list_of_dicts):
    latitudes = [float(item['reclat']) for item in a_list_of_dicts]
    longitudes = [float(item['reclong']) for item in a_list_of_dicts]

    return {
        'latitude_range': (min(latitudes), max(latitudes)),
        'longitude_range': (min(longitudes), max(longitudes))
    }

# Function to compute the geographical standard deviation from a list of dictionaries
def compute_geographical_std_deviation(a_list_of_dicts):
    latitudes = [float(item['reclat']) for item in a_list_of_dicts]
    longitudes = [float(item['reclong']) for item in a_list_of_dicts]

    # Compute mean latitude and mean longitude
    mean_latitude = sum(latitudes) / len(latitudes)
    mean_longitude = sum(longitudes) / len(longitudes)

    # Compute the sum of squared deviations
    deviation_sum = sum((lat - mean_latitude)**2 + (lon - mean_longitude)**2 for lat, lon in zip(latitudes, longitudes))

    # Compute the square root of the average squared deviations
    return math.sqrt(deviation_sum / len(latitudes))

# Main function to execute the script
def main():
    # Setup argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Compute summary statistics for meteorite data.')
    parser.add_argument('input_file', help='Path to the JSON file containing meteorite data.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Open the JSON file containing meteorite data
    with open(args.input_file, 'r') as f:
        ml_data = json.load(f)

    # Compute average mass
    average_mass = compute_average_mass(ml_data['meteorite_landings'], 'mass (g)')

    # Check hemisphere and location statistics
    hemisphere_statistics = {
        'Northern': 0,
        'Southern': 0,
        'Northern & Eastern': 0,
        'Southern & Eastern': 0,
        'Northern & Western': 0,
        'Southern & Western': 0
    }

    # Geolocation range
    geolocation_range = compute_geolocation_range(ml_data['meteorite_landings'])

    # Geographical standard deviation
    geographical_std_deviation = compute_geographical_std_deviation(ml_data['meteorite_landings'])

    # Iterate through each meteorite record
    for row in ml_data['meteorite_landings']:
        latitude, longitude = float(row['reclat']), float(row['reclong'])
        location = check_hemisphere(latitude, longitude)
        hemisphere_statistics[location] += 1

    # Count occurrences of recclass
    recclass_occurrences = count_occurrences(ml_data['meteorite_landings'], 'recclass')

    # Combine all results into a summary dictionary
    summary_statistics = {
        'average_mass': average_mass,
        'hemisphere_statistics': hemisphere_statistics,
        'geolocation_range': geolocation_range,
        'geographical_std_deviation': geographical_std_deviation,
        'recclass_occurrences': recclass_occurrences
    }

    # Output summary statistics in JSON format
    print(json.dumps(summary_statistics, indent=2))

# Check if the script is being run as the main module
if __name__ == "__main__":
    main()
