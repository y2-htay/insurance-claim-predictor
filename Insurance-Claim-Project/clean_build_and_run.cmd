docker-compose down --volumes
docker system prune --all --volumes --force
docker-compose up --build -d