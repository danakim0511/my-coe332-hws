# Homework 05 The Darjeeling Flask

## Objective

This project provides a Flask application for tracking the International Space Station (ISS) using NASA's ISS data API. The app exposes several routes to retrieve information about ISS state vectors, including the entire data set, state vectors for a specific epoch, instantaneous speed for a specific epoch, and state vectors with instantaneous speed for the epoch nearest in time.

## How to Access the Data

The ISS data is fetched from the NASA API. You can access the data by making a GET request to the following URL:
[ISS Data API](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)

## Building the Container

To build the Docker container for the Flask app, navigate to the project directory and run the following command:
