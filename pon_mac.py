#!/usr/local/bin/python3.13

from sys import argv
from time import sleep
from os import system

from calix.ssp import ssp
from calix.e9 import CalixE9
from fibers import ROSE

shelf, slot, port = ssp()

calix = CalixE9(argv[1], argv[2])

if __name__ == "__main__":
    while True:
        subs, mod_len = calix.light(f"{shelf}/{slot}/xp{port}")
        with open("light.txt", "w") as f:
            f.write(f"{mod_len}\n")
            for sub in subs:
                f.write(sub)
        system("clear")
        with open("light.txt", "r") as f:
            lines = f.read()
            print(lines)
        system("rm light.txt")
        print(f"{ROSE}Refreshing" + ".", end="\r")
        sleep(1)
        print(f"{ROSE}Refreshing" + "..", end="\r")
        sleep(1)
        print(f"{ROSE}Refreshing" + "...", end="\r")
        sleep(1)
