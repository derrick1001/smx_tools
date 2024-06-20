#!/usr/bin/python3

import requests
from sys import argv
from netmiko import ConnectHandler


# Will return a string, need to split string and make new list with acct, name, loc, em for each affected sub
def affected():
    get_affected = requests.get(f'https://10.20.7.10:18443/rest/v1/fault/export/csv/subscriber/device-name/CVEC-E9-1/instance-id/3.76637',
                                auth=('admin', 'Thesearethetimes!'), verify=False)
    r = get_affected.text.split('\r\n')
    for i in r[1:-1]:
        sp = i.split(',')
        acct = sp[0]
        name = sp[1]
        loc = ' '.join(sp[2:5])
        em = sp[-1]
        with open('test.txt', 'w') as f:
            f.write(f'{acct}\n{name}\n{loc}\n{em}\n')

        # print(f'{acct}\n{name}\n{loc}\n{em}\n')
    # email(acct, name, loc, em)


# def clr_alarm():
#    device = {'device_type': 'cisco_ios',
#              'host':   '10.20.99.51',
#              'username':   'sysadmin',
#              'password':   'Thesearethetimes!',
#              'fast_cli':   False,
#              }
#    con = ConnectHandler(**device)
#    output = con.send_command('show alarm active alarm 1')
#    instid = output.split()
#    con.send_command(f'manual shelve instance_id {instid}')
#    affected(instid[11])


def email(acct, name, loc, em):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(f'{acct}\n{name}\n{loc}\n{em}')
    msg['Subject'] = 'Affected Subs'
    msg['From'] = 'python@precision.net'
    msg['To'] = 'dishman@cvecfiber.com'

    s = smtplib.SMTP('10.20.7.31')
    s.send_message(msg)
    s.quit()


affected()
