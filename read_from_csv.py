import re
from time import sleep

from calix.rmont import rmont
from calix.rmsub import rmsub


def rem_sub(csv_file: str):
    with open(csv_file, "r") as f:
        lines = f.read()
        pattern = re.compile("17000\\d{5}")
        for match in pattern.finditer(lines):
            d = rmsub(str(match.group()))
            if d == 200:
                print("Account removed successfully!!")
            elif d == 404:
                print(f"Account {match.group()} id not exist, skipping")
                continue


def rem_ont(dtc: dict):
    for k, v in dtc.items():
        rm = rmont(k, v)
        if rm == 200:
            print("ONT removed successfully!!")
        elif rm == 404:
            print(f"ONT {k} did not exist, skipping")
            continue


if __name__ == "__main__":
    # dct = {k: v for k, v in zip(id, e9)}
    rem_ont(dct)
    print("Removing subs...\n")
    sleep(3)
    rem_sub("fiber_dnp.csv")
