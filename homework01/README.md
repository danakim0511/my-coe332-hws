# Meteorite Data Readers

This set of scripts provides functionality to read meteorite data from different file formats and compute summary statistics. The supported file formats include JSON, CSV, XML, and YAML.

## Common Functions:

### 1. `compute_average_mass(a_list_of_dicts, a_key_string)`:
Computes the average mass from a list of dictionaries.

### 2. `check_hemisphere(latitude, longitude)`:
Determines the hemisphere and location based on latitude and longitude.

### 3. `count_occurrences(a_list_of_dict, a_key_string)`:
Counts occurrences of a specific key in a list of dictionaries.

### 4. `compute_geolocation_range(a_list_of_dicts)`:
Computes the geolocation range (latitude and longitude) from a list of dictionaries.

### 5. `compute_geographical_std_deviation(a_list_of_dicts)`:
Computes the geographical standard deviation from a list of dictionaries.