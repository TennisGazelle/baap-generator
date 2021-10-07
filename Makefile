build_docker: Dockerfile
	docker build -t baap-generator:latest .

run_docker: Dockerfile
	docker run -p 5000:5000 baap-generator:latest

local_run: src/main.py
	python3 src/main.py

test: response.zip
	curl -XPOST localhost:5000/generate -d ‘@$(pwd)/test/config.yaml’  -o response.zip
	unzip -d tempdir -o response.zip