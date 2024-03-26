from flask import Flask, jsonify, request
import requests
import redis
import csv
import json

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def parse_hgnc_data(url):
    response = requests.get(url)
    response.raise_for_status()
    decoded_content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(decoded_content.splitlines(), delimiter='\t')
    data = [row for row in csv_reader]
    return data


@app.route('/data', methods=['POST'])
def load_data():
    """
    Load HGNC data to Redis database.
    """
    try:
        hgnc_data = parse_hgnc_data("https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/tsv/hgnc_complete_set.txt")
        redis_client.set('hgnc_data', json.dumps(hgnc_data))
        return jsonify({'message': 'Data loaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/data', methods=['GET'])
def get_data():
    """
    Read all data out of Redis and return it as a JSON list.
    """
    try:
        hgnc_data = redis_client.get('hgnc_data')
        if hgnc_data:
            return jsonify(json.loads(hgnc_data)), 200
        else:
            return jsonify({'message': 'No data available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/data', methods=['DELETE'])
def delete_data():
    """
    Delete all data from Redis.
    """
    try:
        redis_client.delete('hgnc_data')
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/genes', methods=['GET'])
def get_gene_ids():
    """
    Return json-formatted list of all hgnc_ids.
    """
    try:
        hgnc_data = redis_client.get('hgnc_data')
        if hgnc_data:
            hgnc_data = json.loads(hgnc_data)
            gene_ids = [entry['hgnc_id'] for entry in hgnc_data]
            return jsonify(gene_ids), 200
        else:
            return jsonify({'message': 'No data available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/genes/<hgnc_id>', methods=['GET'])
def get_gene_data(hgnc_id):
    """
    Return all data associated with a given <hgnc_id>.
    """
    try:
        hgnc_data = redis_client.get('hgnc_data')
        if hgnc_data:
            hgnc_data = json.loads(hgnc_data)
            for entry in hgnc_data:
                if entry['hgnc_id'] == hgnc_id:
                    return jsonify(entry), 200
            return jsonify({'message': 'Gene ID not found'}), 404
        else:
            return jsonify({'message': 'No data available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
