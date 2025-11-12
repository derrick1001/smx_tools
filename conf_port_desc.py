from typing import Generator
import threading
from calix.e9 import CalixE9

e9 = CalixE9("10.20.10.51", "Dustin-E9-1")


def dry_run(ports: list, feeder: str, fibers: Generator):
    try:
        for p in ports:
            print(f"{p} -> {feeder},{next(fibers)}-{next(fibers)}")
    except StopIteration:
        print("No more fibers")


def descriptions(ports: list):
    desc = [f"{p} -> {e9.description(p, 'pon')}" for p in ports]
    return desc


def config(ports: list, feeder: str, fibers: Generator):
    e9.connection.send_command_timing("configure")
    for p in ports:
        try:
            cmds = [
                f"interface pon {p}\ndescription {feeder},{next(fibers)}-{next(fibers)}"
            ]
            e9.connection.send_command_timing(cmds[0])
        except StopIteration:
            print("No more fibers")


def thread1(dry=True):
    ports = e9.pon_range("2", "1", "1-9")
    feeder = "e3"
    fibers = e9.fiber_range(1, 19)
    if dry is True:
        dry_run(ports, feeder, fibers)
    elif dry is False:
        config(ports, feeder, fibers)


def thread2(dry=True):
    ports = e9.pon_range("2", "1", "10-16")
    more_ports = e9.pon_range("2", "2", "1-13")
    ports.extend(more_ports)
    feeder = "s1"
    fibers = e9.fiber_range(1, 45)
    if dry is True:
        dry_run(ports, feeder, fibers)
    elif dry is False:
        config(ports, feeder, fibers)


def thread3(dry=True):
    ports = e9.pon_range("2", "2", "13-18")
    feeder = "w1"
    fibers = e9.fiber_range(1, 13)
    if dry is True:
        dry_run(ports, feeder, fibers)
    elif dry is False:
        config(ports, feeder, fibers)


def thread4(dry=True):
    ports = e9.pon_range("2", "2", "13-18")
    feeder = "w1"
    fibers = e9.fiber_range(1, 13)
    if dry is True:
        dry_run(ports, feeder, fibers)
    elif dry is False:
        config(ports, feeder, fibers)


if __name__ == "__main__":
    choice = input("Dry run?: ")
    if choice == "y":
        thread1()
        thread2()
    elif choice == "n":
        t1 = threading.Thread(target=thread1, kwargs={"dry": False})
        t2 = threading.Thread(target=thread2, kwargs={"dry": False})
        t1.start()
        t2.start()
    else:
        print("Please use 'y' or 'n'")
