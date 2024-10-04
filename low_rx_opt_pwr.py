#!/usr/bin/python3

from datetime import date
from requests import get
from datetime import timedelta
from sys import argv, path
from netmiko import ConnectHandler

# Notes
# call main with diff alarm tables?


def send_commands():
    # Set dictionary variable for the arguments to ConnectHandler
    device = {'device_type': 'cisco_ios',
              'host':   f'{argv[1]}',
              'username':   'sysadmin',
              'password':   'Thesearethetimes!',
              'fast_cli':   False,
              }

    def cmds():
        cnct = ConnectHandler(**device)
        # Send commands down the ssh channel
        alrm_tbl = cnct.send_command_timing(
            'show alarm active | include low-rx-opt-pwr-[fn]e')
        cnct.send_command_timing('configure')
        hostname = cnct.send_command_timing(
            'show full-configuration hostname')
        cnct.send_command_timing('exit')
        # Sometimes you get the prompt back as a string in your data, we split here on \n and the [0] index is the hostname
        strip_prompt = hostname.split('\n')
        e9 = strip_prompt[0].lstrip('hostname ')
        return e9, alrm_tbl, cnct
    return cmds()


def cx_detail(e9, tbl, cnct):

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

    def affected(e9, instid, port):
        get_affected = get(f'https://10.20.7.10:18443/rest/v1/fault/export/csv/subscriber/device-name/{e9}/instance-id/{instid}',
                           auth=('admin', 'Thesearethetimes!'), verify=False)
        r = get_affected.text.split('\r\n')
        for i in r[1:-1]:
            get_phone = get(f'https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{port}%2Fx1',
                            auth=('admin', 'Thesearethetimes!'),
                            verify=False)
            r1 = get_phone.json()
            try:
                phone = r1.get('locations')[0].get('contacts')[0].get('phone')
                if phone is None:
                    phone = 'No phone'
            except:
                phone = 'No phone'
            sp = i.split(',')
            acct = sp[0]
            name = sp[1]
            loc = ' '.join(sp[2:5])
            em = sp[-1]
            if em == "":
                em = 'No email'
        return f'{acct}\n{name}\n{phone}\n{em}\n{loc}'

    def email(e9, instid, port):
        import smtplib
        from email.message import EmailMessage
        with open(f'{e9}_{date.today()}.txt', 'r') as f:
            msg = EmailMessage()
            msg.set_content(f.read())
        msg['Subject'] = f'Low light alarms on {e9}'
        msg['From'] = 'nms@mycvecfiber.com'
        msg['To'] = 'dishman@cvecfiber.com'
        msg['Cc'] = ['kmarshala@cvecfiber.com', 'jjackson@cvecfiber.com']
        s = smtplib.SMTP('10.20.7.31')
        s.send_message(msg)
        s.quit()

    def clean_up(e9, instid, cnct):
        from subprocess import run
        path.append(
            '/home/derrick/Documents/CVEC_Stuff/low-rx-pwr/')
        cnct.send_command_timing(
            f'manual acknowledge instance-id {instid}')
        run(f'mv {e9}_{date.today()}.txt {path[-1]}/{e9}/{e9}_{date.today()}.txt',
            shell=True
            )

    def process_alarm(tbl):
        alarms = tbl.split('\n')
        for alarm in alarms:
            data = alarm.split()
            if not len(data) >= 13:
                continue
            instid, gport = data[7], data[13].split("'")
            port = gport[1]
            ont_info = ont_detail(e9, port)
            cx_info = affected(e9, instid, port)
            all_info = f'{cx_info}{ont_info}\n'
            with open(f'{e9}_{date.today()}.txt', 'a') as f:
                f.write(all_info)
        email(e9, instid, port)
        clean_up(e9, instid, cnct)
        cnct.disconnect()

    process_alarm(tbl)


e9, tbl, cnct = send_commands()
cx_detail(e9, tbl, cnct)
