import os
import sys
from icecream import ic


def print_code(file: str, from_line: int, to_line: int):
    if os.path.isfile(file):
        if to_line < from_line:
            to_line += from_line - 1
        if from_line > 40:
            answer = input(">")
            if answer != "":
                sys.exit(0)

        print("--------------------------------------------------------------------")
        ic(file)
        print("--------------------------------------------------------------------")
        with open(file, "r", encoding="utf-8") as file:
            data = file.read().split("\n")
            for i in range(from_line - 1, to_line):
                print(i, "\t", data[i])
        print("")
        answer = input(">")
        if answer != "":
            sys.exit(0)
