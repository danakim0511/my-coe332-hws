# Moonrise Genes
## Description
This project containerizes a Flask-based API for gene data retrieval and manipulation. The API interacts with a Redis database to store gene information fetched from a public dataset. It provides endpoints to load, retrieve, and delete gene data, as well as to fetch specific gene information by gene ID.
## Main Files
- Dockerfile: Contains instructions to build the Docker image for the Flask API.
- docker-compose.yaml: Defines the services required to run the application, including the Flask app and Redis.
- gene_api.py: Python script containing the Flask application code.
- README.md: Documentation file describing how to build and run the Docker container, API usage examples, and data description.
## Instructions to Build
To build the Docker image from the Dockerfile, run the following command in the terminal:
```bash
docker build -t flask-app .
```
## Instructions to Launch
To launch the containerized app along with Redis using docker-compose, execute the following command:
```bash
docker-compose up
```
## Example API Query Commands
### Load Data
```bash
curl -X POST http://localhost:5000/data
```
### Output
```bash
{
  "message": "Data loaded successfully"
}
```
### Retrieve All Data
```bash
curl -X GET http://localhost:5000/data
```
### Output
```bash
[  {    "hgnc_id": "HGNC:5",    "symbol": "A1BG",    "name": "alpha-1-B glycoprotein",    ...  },  {    "hgnc_id": "HGNC:37133",    "symbol": "A1BG-AS1",    "name": "A1BG antisense RNA 1",    ...  },  ...]
```
### Retrieve Gene Data by ID
```bash
curl -X GET http://localhost:5000/genes/HGNC:5
```
### Output
```bash
{
  "hgnc_id": "HGNC:5",
  "symbol": "A1BG",
  "name": "alpha-1-B glycoprotein",
  ...
}
```
## Data Description
The gene data is sourced from the HGNC (HUGO Gene Nomenclature Committee) database, which provides standardized nomenclature for human genes. Each gene entry contains information such as the HGNC ID, gene symbol, gene name, genomic location, gene type, and other relevant details. The data allows researchers and developers to retrieve information about human genes for various biomedical and bioinformatics applications.
## Data Citation
The gene data used in this project is sourced from the HGNC database. For more information about the data and proper citation, please visit the HGNC website.



