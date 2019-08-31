import time
from master import job_q, queue_manager, enqueue_job

def job_q_to_qms(job_q):
    while True:
        time.sleep(1)
        while len(job_q):
            user = job_q.pop(0)
            status = queue_manager(user)
            if status is not 'success':
                enqueue_job(user)

job_q_to_qms(job_q)
