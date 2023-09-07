# HoloPipelines 2023<a href="https://dev.azure.com/Holo-Repository/OrganSegmentation/_build/results?buildId=70&view=results"><img src="https://dev.azure.com/MSGOSHHOLO/HoloRepository/_apis/build/status/HoloRepository-Core?branchName=dev&jobName=HoloPipelines%20-%20Core" alt="HoloPipelines core build status" align="right" /></a>

This is an update of the 2019 version of HoloPipelines. The main changes are:

-  The mesh generation method has been upgraded to use the method from [HoloRepository 2020](https://github.com/AppertaFoundation/HoloRepository-2020/tree/master/HoloRepository2020Viewer)'s HoloPipelines  
-  The write to glTF file method has been upgraded to also use the methods from HoloRepository 2020's [glb file writer](https://github.com/AppertaFoundation/HoloRepository-2020/blob/master/HoloRepository2020Viewer/core/adapters/glb_file.py), with some minor changes to fix the model's pivot issue when displayed in Unity
- The abdominal pipeline has been updated to use [MONAI model](https://monai.io/model-zoo.html), and the nifitynet.py file is updated to reflect the update

Below is the readme from the 2019 version of HoloPipelines

## Architecture

The HoloPipelines themselves are a cloud-based application developed with Python. The
code implements a Pipes-and-Filters pattern and is kept modular. Different modules can
be pieced together to reflect different workflows, and thereby provide different
pipelines.

The modules that form a pipeline can perform different tasks:

- The first module in the chain is responsible for listening to incoming `POST` requests
  and then actively pulling the input data from the PACS.
- Intermediate modules perform various pre- or post-processing tasks such as rescaling,
  cropping, or filtering.
- Special adapter modules are used to call the pre-trained NN models, which are being
  deployed as separate containers and accessed via HTTP calls.
- The last module is responsible for sending the result off to the HoloStorage Accessor.

## Job-specific working areas

When jobs are triggered, they will automatically create and maintain their local working
 area in `<app-root-dir>/__jobs__/<job-id>`.
 
This directory contains subdirectories for `input`, `output` and `temp` data.
Furthermore, a `job.log` file contains the job-specific logs and a `job.state` file
contains the current state. The automatic garbage collection usually deletes all binary
files, but keeps logs around by default. For production deployment, this should be
changed (or the `__finished_jobs__` directory should be emptied regularly). If you want
to keep all files or change other settings, refer to the
[configuration](#configuration).

## How to add new pipelines

Adding a new pipeline is fairly easy; however, it currently does include some manual
steps. The required steps vary depending on the specific use case, and on the type of
pipeline. Currently, we have three types of pipelines, that differ in the way they
perform automatic segmentation:
* Algorithmic segmentation using low-level libraries (e.g. `bone_segmentation` pipeline)
* Existing implementations of algorithmic segmentation (e.g. `lung_segmentation`
  pipeline)
* Automatic segmentation using external neural networks (e.g.
  `abdominal_organs_segmentation` pipeline)

In each case, you will have to create a new pipeline module in `./core/pipelines/`. It
should expose a `run` function (refer to existing pipelines for the signature) and be
directly invokable for testing purposes (via `__main__`). You should then also add your
pipeline to the `./core/pipelines.json` to document the pipeline's specification and
make it visible for external clients. By adding it here, it will show up as an option
for clients to run. The `job_controller` will then automatically load the new pipeline
without any code changes.

In the pipeline itself, you should only a) call other components to perform actions and
b) update the job status. Pipelines are pieced together from other components, which are
really the core building blocks of the system. For the pre- and postprocessing steps, it
is encouraged to reuse existing `tasks`, `services`, `adapters`, `wrappers` and
`clients`. If your pipeline requires other functionality, try to extract it to a
reusable components.

If you encounter an error in your component, it's okay to just raise an Error or
Exception. The `job_controller` which runs the pipelines will catch it and show an error
message. The garbage collection will clean up after you.

If you want to integrate an existing implementation in python code or need to call an
external program, write a wrapper.


## Development

### Requirements:

Python 3.7 or above

### Dependencies and installation:

Dependencies can be installed by using pip command as follow

```
pip install -r requirements.txt
```

Some dependencies are not available through pip, they are listed below with their
installation instructions

These 2 dependencies can be installed using Node.js package manager. Please make sure to
have the latest version of npm installed.

**obj2gltf** https://github.com/AnalyticalGraphicsInc/OBJ2GLTF

```
npm install -g obj2gltf
```

### Local development

Just start the Flask server locally. It will automatically run in debug mode, including
features like live reloading, extensive debug statements, etc.

```shell
python server.py
```

### Configuration

The application is configured through environment variables. For local development, the
`.env` file will automatically be read and the variables will be made available (Note:
`.env` file is included with test values in VCS in this case as it doesn't contain any
secrets).

In production environments, all variables in `.env` should be set by the CD workflow.

## Testing

Testing is done using pytest:

```
pip install pytest pytest-mock pytest-cov
```

Execute tests by running the following command in `HoloPipelines` directory:

```
pytest --cov
```

### Manual testing with Postman

The file `tests/HoloPipelines.postman_collection.json` contains a Postman collection
 that can be used to try out the API endpoints manually. The typical workflow is to
 trigger one of the pipelines by starting a new job (`POST /jobs`) and then tracking it
 via the `/state` and `/log` endpoints.

 Note that to test the end-to-end flow, the HoloStorageAccessor and any relevant neural
 network containers should be running as well. You can use the `docker-compose` file in
 the project root directory to help start the different sub-systems.

 ## Build and deployment

### Building and running the docker image

```shell
docker build . -t holopipelines-core
docker run --rm -p 3100:3100 --env-file .env holopipelines-core:latest
```

## API specification

```
POST /job
    Starts a new job.

GET /pipelines
    Returns a JSON list of available pipelines

GET /job/<job_id>/state
    Returns the state of a job with specific ID

GET /job/<job_id>/log
    Returns the complete log of a job with specific ID
```
