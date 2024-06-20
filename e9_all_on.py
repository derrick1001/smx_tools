#!/usr/bin/python3

from netmiko import ConnectHandler


def connect():
    device = {'device_type': 'cisco_ios',
              'host':   '192.168.1.1',
              'username':   'sysadmin',
              'password':   'sysadmin',
              'fast_cli':   False,
              }

    con = ConnectHandler(**device)
    return con


def card2():
    # configure
    # interface pon x/x/x
    # no shut
    # top
    con = connect()
    for i in range(1, 17):
        for k in range(1, 3):
            cmds = ['configure', f'interface 2/{k}/xp{i}', 'no shut', 'top']
            con.send_command_timing(cmds)
    con.disconnect()


def card3():
    con = connect()
    for i in range(1, 17):
        for k in range(1, 3):
            cmds = ['configure', f'interface 3/{k}/xp{i}', 'no shut', 'top']
            con.send_command_timing(cmds)
    con.disconnect()


def card4():
    con = connect()
    for i in range(1, 17):
        for k in range(1, 3):
            cmds = ['configure', f'interface 4/{k}/xp{i}', 'no shut', 'top']
            con.send_command_timing(cmds)
    con.disconnect()


def card5():
    con = connect()
    for i in range(1, 17):
        for k in range(1, 3):
            cmds = ['configure', f'interface 5/{k}/xp{i}', 'no shut', 'top']
            con.send_command_timing(cmds)
    con.disconnect()

# card2()
# card3()
# card4()
# card5()
