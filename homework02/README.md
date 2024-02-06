## Homework 02: Rushmeteorite

## Description:
This project focuses on analyzing Meteorite Landings data from NASA using Python scripts. The primary script reads a CSV-formatted dataset, performs various summary statistics, and uses a great-circle distance algorithm to calculate distances between landing sites. Additionally, the project includes a secondary script containing the great-circle distance funciton and two unit test scripts to ensure the accuracy of the implemented functions.

## Contents
### 1. Primary Script (ml_data_analysis.py)
Reads in Meteorite Landings data.
Computes summary statistics, such as maximum and minimum mass, average latitude and longitude, and great-circle distances between landing sites.
Generate a scatter plot of meteorite landing sites and saves it as an image.
### 2. Secondary Script (great_circle_distance.py)
Contains the standalone great-circle distance algorithm, used by the primary script.
### 3. Unit Test Scripts
test_ml_data_analysis.py: Tests for functions in the primary script
test_gcd_algorithm.py: Test for the great-circle distance algorithm
### 4. README.md
Descriptive documentation providing information on the project's purpose, script functionalities, and instructions for running the code

## Data Source
To run the primary script successfully, download the Meteorite Landings dataset in CSV format from ASA and save it as 'Meteorite_Landings.csv' in the project directory.

## Running the Code
### 1. Clone the repository
git clone https://github.com/danakim0511/my-coe332-hws.git
### 2. Navigate to the homework02 directory
cd COE-332-Homeworks/homework02
### 3. Install required dependencies (Ensure you have Python3, matplotlib, and pip)
### 4. Download the Meteorite Landingdataset and save it as 'Meteorite_Landings.csv' in the homework02 directory
### 5. Run the primary script:
python ml_data_analysis.py
### 6. Review the printied summary statistics and check the generated 'meteorite_landing_sites.png' image.

## Results Interpretation
The script prints various summary statistics, including maximum and minimum mass, average latitude and longitude, and hemisphere distribution.
The scatter plot visually represents the distribution of meteorite landing sites.
