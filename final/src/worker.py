from jobs import get_job_by_id, update_job_status, q, rd, res
import json

def do_work():
    """
    Worker function to process jobs from the queue.
    """
    while True:
        # Pop a jobid from the queue
        jobid = q.get()
        if jobid is None:
            break  # Exit the loop if no more jobs
        try:
            update_job_status(jobid, 'in progress')
            # Retrieve job data
            job_data = get_job_by_id(jobid)
            start_date = job_data['start_date']
            end_date = job_data['end_date']
            # Perform analysis
            analysis_results = analyze(start_date, end_date)
            # Save analysis results
            res.set(jobid, json.dumps(analysis_results))
            # Update job status to complete
            update_job_status(jobid, 'complete')
        except Exception as e:
            update_job_status(jobid, 'failed')
            print(f"An error occurred while processing job {jobid}: {e}")

def analyze(start_date, end_date):
    """
    Performs analysis...
    """
    fqhc_with_parameters = [json.loads(rd.get(key)) for key in rd.keys() if start_date <= json.loads(rd.get(key))['site_postal_code'] <= end_date]
    subprogram_offered = 0  # Initialize counter
    for health_center in fqhc_with_parameters:
        if health_center.get('health_care_for_the_homeless_hrsa_grant_subprogram_indicator') == 'Y':
            subprogram_offered += 1
    return {"Amount of subprograms offered within a certain postal code:": subprogram_offered}

# Start the worker
if __name__ == "__main__":
    do_work()
