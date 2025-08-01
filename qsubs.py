#!/usr/local/bin/python3

from sys import argv

from calix.affected_decorator import affected_decorator

onts = input("ONT_IDs:").split()


@affected_decorator
def main(e9=argv[2]):
    yield onts


if __name__ == "__main__":
    subs = main(e9=argv[2])
    for sub in subs:
        print(sub)
