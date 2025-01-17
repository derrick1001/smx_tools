from time import sleep

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": '10.20.5.51',
    "username": "sysadmin",
    "password": "Thesearethetimes!",
    "fast_cli": False,
}
cnct = ConnectHandler(**device)
cnct.send_command_timing("configure")
output = cnct.send_command_timing("copy running-config startup-config")


fn1 = 'n1'
fw2 = 'w2'
fs3 = 's3'
fxw2 = 'xw2'
a = range(1, 12)
port = 
