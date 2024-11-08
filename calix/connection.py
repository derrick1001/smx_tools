from netmiko import ConnectHandler
from sys import argv


# NOTE: Returns connection object
def calix_e9():
    """
    *************************
    This function sets up a
    common ssh connection to
    the device it was called with.

    It returns the connection
    object that you can call
    in the script.
    *************************
    """
    device = {
        "device_type": "cisco_ios",
        "host": f"{argv[1]}",
        "username": "sysadmin",
        "password": "Thesearethetimes!",
        "fast_cli": False,
    }
    return ConnectHandler(**device)
