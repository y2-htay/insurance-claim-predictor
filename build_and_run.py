from os import system

system('docker compose down')

system('docker compose up --build -d')