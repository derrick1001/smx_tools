from calix.ssp import ssp

shelf, slot, port = ssp()


def get_ranges(shelf: str, slot: str, port: str) -> tuple(range, range):
    if slot == "":
        slot_range = range(1, 3)
    if "-" in port:
        port_range = range(port.split("-")[0], port.split("-")[1] + 1)
    elif port == "":
        port_range = range(1, 17)
    return slot_range, port_range


def main():
    pass


if __name__ == "__main__":
    # cnct = calix_e9()
    slots, ports = get_ranges()
    for slot in slots:
        for port in ports:
            print(f"{shelf}{slot}/xp{port}")
