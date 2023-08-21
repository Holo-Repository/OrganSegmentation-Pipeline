"""
This module contains functionality related to communicating with pre-trained neural
networks built with Niftynet and packaged for HoloPipelines usage as described in
the /models/README. Models have a well-defined API and this module is the counterpart
that calls this API and thus integrates it with the pipelines.
"""

import requests

from config import NIFTYNET_MODEL_TIMEOUT
from jobs.jobs_io import (
    get_logger_for_job,
)
#Enables logging in for function in this file:
#Example:
#logger = get_logger_for_job(job_id)
#logger.info("info")


def call_model(
    model_host: str, model_port: int, input_file_path: str, output_file_path: str, job_id: str
) -> None:
    """
    Calls a pre-trained Niftynet model. The model has to be running and expose the
    /model endpoint, as documented in the /models directory.
    """
    logger = get_logger_for_job(job_id)
    # First is for deploy remotely, second is for local testing
    model_endpoint = f"{model_host}/model"        
    # model_endpoint = f"http://172.17.0.2:5000/model"

    with open(input_file_path, "rb") as input_fie:
        files = {"file": input_fie}
        response = requests.post(
            model_endpoint, files=files, timeout=3000
        )
        logger.info(f"model status code: {response.status_code}")
        if response.status_code != 200:
            raise Exception(f"HTTP response {response.status_code}: {response.content}")
    with open(output_file_path, "wb") as output_file:
        output_file.write(response.content)
