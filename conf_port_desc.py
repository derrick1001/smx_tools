from argparse import ArgumentParser

from typing import Generator
from time import time
from calix.e9 import CalixE9
from calix.axos_e9 import device


parser = ArgumentParser(description="A script for setting the port descriptions with the correct fibers on E9-2 cards")

parser.add_argument("-n", "--dryrun", action="store_true", help="Display what will be configured on the device, no configuration is changed")
parser.add_argument("-f", "--feeder", help="Feeder name for labeling purposes")
parser.add_argument("-d", "--device", help="E9 system to run the program against")
args = parser.parse_args()


e9 = CalixE9(device(args.device))
params: tuple = [(e9.pon_range(2, "1", "1-9"), f"{args.feeder}", e9.fiber_range(1, 20))]


def dry_run(ports: list, feeder: str, fibers: Generator):
    try:
        for p in ports:
            print(f"{p} -> {feeder},{next(fibers)}-{next(fibers)}")
    except StopIteration:
        print("No more fibers")


def config(ports: list, feeder: str, fibers: Generator):
    for p in ports:
        try:
            cmds = [
                f"configure\ninterface pon {p}\ndescription {feeder},{next(fibers)}-{next(fibers)}\ntop"
            ]
            e9.connection.send_command_timing(cmds[0], last_read=.2)
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
