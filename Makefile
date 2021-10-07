build_docker: Dockerfile
	docker build -t baap-generator:latest .

run_docker: Dockerfile
	docker run -p 5000:5000 baap-generator:latest

local_run: src/main.py
	python3 src/main.py

test: response.zip
	unzip -d tempdir -o response.zip