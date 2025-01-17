#!/usr/bin/python3

from sys import argv

from calix.affected_decorator import affected_decorator
from crayon import c_BLUE, c_CYAN, c_WHITE

onts = list(input(f"{c_BLUE}ONT_IDS{c_WHITE}: ").split())


@affected_decorator
def main(e9=argv[2]):
    return onts


if __name__ == "__main__":
    subs = main(e9=argv[2])
    for sub in subs:
        print(sub)
    q = input(f"{c_CYAN}Press any key to exit...")
    if q is None:
        exit()
