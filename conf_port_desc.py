from argparse import ArgumentParser

from typing import Generator
from time import time
from calix.e9 import CalixE9
from calix.axos_e9 import burnett

# NOTE: Change fiber_range function to return a list and use zip() to iterate over it instead

parser = ArgumentParser(description="A script for setting the port descriptions with the correct fibers on E9-2 cards")

parser.add_argument("-n", "--dryrun", action="store_true", help="Display what will be configured on the device, no configuration is changed")
args = parser.parse_args()


e9 = CalixE9(burnett)
params = [(e9.pon_range(3, "1", "11-16", extend=e9.pon_range(3, "2", "1-3")), "n2", e9.fiber_range(97, 114))]


def dry_run(ports: list, feeder: str, fibers: Generator):
    try:
        for p in ports:
            print(f"{p} -> {feeder},{next(fibers)}-{next(fibers)}")
    except StopIteration:
        print("No more fibers")


def config(ports: list, feeder: str, fibers: Generator):
    e9.connection.send_command_timing("configure")
    for p in ports:
        try:
            cmds = [
                f"interface pon {p}\ndescription {feeder},{next(fibers)}-{next(fibers)}"
            ]
            e9.connection.send_command(cmds[0])
        except StopIteration:
            print("No more fibers")


if __name__ == "__main__":
    start = time()
    if args.dryrun:
        for ports, feeder, fibers in params:
            dry_run(ports, feeder, fibers)
    else:
        for ports, feeder, fibers in params:
            config(ports, feeder, fibers)
    end = time()
    print(f"\nFinished in {end - start:.2f} seconds")
