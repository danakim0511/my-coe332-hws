from jobs import get_job_by_id, update_job_status, q, rd, res
import json

@q.worker
def do_work(jobid):
    """
    Calls the analyze function to do work based on parameters
    """
    try:
        update_job_status(jobid, 'in progress')
        # retrieves the data
        job_data = get_job_by_id(jobid)
    
        start_date = job_data['start_date']    # modify again
        end_date = job_data['end_date']

        analysis_results = analyze(start_date, end_date)

        res.set(jobid, json.dumps(analysis_results))
        
        update_job_status(jobid, 'complete')

    except ValueError:
        update_job_status(jobid, 'failed')
        print(f"Invalid jobid provided.")
        
def analyze(start_date, end_date):
    """
    Performs analysis to... """
    fqhc_with_parameters = [json.loads(rd.get(key)) for key in rd.keys() if start_date <= json.loads(rd.get(key))['site_postal_code'] <= end_date]
    
    subprogram_offered = 0  # Initialize counter
    for health_center in fqhc_with_parameters:
        if health_center.get('health_care_for_the_homeless_hrsa_grant_subprogram_indicator') == 'Y':
            subprogram_offered += 1
    return {"Amount of subprograms offered within a certain postal code:": subprogram_offered} 
    
# Enqueue a job with RQ
job = q.enqueue(do_work, jobid=123)  # Assuming 123 is the jobid
