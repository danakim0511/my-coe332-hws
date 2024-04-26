# jobs.py
import xml.etree.ElementTree as ET
import os
import json

from redis import Redis

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host=redis_ip, port=6379, db=0)
rd2 = Redis(host=redis_ip, port=6379, db=2)

def parse_xml_data(xml_file: str) -> dict:
    """
    Parse the healthcare center data from the given XML file.

    Args:
        xml_file (str): The path to the XML file.

    Returns:
        data (dict): The parsed healthcare center data.
    """
    data = {'sites': []}

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for site in root.findall('.//row'):  # Assuming each site is represented as a 'row' element
            site_data = {}
            for field in site.findall('*'):
                site_data[field.tag] = field.text
            data['sites'].append(site_data)
    except Exception as e:
        print(f"Error parsing XML data: {e}")

    return data

def get_data(xml_file: str = 'SITE_HCC_FCT_DET.xml') -> dict:
    """
    Retrieve the healthcare center data from the XML file and return as a dictionary.

    Args:
        xml_file (str, optional): The path to the XML file. Defaults to 'SITE_HCC_FCT_DET.xml'.

    Returns:
        data (dict): The healthcare center data.
    """
    data = parse_xml_data(xml_file)

    # Store the data in Redis
    try:
        rd.set('healthcare_data', json.dumps(data))
    except Exception as e:
        print(f"Error storing data in Redis: {e}")

    return data

def compute_average_hours(data: dict) -> float:
    """
    Compute the average operating hours per week for all healthcare centers.

    Args:
        data (dict): The healthcare center data.

    Returns:
        average_hours (float): The average operating hours per week.
    """
    total_hours = 0
    num_centers = len(data['sites'])

    for site in data['sites']:
        hours = site.get('Operating Hours per Week', 0)  # Get the operating hours for each site
        total_hours += float(hours)

    if num_centers > 0:
        average_hours = total_hours / num_centers
    else:
        average_hours = 0

    return average_hours

def site_count_by_state(data: dict) -> dict:
    """
    Count the number of healthcare centers in each state.

    Args:
        data (dict): The healthcare center data.

    Returns:
        state_counts (dict): A dictionary containing the count of centers in each state.
    """
    state_counts = {}

    for site in data['sites']:
        state = site.get('Site State Abbreviation')
        if state:
            state_counts[state] = state_counts.get(state, 0) + 1

    return state_counts
