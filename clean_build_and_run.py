from os import system

system('docker compose down')
system('docker compose down --volumes')
system('docker system prune --all --volumes --force')
system('docker compose up --build -d')
system('docker compose down')
system('docker compose up --build -d')
