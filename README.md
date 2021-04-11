# geoService
A small service to help you with your ignorance, made with grpc and python

## Start Docker:

```bash
docker-compose up --build -d
 ```
 
 ## Build proto files
 
The proto files are already generated, if geoService.proto is modifyed these files need to be re generated

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. geoService.proto --experimental_allow_proto3_optional
 ```
