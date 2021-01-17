import os
import subprocess  # noqa

import getch
from clean_user_data import cleaning
from get_prediction import create_plots


headline = """
############################################################
#                    Sentiment analysis                    #
#                       with tweets                        #
############################################################ """  # noqa


def get_twits(name):
    os.mkdir(f"../Users/{name}")
    comand = f"twint -u {name} --since 2020-01-01 --until 2020-12-31 -o ../Users/{name}/{name}.csv --csv"
    process = subprocess.Popen(  # noqa
        comand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    if error:
        raise ValueError


print(headline)  # noqa
if not os.path.exists(r"../Users"):
    os.mkdir(r"../Users")
while True:
    while True:
        name = input("Enter username:")  # noqa

        try:
            path = f"../Users/{name}"
            if os.path.exists(f"{path}/{name}.csv"):
                print(f"\nPlots already exist! Please, check {path}")  # noqa
                break
            get_twits(name)
        except ValueError:
            print("Wrong username! Please try again!")  # noqa
            continue
        else:
            cleaning(name)
            create_plots(name)
            print("\nAll plots was created!")  # noqa
            break

    print("\nPress <Esc> to exit or any other key to continue.")  # noqa
    key = ord(getch.getch())
    if key == 27:  # ESC
        break
