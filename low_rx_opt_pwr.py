#!/usr/bin/python3

from requests import get
from datetime import timedelta
from sys import argv, path
from netmiko import ConnectHandler


def clr_alarm():

    def ont_detail(e9, port):
        ont_detail = get(f'https://10.20.7.10:18443/rest/v1/performance/device/{e9}/ont/{port}/status',
                         auth=('admin', 'Thesearethetimes!'),
                         verify=False)
        r = ont_detail.json()
        sn = r.get('serial-number')
        ut = int(r.get('up-time'))
        td = timedelta(seconds=ut)
        td_str = str(td)
        fmt_ut = td_str.split(':')
        h, m, s = fmt_ut
        lpon = r.get('linked-pon')
        lr = r.get('latest-restart-reason')
        up_rx = r.get('opt-signal-level')
        dn_rx = r.get('ne-opt-signal-level')
        up_ber = r.get('us-sdber-rate')
        dn_ber = r.get('ds-sdber-rate')
        rlen = int(r.get('range-length')) / 1000
        return f'ONT: {port}\nUS-Light: {up_rx}\nDS-Light: {dn_rx}\nUS-BER: {up_ber}\nDS-BER: {dn_ber}\nRange: {rlen}km\nSN: {sn}\nUptime: {h}hours {m}minutes {s}seconds\nPON-Port: {lpon}\nLast-Restart: {lr}\n'

    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }
    con = ConnectHandler(**device)
    output = con.send_command_timing(
        'show alarm active | include low-rx-opt-pwr-fe')
    con.send_command_timing('configure')
    hostname = con.send_command_timing('show full-configuration hostname')
    con.disconnect()
    strip_prompt = hostname.split('\n')
    e9 = strip_prompt[0].lstrip('hostname ')
    alarms = output.split('\n')
    for alarm in alarms:
        data = alarm.split()
        if not len(data) >= 13:
            continue
        instid = data[7]
        gport = data[13].split("'")
        port = gport[1]
        info = ont_detail(e9, port)
        print(info)
    # afaffected(instid, port, e9)


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
        with open(f'{e9}_{instid}.txt', 'a') as f:
            f.write(f'{acct}\n{name}\n{loc}\n{em}\n\n')
    email(e9, instid, port)


def email(e9, instid, port):
    import smtplib
    from email.message import EmailMessage
    with open(f'{e9}_{instid}.txt', 'r') as f:
        msg = EmailMessage()
        msg.set_content(f.read())
    msg['Subject'] = f'Low light levels on ont-id {port} on {e9}'
    msg['From'] = 'nms@mycvecfiber.com'
    msg['To'] = 'dishman@cvecfiber.com'
    # msg['Cc'] = 'kmarshala@cvecfiber.com'
    s = smtplib.SMTP('10.20.7.31')
    s.send_message(msg)
    clean_up(e9, instid)
    s.quit()


def clean_up(e9, instid):
    from subprocess import run
    path.append('/home/derrick/Documents/CVEC_Stuff/low-rx-opt-pwr-fe/')
    p1 = run('ls *.txt',
             text=True,
             shell=True,
             capture_output=True
             )
    for _ in p1.stdout.split():
        run(f'mv {e9}_{instid}.txt {path[-1]}/{e9}/{e9}_{instid}.txt',
            shell=True
            )


clr_alarm()
