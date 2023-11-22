# File Security REST Scanner

## A simple REST server to leverage the Trend Micro Vision One File Security SDK.

This uses FastAPI to provide a simple asynchronous REST implementation of the File Security scanner. It has a single endpoint, "/scan". It also has API reference pages located @ "/docs" or "/redoc".

**WARNING**: This does not have authentication & authorization built into the REST endpoint. It is highly advised to not make it public facing.

## Build Image

To build the Docker image, use the following command:

```bash
docker build --build-arg PORT=<port> --build-arg REGION=<region> -t <your_image_name> .
```

PORT is an optional build argument. Default is 8000

REGION is a mandatory build argument. Below is a list of valid regions.
- us-1
- in-1
- de-1
- sg-1
- au-1
- jp-1
- gb-1
- ca-1

*Please ensure you are providing the region that is associated with the API key that will be passed to the container as an environment variable.*

To run a the container
```bash
docker run -e V1_API_KEY=<key> -p <HOST_PORT>:<CONTAINER_PORT> <your_image_name>
```
