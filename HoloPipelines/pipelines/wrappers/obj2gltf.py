import subprocess
import pathlib
from shutil import move
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
new_cwd = str(pathlib.Path(str(os.path.dirname(os.path.realpath(__file__)))))

success = True


def call_obj2gltf(obj_input_path, glb_output_path):
    # TODO: Paths vs strings
    obj_input_path = str(pathlib.Path(obj_input_path))
    obj2gltf_command = f"obj2gltf --binary --input {obj_input_path} --output {glb_output_path}"
    completed_process = subprocess.run(obj2gltf_command)
    if completed_process.returncode == 0:
        logging.info("obj2glb: conversion complete")
    else:
        sys.exit("obj2glb: conversion failed")

    logging.info("obj2glb: done")
    return glb_output_path
