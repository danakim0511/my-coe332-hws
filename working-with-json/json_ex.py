import json

def compute_average_mass(a_list_of_dicts, a_key_string):
    total_mass = 0.
    for i in range(len(a_list_of_dicts)):
        total_mass += float(a_list_of_dicts[i][a_key_string])
    return (total_mass / len(a_list_of_dicts))

def check_hemisphere(latitude: float, longitude: float) -> str:    # type hints
    location = ''
    if (latitude > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (longitude > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return(location)

def count_classes( a_list_of_dict, 'recclass' ):
    results = {}
    for item in a_list_of_dict:
        if item['recclass'] in results.keys():
            results[ item['recclass'] ] += 1
        else:
            reults[ item['recclass'] ] = 1
    return results

with open ('Meteorite_Landings.json', 'r') as f:
    ml_data = json.load(f)

print(compute_average_mass(ml_data['meteorite_landings'], 'mass (g)'))

for row in ml_data['meteorite_landings']:
    print(check_hemisphere(float(row['reclat']), float(row['reclong'])))

results = count_classes(ml_data['meteorite_landings'], 'recclass') 
for item in results.keys():
    print(i'{item}, {results[item]}')


