# import statements
import requests
from typing import List, Dict
from datetime import datetime
import xml.etree.ElementTree as ET

# Function to parse the ISS data from the XML file
def parse_iss_data(xml_file_path: str) -> List[Dict[str, str]]:
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    iss_data = []

    for state_vector in root.findall(".//stateVector"):
        data_point = {
            "EPOCH": state_vector.find("EPOCH").text,
            "X": state_vector.find("X").text,
            "Y": state_vector.find("Y").text,
            "Z": state_vector.find("Z").text,
            "X_DOT": state_vector.find("X_DOT").text,
            "Y_DOT": state_vector.find("Y_DOT").text,
            "Z_DOT": state_vector.find("Z_DOT").text,
        }
        iss_data.append(data_point)

    return iss_data

# Function to calculate average speed
def calculate_average_speed(iss_data: List[Dict[str, str]]) -> float:
    total_speed = 0
    for data_point in iss_data:
        total_speed += (
            (float(data_point["X_DOT"])**2 +
             float(data_point["Y_DOT"])**2 +
             float(data_point["Z_DOT"])**2)**0.5
        )
    return total_speed / len(iss_data)

# Function to find the closest data point to "now"
def find_closest_data_point(iss_data: List[Dict[str, str]]) -> Dict[str, str]:
    now = datetime.utcnow()
    iss_data.sort(key=lambda x: abs(now - datetime.fromisoformat(x["EPOCH"])))
    return iss_data[0]

# Function to print data range statement
def print_data_range(iss_data: List[Dict[str, str]]):
    start_epoch = iss_data[0]["EPOCH"]
    end_epoch = iss_data[-1]["EPOCH"]
    print(f"Data range from {start_epoch} to {end_epoch}")

# Main function
def main():
    try:
        xml_file_path = "ISS.OEM_J2K_EPH.xml"
        iss_data = parse_iss_data(xml_file_path)

        print_data_range(iss_data)

        closest_data_point = find_closest_data_point(iss_data)
        print(f"\nClosest data point to 'now': {closest_data_point}")

        avg_speed = calculate_average_speed(iss_data)
        print(f"\nAverage speed over the whole data set: {avg_speed} km/s")

        instant_speed = (
            float(closest_data_point["X_DOT"])**2 +
            float(closest_data_point["Y_DOT"])**2 +
            float(closest_data_point["Z_DOT"])**2
        )**0.5
        print(f"Instantaneous speed closest to 'now': {instant_speed} km/s")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
