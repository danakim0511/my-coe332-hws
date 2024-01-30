import xmltodict
import math
from pprint import pprint

def compute_average_mass(a_list_of_dicts, a_key_string):
    if not a_list_of_dicts:
        return 0  # Return 0 if the list is empty to avoid division by zero
    total_mass = sum(float(item[a_key_string]) for item in a_list_of_dicts)
    return total_mass / len(a_list_of_dicts)

def check_hemisphere(latitude, longitude):
    location = 'Northern' if (latitude > 0) else 'Southern'
    location = f'{location} & Eastern' if (longitude > 0) else f'{location} & Western'
    return location

def count_occurrences(a_list_of_dict, a_key_string):
    results = {}
    for item in a_list_of_dict:
        if item[a_key_string] in results.keys():
            results[item[a_key_string]] += 1
        else:
            results[item[a_key_string]] = 1
    return results

def compute_geolocation_range(a_list_of_dicts):
    latitudes = [float(item['reclat']) for item in a_list_of_dicts]
    longitudes = [float(item['reclong']) for item in a_list_of_dicts]

    if not latitudes:
        print("No latitude values found.")
        return {'latitude_range': (0, 0), 'longitude_range': (0, 0)}

    print("Latitudes:", latitudes)
    print("Longitudes:", longitudes)

    return {
        'latitude_range': (min(latitudes), max(latitudes)),
        'longitude_range': (min(longitudes), max(longitudes))
    }

def compute_geographical_std_deviation(a_list_of_dicts):
    latitudes = [float(item['reclat']) for item in a_list_of_dicts]
    longitudes = [float(item['reclong']) for item in a_list_of_dicts]

    if not latitudes:
        print("No latitude values found.")
        return 0  # Return 0 if latitudes is empty to avoid division by zero

    print("Latitudes:", latitudes)
    print("Longitudes:", longitudes)

    mean_latitude = sum(latitudes) / len(latitudes)
    mean_longitude = sum(longitudes) / len(longitudes)

    deviation_sum = sum((lat - mean_latitude)**2 + (lon - mean_longitude)**2 for lat, lon in zip(latitudes, longitudes))

    return math.sqrt(deviation_sum / len(latitudes))

# Open and read the XML file containing meteorite data using xmltodict
with open('Meteorite_Landings.xml', 'r', encoding='utf-8') as xml_file:
    xml_data = xmltodict.parse(xml_file.read())

# Extract meteorite records from the parsed XML data
ml_data = xml_data.get('data', {}).get('meteorite_landings', [])

# Print the extracted meteorite records to inspect their structure
pprint(ml_data)

# Compute average mass
average_mass = compute_average_mass(ml_data, 'mass_g')

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
geolocation_range = compute_geolocation_range(ml_data)

# Geographical standard deviation
geographical_std_deviation = compute_geographical_std_deviation(ml_data)

# Iterate through each meteorite record
for row in ml_data:
    latitude, longitude = float(row['reclat']), float(row['reclong'])
    location = check_hemisphere(latitude, longitude)
    hemisphere_statistics[location] += 1

# Count occurrences of recclass
recclass_occurrences = count_occurrences(ml_data, 'recclass')

# Combine all results into a summary dictionary
summary_statistics = {
    'average_mass': average_mass,
    'hemisphere_statistics': hemisphere_statistics,
    'geolocation_range': geolocation_range,
    'geographical_std_deviation': geographical_std_deviation,
    'recclass_occurrences': recclass_occurrences
}

# Output summary statistics in a readable format using pprint
pprint(summary_statistics)