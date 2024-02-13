
## Homework 03: The Royal Containers
This project continues the analysis of Meteorite Landings data from NASA using Python scripts. The code is containerized using Docker for easier deployment and reproducibility. The primary script, ml_data_analysis.py, reads the Meteorite Landings data, performs various analyses, and generates a scatter plot of the landing sites. Unit tests are provided to ensure the correctness of the implemented functions.

## Contents
### 1. Primary Script (ml_data_analysis.py)
Reads Meteorite Landings data in CSV or JSON format.
Computes summary statistics, great-circle distances, and generates a scatter plot.
Great Circle Distance Algorithm (great_circle_distance.py)

### 2. Standalone module providing the great-circle distance calculation.
### 3. Unit Test Scripts
test_ml_data_analysis.py: Tests for functions in the primary script.
test_gcd_algorithm.py: Tests for the great-circle distance algorithm.
### 4. Dockerfile
Defines the Docker image to containerize the project.
### 5. README.md
Descriptive documentation with instructions for running the tool in a Docker container.

## Data Source
To run the primary script successfully, download the Meteorite Landings dataset in CSV or JSON format from NASA and save it as 'Meteorite_Landings.csv' or 'Meteorite_Landings.json' in the project directory.

## Running the Code in Docker Container
### 1. Clone the repository:
    bash
    Copy code
    git clone https://github.com/danakim0511/my-coe332-hws.git
### 2. Navigate to the homework03 directory:
    bash
    Copy code
    cd COE-332-Homeworks/homework03
### 3. Build the Docker image:
    bash
    Copy code
    docker build -t danakim/ml_data_analysis:latest .
### 4. Download the Meteorite Landing dataset (CSV or JSON) and save it in the homework03 directory.
### 5. Run the Docker container:
    bash
    Copy code
    docker run --rm -it -v $PWD/Meteorite_Landings.json:/data/Meteorite_Landings.json danakim/ml_data_analysis:latest
### 6. Review the printed summary statistics and check the generated 'meteorite_landing_sites.png' image.

## Running Unit Tests in Docker Container
### 1. Build the Docker image with the test dependencies:
    bash
    Copy code
    docker build -t danakim/ml_data_analysis_test:latest -f Dockerfile.test .
### 2. Run the Docker container with unit tests:
    bash
    Copy code
    docker run --rm danakim/ml_data_analysis_test:latest
### 3. Review the test results.

## Results Interpretation
The script prints various summary statistics, including maximum and minimum mass, average latitude and longitude, and hemisphere distribution.
The scatter plot visually represents the distribution of meteorite landing sites.