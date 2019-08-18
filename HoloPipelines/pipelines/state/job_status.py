import logging
from datetime import datetime


# TODO: Refactor (or remove, if we only do the logging to file?)
from pipelines.clients.http import send_post_to_status

status = {
    "j0": {"status": "segment", "timestamp": "2019-08-05 14:09:19"},
    "j1": {
        "status": "segment",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    },
}

# TODO: Moved from compJobStatus. A bit ugly to have this here, but ideally we can get rid of the self-POSTing altogether
def post_status_update(job_ID, job_status):
    data = {job_ID: {"status": job_status, "timestamp": str(datetime.now())}}
    response = send_post_to_status(data)
    return_code = response.status_code
    logging.debug("return code: " + str(return_code))