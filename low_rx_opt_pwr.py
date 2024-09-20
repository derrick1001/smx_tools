#!/usr/bin/python3

from requests import get
from datetime import timedelta
from sys import argv, path
from netmiko import ConnectHandler

# Notes
# call main with diff alarm tables?


def get_cmds():
    # Set dictionary variable for the arguments to ConnectHandler
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }

    with ConnectHandler(**device) as cnct:
        # Send commands down the ssh channel
        alrm_tbl = cnct.send_command_timing(
            'show alarm active | include low-rx-opt-pwr-[fn]e')
        cnct.send_command_timing('configure')
        hostname = cnct.send_command_timing('show full-configuration hostname')

    # Sometimes you get the prompt back as a string in your data, we split here on \n and the [0] index is the hostname
    strip_prompt = hostname.split('\n')
    e9 = strip_prompt[0].lstrip('hostname ')
    return e9, alrm_tbl


def cx_detail(e9, tbl):

    def ont_detail(e9, port):
        ont = get(f'https://10.20.7.10:18443/rest/v1/performance/device/{e9}/ont/{port}/status',
                  auth=('admin', 'Thesearethetimes!'),
                  verify=False)
        r = ont.json()
        sn = r.get('serial-number')
        ut = int(r.get('up-time'))
        td = timedelta(seconds=ut)
        td_str = str(td)
        fmt_ut = td_str.split(':')
        h, m, s = fmt_ut
        lpon = r.get('linked-pon')
        lr = r.get('latest-restart-reason')
        up_rx = r.get('ne-opt-signal-level')
        dn_rx = r.get('opt-signal-level')
        up_ber = r.get('us-sdber-rate')
        dn_ber = r.get('ds-sdber-rate')
        rlen = int(r.get('range-length')) / 1000
        return f'\nONT: {port}\nUS-Light: \t{up_rx}\nDS-Light: \t{dn_rx}\nUS-BER: \t{up_ber}\nDS-BER: \t{dn_ber}\nRange: {rlen}km\nSN: {sn}\nPON-Port: {lpon}\nUptime: {h}hours {m}minutes {s}seconds\nLast-Restart: {lr}\n'

    def affected(instid, port, e9):
        get_affected = get(f'https://10.20.7.10:18443/rest/v1/fault/export/csv/subscriber/device-name/{e9}/instance-id/{instid}',
                           auth=('admin', 'Thesearethetimes!'), verify=False)
        r = get_affected.text.split('\r\n')
        for i in r[1:-1]:
            sp = i.split(',')
            acct = sp[0]
            name = sp[1]
            loc = ' '.join(sp[2:5])
            em = sp[-1]
        return f'{acct}\n{name}\n{loc}\n{em}'

    def email(e9, instid, port):
        import smtplib
        from email.message import EmailMessage
        with open(f'{e9}_{instid}.txt', 'r') as f:
            msg = EmailMessage()
            msg.set_content(f.read())
        msg['Subject'] = f'Low light levels on ONT-id {port} on {e9}'
        msg['From'] = 'nms@mycvecfiber.com'
        msg['To'] = 'dishman@cvecfiber.com'
        msg['Cc'] = 'jjackson@cvecfiber.com'
        s = smtplib.SMTP('10.20.7.31')
        s.send_message(msg)
        s.quit()

    def clean_up(e9, instid):
        from subprocess import run
        path.append(
            '/home/derrick/Documents/CVEC_Stuff/low-rx-pwr/')
        p1 = run('ls *.txt',
                 text=True,
                 shell=True,
                 capture_output=True
                 )
        for _ in p1.stdout.split():
            run(f'mv {e9}_{instid}.txt {path[-1]}/{e9}/{e9}_{instid}.txt',
                shell=True
                )

    alarms = tbl.split('\n')
    for alrm in alarms:
        data = alrm.split()
        if not len(data) >= 13:
            continue
        instid, gport = data[7], data[13].split("'")
        port = gport[1]
        ont_info = ont_detail(e9, port)
        cx_info = affected(instid, port, e9)
        all_info = f'{cx_info}\n{ont_info}'
        with open(f'{e9}_{instid}.txt', 'w') as f:
            f.write(all_info)
        email(e9, instid, port)
        clean_up(e9, instid)

        # with open(f'{e9}_{instid}.txt', 'a') as f:
        #   f.write(f'{acct}\n{name}\n{loc}\n{em}\n\n')
        #   affected(instid, port, e9)


e9, tbl = get_cmds()
cx_detail(e9, tbl)
