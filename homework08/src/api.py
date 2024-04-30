# api.py

from flask import Flask, request, send_file, jsonify
import requests
import json
import os
from redis import Redis
from hotqueue import HotQueue
from jobs import add_job

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host=redis_ip, port=6379, db=0)
q = HotQueue('queue', host=redis_ip, port=6379, db=1)
rd2 = Redis(host=redis_ip, port=6379, db=2)

app = Flask(__name__)

@app.route('/data', methods=['DELETE'])
def delete_data() -> str:
    """
    This function deletes the data completely.

    Returns:
        message (str): Message saying that the data was deleted.
    """

    rd2.delete('data')

    message = 'Successfully deleted all the data from the dictionary!\n'
    return message

@app.route('/data', methods=['POST'])
def post_data() -> str:
    """
    This function adds the DATA dictionary object with the data from the web and returns
    a success message.

    Returns:
        message (str): Message saying that the data was successfully reloaded.
    """

    # Assuming you have logic here to fetch and process XML data into dictionary format
    data = {}  # Your processed XML data

    rd2.set('data', json.dumps(data))

    message = 'Successfully loaded in the dictionary.\n'

    return message

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs():
    jobsList = list_of_jobs()
    return jsonify(jobsList)

@app.route('/jobs/<string:route>', methods=['POST'])
def post_job(route: str) -> dict:
    jid = add_job(q, route)
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

@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    rd.flushdb()
    return 'Successfully cleared the jobs list!\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
