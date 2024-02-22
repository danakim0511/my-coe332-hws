# Homework 04 The ISS Aquatic

## Overview

This project provides a Python script to track the International Space Station (ISS) based on NASA's open data. The script parses real-time ISS data, calculates average speed, finds the closest data point to the current time, and prints relevant information.

## Folder Contents

- `iss_tracker.py`: Python script to track ISS and calculate relevant metrics.
- `test_iss_tracker.py`: Unit tests for the ISS tracker script.
- `Dockerfile`: Docker configuration file for containerization.
- `requirements.txt`: List of Python dependencies.

## Data Set

The ISS data set is retrieved in real-time from NASA's public data repository. You can access the original data [here](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml).

## Building the Container

To build the Docker container, execute the following commands:

```bash
docker build -t iss-tracker:latest .

## Running the Container

Execute the following command to run the unit tests:

docker run iss-tracker python3 -m unittest test_iss_tracker.py

# Expected Output

## Script Execution

Upon running the script, you can expect to see information about the ISS, including the data range, the closest data point to the current time, and average speed.

## Unit Tests

The unit tests validate the functionality of the ISS tracker script. A successful run will display "OK," indicating that all tests passed.