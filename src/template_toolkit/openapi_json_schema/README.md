# Istio OpenAPI JSON Schema
[![Istio](https://img.shields.io/badge/Istio-1.9.2-blue)](https://github.com/istio/istio/tree/1.9.2)
[![Istio API](https://img.shields.io/badge/Istio_API-1.9.2-blue)](https://github.com/istio/api/tree/1.9.2)

## Generate Kubernetes JSON Schema


## Generate Istio JSON Schema
The [istio/api](https://github.com/istio/api) provides build environment through [docker](https://docs.docker.com/get-docker/).
After docker installed, you can build Istio OpenAPI JSON Schema by following commands:

```shell
cd isito_json_schema
git clone https://www.github.com/istio/api istio-api
cd istio-api
make
```

Then run extract script to aggregate json schema files:

```shell
cd ..
python extract_json_schema.py istio-api .
```