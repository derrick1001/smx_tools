#!/usr/bin/env python3

from sys import argv

from calix.e9 import CalixE9
from calix.axos_e9 import device


if __name__ == "__main__":
    e9 = CalixE9(device(argv[1]))
    onts = e9.get_onts(argv[2:])
    subs = (e9.get_subs(onts))
    with open('subs.txt', 'a') as f:
        for sub in subs:
            f.write(sub)
