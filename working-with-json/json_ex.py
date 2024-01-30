import json

def compute_average_mass(a_list_of_dicts, a_key_string):
    total_mass = 0.
    for item in a_list_of_dicts:
        total_mass += float(item[a_key_string])
    return(total_mass / len(a_list_of_dicts) )

def check_hemisphere(latitude, longitude):
    location = 'Nothern' if (latitude > 0) else 'Southern'
    location = f'{location} & Eastern' if (longitude > 0) else f'{location} & Western'
    return(location)

def count_occurrences( a_list_of_dict, a_key_string ):
    results = {}
    for item in a_list_of_dict:
        if item[a_key_string] in results.keys():
            results[ item[a_key_string] ] += 1
        else:
            results[ item[a_key_string] ] = 1
    return results

with open ('Meteorite_Landings.json', 'r') as f:
    ml_data = json.load(f)

print(compute_average_mass(ml_data['meteorite_landings'], 'mass (g)'))

for row in ml_data['meteorite_landings']:
    print(check_hemisphere(float(row['reclat']), float(row['reclong'])))
 
results = count_occurrences(ml_data['meteorite_landings'], 'recclass')
for item in results.keys():
    print(f'{item} , {results[item]}')
    


