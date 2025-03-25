import stat
from os import system, chmod
import shutil

PATHS = ["backend/backend_app/migrations", "frontend/frontend_app/migrations"]


def change_perms(func, path, _):
    chmod(path, stat.S_IWRITE)
    func(path)


def delete_migrations():
    for path in PATHS:
        try:
            shutil.rmtree(path, onerror=change_perms)
        except FileNotFoundError:
            continue
    print("Migrations deleted successfully!")


def clean_build_and_run():
    system('docker compose down')
    system('docker compose down --volumes')
    system('docker system prune --all --volumes --force')
    delete_migrations()
    system('docker compose up --build -d')
    system('docker compose down')
    system('docker compose up --build -d')


if __name__ == "__main__":
    clean_build_and_run()
