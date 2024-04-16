import csv, folium, uuid, os, json
from hotqueue import HotQueue
from collections import Counter
from redis import Redis
import io

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host = redis_ip, port=6379, db=0)
q = HotQueue('queue', host = redis_ip, port = 6379, db=1)
rd2 = Redis(host = redis_ip, port=6379, db=2)

def get_sites_data() -> dict:
    '''
        This function pulls the full data csv from the current directory and formats
        it into json format for use in most other functions.

        Args:
            None
        Returns:
            data (dict) : A dictionary containing the key 'sites' that contains
            a list of dictionaries of each site
    '''
    data = {}
    data['sites'] = []

    with open('SITE_HCC_FCT_DET.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['sites'].append(dict(row))

    return(data)

# JOB HANDLING

def generate_jid() -> str:
    """
      Generate a pseudo-random identifier for a job and returns it.
      
      Returns:
          randomID (str): A random job ID.
    """
    
    randomID = str(uuid.uuid4())
    return randomID

def generate_job_key(jid):
    """
      Generate the redis key from the job id to be used when storing, retrieving or updating
      a job in the database.
      
      Returns:
          jid (str): The jobID to be used for the redis key.
    """
    return '{}'.format(jid)

def instantiate_job(jid, route, status):
    """
      Create the job object description as a python dictionary. Requires the job id, route, and status.
      
      Return:
          (dict): The job object description.
    """
    return {'id': jid,
            'route': route,
            'status': status
    }

def save_job(job_key, job_dict):
    """
    Save a job object in the rd Redis database.
    """
    rd.set(job_key, json.dumps(job_dict))

def queue_job(jid):
    """
    Adds a job id to the redis queue.
    """
    q.put(jid)

def add_job(route):
    """
    Fully creates the job ID and information regarding the job. Then it
    makes the status into submitted, and saves and queues the job. It returns the
    job ID so that it can be sent to the user during the success message.
    
    Returns:
        jid (str): The job ID.
    """
    jid = generate_jid()
    job_dict = instantiate_job(jid, route, "submitted")
    save_job(jid, job_dict)
    queue_job(jid)
    
    return jid

def update_job_status(jid, status):
    """
    Update the status of job with job id `jid` to status `status`.
    """

    job = json.loads(rd.get(jid))
    if job:
        job['status'] = status
        save_job(generate_job_key(jid), job)
    else:
        raise Exception()

def list_of_jobs():
    """
    This function creates a list of jobs that is in an easily returnable state.
    
    Returns:
        jobsList (list): The list of current jobs queued by the user.
    """
    jobsList = []
    for key in rd.keys():
        jobsList.append(json.loads(rd.get(key.decode('utf-8'))))
        
    return jobsList
        
# JOB RELATED

def get_data() -> dict:
    """
    This function returns the data from Redis, but only if it exists or is empty.
    Otherwise it will return a message saying that the data does not exist.

    Returns:
        redisData (dict): The entire health care center data.
    """

    #try-except block that returns if the data doesn't exist and an error occurs because of it
    try:
        #un-seralizing the string into a dictionary
        redisData = json.loads(rd2.get('data'))
    except NameError:
        return 'The data does not exist.'
    except TypeError:
        return 'The data does not exist.'

    return redisData


def get_sites_by_state(full_data_json:dict, state:str) -> list:
    '''
        This function gets a list of all the sites in a state.

        Args:
            full_data_json (dict) : The full data json from the database
            state (str) : The name of the desired state
        Returns:
            sites (list) : A list of strings of sites
    '''

    sites = []
    for item in full_data_json['']:
        if item['Site State Abbreviation'] == state:
            sites.append(item['Site Name'][:item['Site Name'].index(" |")])

    return(sites)






