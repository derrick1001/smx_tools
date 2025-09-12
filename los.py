#!/usr/local/bin/python3.13

from sys import argv

from calix.e9 import CalixE9
from calix.e_mail import email


if __name__ == "__main__":
    e9 = CalixE9(argv[1], argv[2])
    los = e9.loss_of_signal()
    ports = {port: e9.description(port) for port in los}
    for port, description in ports.items():
        email(
            f"PON Loss of signal on {e9.name}",
            f"{port}__{description}",
        )
