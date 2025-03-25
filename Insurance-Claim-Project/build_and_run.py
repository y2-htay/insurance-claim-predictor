from os import system
from clean_build_and_run import clean_build_and_run


def build_and_run():
    system('docker compose down')
    system('docker compose up --build -d')


# checking if a clean build has been recommended
try:
    with open('do_clean_build.txt', 'r', encoding='utf-8') as file:
        content = file.readline().strip()
except FileNotFoundError:
    content = "0"

if content == "1":
    answer = input(
        "A clean build and run has been recommended. Do you want to perform this action? "
        "Note this will delete all existing containers and volumes!\n"
        "Please answer Y or N\n"
    )
    # run a clean build and run if the user wants and set the file to no-longer recommend it
    if answer.casefold() == "y":
        print("Running clean build and run!")
        with open('do_clean_build.txt', 'w', encoding='utf-8') as file:
            file.write("0")
        clean_build_and_run()
    else:
        build_and_run()
else:
    build_and_run()
