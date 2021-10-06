build_docker: Dockerfile
	docker build -t baap-generator:latest .

run_docker: Dockerfile
	docker run -p 5000:5000 baap-generator:latest