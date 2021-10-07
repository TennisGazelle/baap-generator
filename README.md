# BAAP-Generator

Flask Microservice that can generate BAAP workdirs from a predefined config.yaml file or simply validate them.

ENV | URL
--- | ---
PROD | https://baap-workdir-generator-auahkugdnq-uw.a.run.app
LOCAL | http://localhost:5000

## Quickstart

    python3 -m pip install -r requirements.txt
    python3 main.py

## Docker Run


## Endpoints

### `/` (GET)
Health Check
Test:

    curl -XGET localhost:5000

Returns:

    <h1>Hi there!!!</h1>

### `/generate` (POST)
Expects: YAML file in POST payload
Test:

    curl -XPOST localhost:5000/generate

Test (with file):
    
    curl -XPOST localhost:5000/generate -d ‘@$(pwd)/test/config.yaml’  -o response.zip
    curl -XPOST localhost:5000/generate -d ‘@$(pwd)/test/badconfig.yaml’  -o response.zip
