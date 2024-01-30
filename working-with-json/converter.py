import json

def stof( a_list_of_dict, key_string):
    for item in a_list_of_dict:
        item[key_string] = float(item[key_string])
    return a_list_of_dict

with open ('Meteorite_Landings.json', 'r') as fin:
    ml_data = json.load(fin)

things_to_change = ['id', 'mass (g)', 'reclat', 'reclong']
for item in things_to_change:
    ml_data['meteorite_landings'] = stof( ml_data['meteorite_landings'], item)

with open('Meteorite_Landings_updated.json', 'w') as fout:
    json.dump(ml_data, fout, indent=2)


