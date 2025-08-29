from calix.ssp import ssp

shelf, slot, port = ssp()


def get_ranges(slot: str, port: str) -> tuple[range, range]:
    if slot == "":
        slot_range = range(1, 3)
    else:
        slot_range = slot
    if "-" in port:
        port_range = range(int(port.split("-")[0]), int(port.split("-")[1]) + 1)
    else:
        port_range = range(1, 17)
    return slot_range, port_range


if __name__ == "__main__":
    # cnct = calix_e9()
    slots, ports = get_ranges(slot, port)
    ranges = [f"{shelf}/{slot}/xp{port}" for slot in slots for port in ports]
    for port in ranges:
        print(port)
