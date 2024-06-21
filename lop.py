#!/usr/bin/python3

import requests
from sys import argv
from netmiko import ConnectHandler

# Add another call to get fiber information from the pon port


def affected(instid, port, e9):
    get_affected = requests.get(f'https://10.20.7.10:18443/rest/v1/fault/export/csv/subscriber/device-name/{e9}/instance-id/{instid}',
                                auth=('admin', 'Thesearethetimes!'), verify=False)
    r = get_affected.text.split('\r\n')
    for i in r[1:-1]:
        sp = i.split(',')
        acct = sp[0]
        name = sp[1]
        loc = ' '.join(sp[2:5])
        em = sp[-1]
        with open(f'{e9}_{instid}.txt', 'a') as f:
            f.write(f'{acct}\n{name}\n{loc}\n{em}\n\n')
    email(acct, name, loc, em, port, e9, instid)


def clr_alarm():
    device = {'device_type': 'cisco_ios',
              'host':   '10.20.0.51',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    con = ConnectHandler(**device)
    output = con.send_command('show alarm active alarm 1')
    data = output.split()
    instid = data[11]
    gport = data[17].split("'")
    port = gport[1]
    e9 = data[18].rstrip('#')
    # con.send_command(f'manual shelve instance-id {instid}')
    con.disconnect()
    affected(instid, port, e9)


def email(acct, name, loc, em, port, e9, instid):
    import smtplib
    from email.message import EmailMessage
    with open(f'{e9}_{instid}.txt', 'r') as f:
        msg = EmailMessage()
        msg.set_content(f.read())
    msg['Subject'] = f'Affected Subs {e9} on port {port}'
    msg['From'] = 'python@precision.net'
    msg['To'] = 'dishman@cvecfiber.com'
    # msg['Cc'] = 'jailey@cvecfiber.com'

    s = smtplib.SMTP('10.20.7.31')
    s.send_message(msg)
    s.quit()


clr_alarm()
