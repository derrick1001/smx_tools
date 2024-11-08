from crayon import c_BLUE, c_WHITE


# NOTE: Returns the shelf, slot, and port for PON interface
def ssp():
    shelf = input(f"{c_BLUE}Shelf: {c_WHITE}")
    slot = input(f"{c_BLUE}Slot: {c_WHITE}")
    port = input(f"{c_BLUE}Port: {c_WHITE}")
    return shelf, slot, port
