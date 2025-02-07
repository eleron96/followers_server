cd /root
tar xzvf linkedin_project_files.tar.gz
docker build -t linkedin_project:latest .
docker stop linkedin_project_container || true
docker rm linkedin_project_container || true
docker run --name linkedin_project_container -d --restart always --shm-size=2g -p 8090:8090 --env-file .env linkedin_project:latest
