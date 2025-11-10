from calix.e9 import CalixE9

e9 = CalixE9("10.20.15.51", "United-Clay-E9-1")

feeder = "xe4"
ports = e9.pon_range("5", "1", "25-31", odd=True)
fibers = e9.fiber_range(67, 75)


def dry_run():
    try:
        for p in ports:
            print(f"{p} -> {feeder},{next(fibers)}-{next(fibers)}")
    except StopIteration:
        print("No more fibers")


def descriptions():
    desc = [f"{p} -> {e9.description(p, 'pon')}" for p in ports]
    return desc


def main():
    e9.connection.send_command_timing("configure")
    for p in ports:
        try:
            cmds = [
                f"interface pon {p}\ndescription {feeder},{next(fibers)}-{next(fibers)}"
            ]
            e9.connection.send_command_timing(cmds[0])
        except StopIteration:
            print("No more fibers")


if __name__ == "__main__":
    choice = input("Dry run?: ")
    if choice == "y":
        dry_run()
    elif choice == "n":
        main()
        desc = descriptions()
        for description in desc:
            print(description)
    else:
        print("Please use 'y' or 'n'")
