docker-compose down
docker-compose down --volumes
docker system prune --all --volumes --force
docker-compose up --build -d
docker-compose down
docker-compose up --build -d
