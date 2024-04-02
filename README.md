# File Security REST Scanner

## A simple REST server to leverage the Trend Micro Vision One File Security SDK.
File Security Documentation: https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-file-security

Golang SDK Github repo: https://github.com/trendmicro/tm-v1-fs-golang-sdk

This is a simple REST implementation of the File Security scanner. It has a single endpoint, "/scan".
It accepts a multipart form upload to "file", and can also accept "tags" query parameter which is a comma-seperated string. ie ?tags=dev,east
**WARNING**: This does not have authentication & authorization built into the REST endpoint. It is highly advised to not make it public facing.

## Build Image

To build the Docker image, use the following command:

```bash
docker build --build-arg PORT=<port> --build-arg REGION=<region> -t <your_image_name> .
```

REGION is a mandatory build argument. Below is a list of valid regions.
- ap-northeast-1
- ap-south-1
- ap-southeast-1
- ap-southeast-2
- ca-central-1
- eu-central-1
- eu-west-2
- us-east-1
- us-east-2


*Please ensure you are providing the region that is associated with the API key that will be passed to the container as an environment variable.*

To run a the container
```bash
docker run -e V1_KEY=<key> -p <HOST_PORT>:<CONTAINER_PORT> <your_image_name>
```
