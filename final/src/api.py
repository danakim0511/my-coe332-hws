#!/usr/bin/env python3
import csv
import pandas as pd
from flask import Flask, request, jsonify
import redis   # might not need this 
import requests
import json
from jobs import add_job, get_job_by_id, rd
# !NOTE! not importing the q or jdb client 

app = Flask(__name__)

df = dict(pd.read_csv('https://query.data.world/s/oyh5v7rzzagyct765pfrsu5iljegv2?dws=00000'))

@app.route('/data', methods=['GET', 'POST', 'DELETE'])
def fqhc_data():
    """
    Manages health center data in Redis 

    POST:
        Loads health center data into Redis
    GET:
        Retrieves health center data from Redis
    DELETE:
        Deletes all health center data stored in Redis

    Returns:
        str: Response message 
    """
    if request.method == 'GET':
        # read all data out to Redis and return it as a JSON list
        data = df
        data = [json.loads(rd.get(key)) for key in rd.keys()]
        return jsonify(data), 200
    
    elif request.method == 'POST':
        # load the FQHC data to a redis database
        #reponse = requests.get(df)
        #data = reponse.json()['response']['docs']
        for item in data:
            rd.set(item['health_center_site_fact_identification_number'], json.dumps(item))
        return 'Data loaded into Redis successfully\n', 200

    elif request.method == 'DELETE':
        # delete all data from redis
        rd.flushdb()
        return 'Data deleted from Redis succesfully\n', 200

@app.route('/fqhcs', methods=['GET'])
def fqhcs():
    """
    Returns json-formatted list of all federally quailified health centers
    """
    keys = rd.keys()
    fqhc_data = []
    for key in keys:
        fqhc_id = key.decode('utf-8')
        fqhc = rd.get(key)
        fqhc_data.append({fqhc_id: json.loads(fqhc)})
    return jsonify(fqhc_data), 200

@app.route('/fqhcs/<site_name>', methods=['GET'])
def specific_fqhc(site_name):
    """
    Returns all data associated with a given specific fqhc site name

    Args:

    Returns:

    """
    fqhc_data = rd.get(site_name)
    if fqhc_data:
        return fqhc_data, 200
    else:
        return 'Gene ID not found\n', 404

# *** ADD A COUPLE MORE ROUTES ***

### JOB STUFF ###
@app.route('/jobs', methods=['POST', 'GET'])
def submit_job():
    """
    Posts/Gets a job by filtering through the data, extracting date_modified for each health center and making a new dicitionary holding all the health centers within the specified ...
    """
    if request.method == 'POST':
        data = request.get_json()    
        start_date = data.get('start_date')   # modify this based on new parameters
        end_date = data.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "Please specify a start and end date."})

        job_dict = add_job(start_date, end_date)   
        return job_dict
    elif request.method == 'GET':
        job_ids = [job.decode('utf-8') for job in rd.keys()]
        return job_ids

@app.route('/jobs/<jobid>', methods=['GET'])
def get_job(jobid):
    """
    Returns a job specified by a unique jobid
    """
    return get_job_by_id(jobid)

@app.route('/results/<jobid>', methods=['GET'])
def get_results(jobid):
    """
    Returns the analysis the worker made given a job id
    """
    try:
        job_data = get_job_by_id(jobid)
        if job_data['status'] == 'complete':
            results = get_analysis_results(jobid)
            return jsonify(results)
        else:
            return "Job is still in progress..."
    except ValueError:
        print(f"Job id is invalid.")
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)