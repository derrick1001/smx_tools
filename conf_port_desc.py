from typing import Generator
from time import time
from calix.e9 import CalixE9

e9 = CalixE9("10.20.8.51", "Hanna-E9-1")
params = [(e9.pon_range("2", "2", "14-29"), "w3", e9.fiber_range(1, 34))]


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
            e9.connection.send_command_timing(cmds[0], read_timeout=60)
        except StopIteration:
            print("No more fibers")


if __name__ == "__main__":
    start = time()
    choice = input("Dry run?: ")
    if choice == "y":
        for ports, feeder, fibers in params:
            dry_run(ports, feeder, fibers)
    elif choice == "n":
        for ports, feeder, fibers in params:
            config(ports, feeder, fibers)
    else:
        print("Please use 'y' or 'n'")
    end = time()
    print(f"Finished in {end - start:.2f} seconds")
