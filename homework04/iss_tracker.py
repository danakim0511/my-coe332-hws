import requests
from typing import List, Dict, Any
from dateutil import parser
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import json
import xmltodict

def parse_iss_data(xml_data: dict) -> List[Dict[str, str]]:
    iss_data = []

    try:
        # Extract necessary information based on your XML structure
        state_vectors = xml_data.get("ndm", {}).get("oem", {}).get("body", {}).get("segment", {}).get("metadata", {}).get("OBJECT_NAME", [])

        if not state_vectors:
            raise ValueError("No state vectors found in the XML data.")

        for state_vector in state_vectors:
            data_point = {
                "EPOCH": state_vector.get("@epoch", ""),
                "X": state_vector.get("X", {}).get("#text", ""),
                "Y": state_vector.get("Y", {}).get("#text", ""),
                "Z": state_vector.get("Z", {}).get("#text", ""),
                "X_DOT": state_vector.get("X_DOT", {}).get("#text", ""),
                "Y_DOT": state_vector.get("Y_DOT", {}).get("#text", ""),
                "Z_DOT": state_vector.get("Z_DOT", {}).get("#text", ""),
            }
            iss_data.append(data_point)

        return iss_data
    except Exception as e:
        print(f"Error parsing ISS data: {e}")
        return []

def calculate_average_speed(iss_data: List[Dict[str, str]]) -> float:
    total_speed = 0
    for data_point in iss_data:
        total_speed += (
            (float(data_point["X_DOT"])**2 +
             float(data_point["Y_DOT"])**2 +
             float(data_point["Z_DOT"])**2)**0.5
        )
    return total_speed / len(iss_data)

def find_closest_data_point(iss_data: List[Dict[str, str]]) -> Dict[str, str]:
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    iss_data.sort(key=lambda x: abs(now - parser.isoparse(x["EPOCH"])))
    return iss_data[0]

def print_data_range(iss_data: List[Dict[str, str]]):
    start_epoch = iss_data[0]["EPOCH"]
    end_epoch = iss_data[-1]["EPOCH"]
    print(f"Data range from {start_epoch} to {end_epoch}")

def main():
    try:
        # Make a GET request to the ISS data URL
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML content using xmltodict and convert to JSON
            data_json = json.loads(json.dumps(xmltodict.parse(response.content)))

            # Extract state vector information from the parsed data
            iss_data = parse_iss_data(data_json)

            # Print the data range
            print_data_range(iss_data)

            # Find the closest data point to 'now'
            closest_data_point = find_closest_data_point(iss_data)
            print(f"\nClosest data point to 'now': {closest_data_point}")

            # Calculate and print average speed
            avg_speed = calculate_average_speed(iss_data)
            print(f"\nAverage speed over the whole data set: {avg_speed} km/s")

            # Calculate and print instantaneous speed closest to 'now'
            instant_speed = (
                float(closest_data_point["X_DOT"])**2 +
                float(closest_data_point["Y_DOT"])**2 +
                float(closest_data_point["Z_DOT"])**2
            )**0.5
            print(f"Instantaneous speed closest to 'now': {instant_speed} km/s")

        else:
            print(f"Failed to fetch ISS data. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

