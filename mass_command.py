from time import sleep

from netmiko import ConnectHandler

ip_list = [
    "10.20.7.51",
    "10.20.11.51",
    "10.20.17.51",
    "10.20.4.51",
    "10.20.24.51",
    "10.20.12.51",
    "10.20.25.51",
    "10.20.16.51",
    "10.20.18.51",
    "10.20.1.51",
    "10.20.3.51",
    "10.20.5.51",
    "10.20.99.51",
    "10.20.27.51",
]
for ip in ip_list:
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "sysadmin",
        "password": "Thesearethetimes!",
        "fast_cli": False,
    }
    cnct = ConnectHandler(**device)
    cnct.send_command_timing("configure")
    cnct.send_command_timing("gpon-behavior pon-loss-behavior missing-only")
    cnct.send_command_timing("exit")
    output = cnct.send_command_timing("copy running-config startup-config")
    print(output)
    sleep(1)
    print("Disconnecting...")
    cnct.disconnect()
    sleep(3)
