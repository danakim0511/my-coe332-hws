from hotqueue import HotQueue
from redis import Redis
from jobs import *
import json

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host = redis_ip, port=6379, db=0)
q = HotQueue('queue', host = redis_ip, port = 6379, db=1)
rd2 = Redis(host = redis_ip, port=6379, db=2)

@q.worker
def execute_job(item: str) -> dict:
    """
    Retrieve a job id from the task queue and execute the job.
    Monitors the job to completion and updates the database accordingly.

    Args:
        Item (str): the job's id from the queue object created by jobs.py

    Returns: 
        new_job (Dict): the dictionary object of the job that was completed. 
    """

    # JOBS ID 
    current_jid = item #string, JID

    # TURN STATUS TO 'IN PROGESS'
    update_job_status(current_jid, 'in progress')

    # ACQUIRE JOB'S DICTIONARY OBJECT
    current_job = json.loads(rd.get(current_jid))
    
    # PASS THE ROUTE INTO USABLE VARIABLES
    current_route = current_job['route'] # full route, e.g., '/get_rockets_by_org-org'

    # INITIALIZING ARGS
    args = []
    
    # THIS CHECKS TO MAKE SURE IF IT HAS ANOTHER ELEMENT TO THE QUERY
    if '-' in current_route:
        args = current_route.split('-') 
        function = args[0] # the 'get_rockets_by_org'
        
        # AS SPACES AREN'T ALLOWED IN THE TERMINAL, THIS IS A WORKAROUND FOR IT
        args[1] = args[1].replace('_', ' ')
    else:
        function = current_route
    
    # EXECUTE FUNCTION IN ROUTE
    full_data = get_data()
    result = []
    
    # SETTING THE STATUS TO COMPLETED NOW SO THAT THIS LINE DOESN'T HAVE TO BE IN EVERY SINGLE IF STATEMENT
    status = 'completed'
    
    if full_data == 'The data does not exist.':
        result = 'The data does not exist, make sure to POST the data!'
        status = 'incompleted'
    else:
        if function == 'get_rockets_by_org' and len(args) == 2:
            result = get_sites_by_state(full_data, args[1])
        else: 
            status = 'incompleted' # changes to incompleted if the route doesn't exist
            result = 'Could not parse a proper function from the route provided.'
    
    # SAVE RESULT AND UPDATE STATUS TO COMPLETE
    if function != 'map-of-sites':

        rd2.set(current_jid, json.dumps(result))
        update_job_status(current_jid, status)
    else:
        rd2.set(current_jid, result)
        update_job_status(current_jid,status)
execute_job()