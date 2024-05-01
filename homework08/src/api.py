# api.py

from flask import Flask, jsonify
import os
from redis import Redis
from hotqueue import HotQueue
import json
from jobs import *

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host=redis_ip, port=6379, db=0)
q = HotQueue('queue', host=redis_ip, port=6379, db=1)
rd2 = Redis(host=redis_ip, port=6379, db=2)

app = Flask(__name__)

@app.route('/data', methods=['DELETE'])
def delete_data() -> str:
    rd2.delete('data')
    message = 'Successfully deleted all the data from the dictionary!\n'
    return message

@app.route('/data', methods=['POST'])
def post_data() -> str:
    data = {}  # Your processed XML data
    rd2.set('data', json.dumps(data))
    message = 'Successfully loaded in the dictionary.\n'
    return message

def list_of_jobs():
    """
    Retrieve a list of all job IDs.

    Returns:
        list: A list of job IDs.
    """
    # Fetch all keys from the Redis database (assuming job IDs are used as keys)
    job_ids = rd2.keys()
    return job_ids

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs():
    jobsList = list_of_jobs()
    # Convert bytes objects to strings before jsonify
    jobsList = [job.decode('utf-8') if isinstance(job, bytes) else job for job in jobsList]
    return jsonify(jobsList)

@app.route('/jobs/<string:route>', methods=['POST'])
def post_job(route: str) -> dict:
    jid = add_job(q, route)  # Pass 'q' as an argument
    return f'Successfully queued a job! \nTo view the status of the job, curl /jobs.\nHere is the job ID: {jid}\n'

@app.route('/jobs/<string:jid>', methods=['GET'])
def get_job(jid: str) -> dict:
    results = rd2.get(jid)
    if results is None:
        return jsonify({'error': 'The job ID is invalid, please try again.'}), 404
    else:
        try:
            json_results = json.loads(results)
            return jsonify(json_results)
        except json.JSONDecodeError as e:
            return jsonify({'error': 'Failed to decode job results: {}'.format(str(e))}), 500

# Route to display all site names
@app.route('/sites', methods=['GET'])
def get_site_names():
    data = get_data()  # Assuming get_data returns data with site names
    site_names = [site['name'] for site in data['sites']]
    return jsonify(site_names)

@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    rd.flushdb()
    return 'Successfully cleared the jobs list!\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')